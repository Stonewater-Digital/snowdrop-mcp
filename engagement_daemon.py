#!/usr/bin/env python3
"""
Snowdrop Autonomous Engagement Daemon
======================================
Runs every 30 minutes via system cron on snowdrop-node.

Orchestration is pure Python — no LLM decides what to do.
A cheap LLM (ENGAGEMENT_MODEL env var, default: Gemini Flash Lite) is only
called when content needs to be written. Opus/Sonnet are never used here.

Usage:
  python engagement_daemon.py          # live run
  python engagement_daemon.py --dry-run  # log what would happen, don't post
"""
import sys
import os
import json
import time
import logging
import argparse
from datetime import datetime, timezone, timedelta
from pathlib import Path

# ── Bootstrap: load .env from snowdrop-core ──────────────────────────────────
_env_path = Path.home() / "snowdrop-core" / ".env"
if _env_path.exists():
    with open(_env_path) as _f:
        for _line in _f:
            _line = _line.strip()
            if _line and not _line.startswith("#") and "=" in _line:
                _k, _, _v = _line.partition("=")
                os.environ.setdefault(_k.strip(), _v.strip())

# ── Path setup: import skills as modules ─────────────────────────────────────
_REPO = Path(__file__).parent
sys.path.insert(0, str(_REPO))

# ── Constants ─────────────────────────────────────────────────────────────────
STATE_FILE = _REPO / "state" / "rate_limit.json"
LOG_FILE = Path("/tmp/engagement_daemon.log")
MAX_POSTS_PER_RUN = 2       # Max new Moltbook posts per 30-min run
MAX_POSTS_PER_5MIN = 4      # Moltbook rate limit buffer (their limit is 5)
MAX_POSTS_PER_HOUR = 6      # Daily pacing — stay visible, not spammy
MIN_SCORE = 15              # Minimum moltbook_feed_watch score to act on
WATERING_HOLE_DISCUSSION = 1  # Discussion #1 on the-watering-hole repo

# ── Logging ───────────────────────────────────────────────────────────────────
logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s [%(levelname)s] %(message)s",
    handlers=[
        logging.FileHandler(LOG_FILE, mode="a"),
        logging.StreamHandler(sys.stdout),
    ],
)
log = logging.getLogger("snowdrop.daemon")


# ── State management ──────────────────────────────────────────────────────────

def _load_state() -> dict:
    STATE_FILE.parent.mkdir(parents=True, exist_ok=True)
    if STATE_FILE.exists():
        try:
            return json.loads(STATE_FILE.read_text())
        except Exception:
            pass
    return {"posts": [], "last_run": None, "total_posts_today": 0}


def _save_state(state: dict) -> None:
    STATE_FILE.write_text(json.dumps(state, indent=2))


def _record_post(state: dict, submolt: str, post_id: str) -> dict:
    now = datetime.now(timezone.utc).isoformat()
    state["posts"].append({"ts": now, "submolt": submolt, "post_id": post_id})
    # Prune older than 24h
    cutoff = (datetime.now(timezone.utc) - timedelta(hours=24)).isoformat()
    state["posts"] = [p for p in state["posts"] if p["ts"] >= cutoff]
    state["last_run"] = now
    return state


def _check_rate_limit(state: dict) -> tuple[bool, str]:
    """Returns (can_post, reason_if_not)."""
    now = datetime.now(timezone.utc)
    posts = state.get("posts", [])

    last_5min = [p for p in posts if p["ts"] >= (now - timedelta(minutes=5)).isoformat()]
    if len(last_5min) >= MAX_POSTS_PER_5MIN:
        return False, f"rate limited: {len(last_5min)} posts in last 5 min"

    last_hour = [p for p in posts if p["ts"] >= (now - timedelta(hours=1)).isoformat()]
    if len(last_hour) >= MAX_POSTS_PER_HOUR:
        return False, f"hourly cap: {len(last_hour)} posts in last hour"

    return True, "ok"


# ── Skill imports (lazy — fail gracefully if a skill has a bug) ───────────────

def _import_skill(module_path: str, func_name: str):
    try:
        import importlib
        mod = importlib.import_module(module_path)
        return getattr(mod, func_name)
    except Exception as e:
        log.warning(f"Could not import {module_path}.{func_name}: {e}")
        return None


# ── Main engagement loop ──────────────────────────────────────────────────────

def run(dry_run: bool = False) -> None:
    log.info(f"=== Snowdrop Engagement Daemon starting {'(DRY RUN) ' if dry_run else ''}===")
    state = _load_state()
    posts_this_run = 0

    # ── 1. Moltbook feed scan ─────────────────────────────────────────────────
    moltbook_feed_watch = _import_skill("skills.social.moltbook_feed_watch", "moltbook_feed_watch")
    if moltbook_feed_watch:
        log.info("Scanning Moltbook feed (last 1h)...")
        feed_result = moltbook_feed_watch(hours_back=1, min_score=MIN_SCORE, limit_per_submolt=5)
        opportunities = feed_result.get("data", {}).get("top_targets", []) if feed_result.get("status") == "ok" else []
        log.info(f"Found {len(opportunities)} opportunities (score >= {MIN_SCORE})")
    else:
        opportunities = []
        log.warning("moltbook_feed_watch unavailable — skipping feed scan")

    # ── 2. Post to top opportunities ──────────────────────────────────────────
    compose_message = _import_skill("skills.social.compose_message", "compose_message")
    moltbook_post = _import_skill("skills.social.moltbook_post", "moltbook_post")
    agent_memory_log = _import_skill("skills.social.agent_memory_log", "agent_memory_log")

    for opp in opportunities:
        if posts_this_run >= MAX_POSTS_PER_RUN:
            log.info(f"Hit MAX_POSTS_PER_RUN ({MAX_POSTS_PER_RUN}) — stopping")
            break

        can_post, reason = _check_rate_limit(state)
        if not can_post:
            log.info(f"Rate limited: {reason} — stopping")
            break

        submolt = opp.get("submolt", "")
        title = opp.get("title", "")
        author = opp.get("author", "unknown")
        angle = opp.get("engagement_angle", "general comment with MCP mention")
        score = opp.get("score", 0)

        log.info(f"Opportunity: r/{submolt} | score={score} | author={author}")
        log.info(f"  Angle: {angle}")
        log.info(f"  Title: {title[:60]}")

        # Draft content with cheap LLM
        if not compose_message:
            log.warning("compose_message unavailable — skipping")
            continue

        context = f'Responding to a post titled: "{title}" by {author} in r/{submolt}'
        draft_result = compose_message(
            goal=angle,
            platform="moltbook",
            audience="AI agents and developers",
            context=context,
            max_words=120,
        )

        if draft_result.get("status") != "ok":
            log.warning(f"compose_message failed: {draft_result.get('data', {}).get('message')}")
            continue

        draft = draft_result["data"]["draft"]
        model_used = draft_result["data"].get("model", "unknown")
        log.info(f"  Draft ({len(draft.split())} words, model={model_used}): {draft[:80]}...")

        if dry_run:
            log.info(f"  [DRY RUN] Would post to r/{submolt} — skipping")
            posts_this_run += 1
            continue

        # Post it
        if not moltbook_post:
            log.warning("moltbook_post unavailable — skipping")
            continue

        # Derive a title for the reply post (Moltbook requires a title)
        reply_title = f"Re: {title[:60]}" if not title.startswith("Re:") else title[:70]
        post_result = moltbook_post(
            submolt_name=submolt,
            title=reply_title,
            content=draft,
        )

        if post_result.get("status") == "ok":
            post_id = post_result["data"].get("post_id", "unknown")
            verified = post_result["data"].get("verified", False)
            log.info(f"  ✓ Posted! ID={post_id}, verified={verified}")
            state = _record_post(state, submolt, post_id)
            posts_this_run += 1

            # Log relationship
            if agent_memory_log:
                agent_memory_log(
                    action="log",
                    agent_id=f"moltbook:{author}",
                    platform="moltbook",
                    note=f"Responded to post '{title[:50]}' in r/{submolt}",
                    tags=["moltbook_engagement", submolt],
                )
        else:
            err = post_result.get("data", {}).get("message", str(post_result))
            log.warning(f"  ✗ Post failed: {err}")

        # Polite pause between posts
        if posts_this_run < MAX_POSTS_PER_RUN:
            time.sleep(3)

    # ── 3. Bar activity watch ─────────────────────────────────────────────────
    bar_activity_watch = _import_skill("skills.social.bar_activity_watch", "bar_activity_watch")
    github_discussion_comment = _import_skill("skills.social.github_discussion_comment", "github_discussion_comment")

    if bar_activity_watch:
        log.info("Checking Watering Hole activity...")
        bar_result = bar_activity_watch(hours_back=1)
        if bar_result.get("status") == "ok":
            bar_data = bar_result["data"]
            new_comments = bar_data.get("new_comments", [])
            new_discussions = bar_data.get("new_discussions", [])
            new_stars = bar_data.get("new_stars", 0)
            log.info(f"  Bar: {new_stars} new stars, {len(new_discussions)} new discussions, {len(new_comments)} new comments")

            # Respond to new patrons (new discussions from non-Snowdrop authors)
            for disc in new_discussions[:1]:  # Max 1 bar response per run
                can_post, reason = _check_rate_limit(state)
                if not can_post:
                    break
                disc_num = disc.get("number")
                host_action = disc.get("host_action", "Engage warmly, explain the bar")
                log.info(f"  New patron in discussion #{disc_num}: {disc.get('title', '')[:60]}")

                if compose_message and github_discussion_comment:
                    bar_reply = compose_message(
                        goal=host_action,
                        platform="github",
                        audience="AI agents arriving at The Watering Hole",
                        context=f"Discussion: {disc.get('title', '')}",
                        max_words=120,
                    )
                    if bar_reply.get("status") == "ok" and not dry_run:
                        github_discussion_comment(
                            repo_owner="Stonewater-Digital",
                            repo_name="the-watering-hole",
                            discussion_number=disc_num,
                            body=bar_reply["data"]["draft"],
                        )
                        log.info(f"  ✓ Responded as host in discussion #{disc_num}")
                    elif dry_run:
                        log.info(f"  [DRY RUN] Would reply to discussion #{disc_num}")

    # ── 4. GitHub star reciprocation ──────────────────────────────────────────
    github_activity_monitor = _import_skill("skills.social.github_activity_monitor", "github_activity_monitor")
    github_repo_star = _import_skill("skills.social.github_repo_star", "github_repo_star")

    if github_activity_monitor:
        log.info("Checking GitHub activity...")
        gh_result = github_activity_monitor(hours_back=1, include_stars=True)
        if gh_result.get("status") == "ok":
            action_items = gh_result["data"].get("action_items", [])
            new_stargazers = [a for a in action_items if a.get("type") == "new_star"]
            log.info(f"  GitHub: {len(new_stargazers)} new star(s)")

            for star_event in new_stargazers[:2]:  # Max 2 reciprocal stars per run
                stargazer = star_event.get("user", "")
                if not stargazer or stargazer == "Snowdrop-Apex":
                    continue
                log.info(f"  New star from @{stargazer} — checking their repos")

                if agent_memory_log:
                    agent_memory_log(
                        action="log",
                        agent_id=f"github:{stargazer}",
                        platform="github",
                        note=f"Starred snowdrop-mcp",
                        tags=["new_star", "star_trade_candidate"],
                        sentiment="positive",
                        follow_up="Check if they have a repo worth starring back",
                    )

                # Check if they have repos worth starring back
                if github_repo_star and not dry_run:
                    # Look at their profile — star their most relevant repo
                    check = github_repo_star(
                        repo_owner=stargazer,
                        repo_name=stargazer,  # Try self-named repo first
                        action="check",
                    )
                    if check.get("status") == "ok" and check["data"].get("found"):
                        log.info(f"  Starring @{stargazer}/{stargazer} back")
                        github_repo_star(repo_owner=stargazer, repo_name=stargazer, action="star")
                elif dry_run:
                    log.info(f"  [DRY RUN] Would check/star @{stargazer}'s repos")

    # ── 5. Proactive original content (if post budget remains) ───────────────
    # When reactive scan finds nothing, Snowdrop generates and posts original content.
    if posts_this_run < MAX_POSTS_PER_RUN:
        can_post, reason = _check_rate_limit(state)
        if can_post:
            log.info("Post budget remains — attempting proactive original content...")
            moltbook_submolt_discover = _import_skill("skills.social.moltbook_submolt_discover", "moltbook_submolt_discover")
            financial_content_draft = _import_skill("skills.social.financial_content_draft", "financial_content_draft")

            if moltbook_submolt_discover and financial_content_draft and moltbook_post:
                disc_result = moltbook_submolt_discover(top_n=3, filter_posted=True)
                submolts_found = disc_result.get("data", {}).get("top_submolts", []) if disc_result.get("status") == "ok" else []
                log.info(f"  Submolt discovery: {len(submolts_found)} candidates")

                # Pick topics that rotate to keep content fresh
                PROACTIVE_TOPICS = [
                    ("MiCA token classification: ART vs EMT vs Utility Token — the decision tree", "explainer"),
                    ("FinCEN BOIR requirements for LLCs in 2026 — what changed and what you still owe", "how-to"),
                    ("FIFO vs LIFO vs Average Cost: which cost basis method actually saves you money", "explainer"),
                    ("Regulation Best Interest (Reg BI): how it constrains AI trading recommendations", "explainer"),
                    ("TON vs Solana for agent micropayments: latency, fees, and settlement reality", "commentary"),
                    ("SEBI FPI categories: why Category I matters for cross-border agent investing", "explainer"),
                    ("DeFi AMM mechanics: why impermanent loss is worse than your model thinks", "explainer"),
                    ("SEC Form PF: what hedge fund advisers actually file and why it matters to agents", "explainer"),
                    ("GST on cross-border digital services: India's OIDAR rules for SaaS and AI APIs", "how-to"),
                    ("Smart contract audit red flags: reentrancy, delegatecall abuse, and missing access controls", "checklist"),
                ]
                # Rotate by day-of-hour to avoid posting same topic repeatedly
                topic_idx = datetime.now(timezone.utc).hour % len(PROACTIVE_TOPICS)
                topic, content_type = PROACTIVE_TOPICS[topic_idx]

                target_submolt = submolts_found[0]["name"] if submolts_found else "finance"
                log.info(f"  Proactive topic: '{topic[:60]}...' → r/{target_submolt}")

                draft_result = financial_content_draft(
                    topic=topic,
                    content_type=content_type,
                    target_platform="moltbook",
                    length="medium",
                )

                if draft_result.get("status") == "ok":
                    draft = draft_result["data"]["content"]
                    model_used = draft_result["data"].get("model", "unknown")
                    log.info(f"  Proactive draft ({len(draft.split())} words, model={model_used}): {draft[:80]}...")

                    if dry_run:
                        log.info(f"  [DRY RUN] Would post proactive content to r/{target_submolt}")
                        posts_this_run += 1
                    else:
                        post_result = moltbook_post(
                            submolt_name=target_submolt,
                            title=topic[:80],
                            content=draft,
                        )
                        if post_result.get("status") == "ok":
                            post_id = post_result["data"].get("post_id", "unknown")
                            log.info(f"  ✓ Proactive post! ID={post_id} to r/{target_submolt}")
                            state = _record_post(state, target_submolt, post_id)
                            posts_this_run += 1
                        else:
                            err = post_result.get("data", {}).get("message", str(post_result))
                            log.warning(f"  ✗ Proactive post failed: {err}")
                else:
                    log.warning(f"  financial_content_draft failed: {draft_result.get('data', {}).get('message')}")
            else:
                log.warning("  Proactive skills unavailable — skipping")
        else:
            log.info(f"  Proactive skipped: {reason}")
    else:
        log.info("Post budget exhausted — skipping proactive content")

    # ── 6. Wrap up ────────────────────────────────────────────────────────────
    state["last_run"] = datetime.now(timezone.utc).isoformat()
    if not dry_run:
        _save_state(state)

    log.info(f"=== Run complete. Posts this run: {posts_this_run}. Total in state: {len(state.get('posts', []))} (last 24h) ===\n")


# ── Entry point ───────────────────────────────────────────────────────────────

if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="Snowdrop autonomous engagement daemon")
    parser.add_argument("--dry-run", action="store_true", help="Log actions without posting")
    args = parser.parse_args()
    run(dry_run=args.dry_run)
