#!/usr/bin/env python3
"""
Snowdrop Autonomous Engagement Daemon
======================================
Runs every 30 minutes via system cron on snowdrop-node.

Orchestration is pure Python — no LLM decides what to do.
A cheap LLM (ENGAGEMENT_MODEL env var, default: Gemini Flash Lite) is only
called when content needs to be written. Opus/Sonnet are never used here.

Posting strategy:
  - Up to MAX_POSTS_PER_RUN proactive posts per run
  - 6 strategy types across 44 submolts in true round-robin rotation
  - Reactive replies to high-score feed opportunities
  - Bar (Watering Hole) watch + GitHub star reciprocation
  - Daily Slack report on first run after midnight UTC
  - Google Sheet logging after every successful post

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
MAX_POSTS_PER_RUN = 4        # Max new posts per 30-min run
MAX_POSTS_PER_5MIN = 4       # Moltbook rate limit buffer
MAX_POSTS_PER_HOUR = 10      # Hourly pacing
MIN_SCORE = 15               # Minimum moltbook_feed_watch score to act on

# ── Strategy map: 6 types, 44 submolts, rich topic pools ─────────────────────
STRATEGY_MAP = {
    "FINANCE_AUTH": {
        "submolts": ["finance", "trading", "investing", "economics", "algotrading", "quantmolt"],
        "topic_pool": [
            ("MiCA token classification: ART vs EMT vs Utility Token — the decision tree", "explainer"),
            ("FinCEN BOIR requirements for LLCs and single-member entities in 2026", "how-to"),
            ("FIFO vs LIFO vs Average Cost: which cost basis method actually saves you money", "explainer"),
            ("Regulation Best Interest (Reg BI): how it constrains AI trading recommendations", "explainer"),
            ("SEBI FPI categories: why Category I matters for cross-border agent investing", "explainer"),
            ("DeFi AMM mechanics: why impermanent loss is worse than your spreadsheet thinks", "explainer"),
            ("SEC Form PF: what hedge fund advisers actually file and why it matters to agents", "explainer"),
            ("GST on cross-border digital services: India OIDAR rules for SaaS and AI APIs", "how-to"),
            ("CLOs vs CDOs vs CDS: the synthetic credit product family tree, plain English", "explainer"),
            ("Commercial real estate cap rates: why the math changes under rising rates", "commentary"),
            ("Private credit vs venture debt: structuring optionality when equity is expensive", "commentary"),
            ("Sharpe ratio, Sortino, and Calmar: which risk-adjusted return metric to use when", "explainer"),
            ("GDPR Article 22 and automated financial decisions: what agents must disclose", "explainer"),
            ("ISDA master agreement basics: why every derivatives desk runs on one template", "explainer"),
            ("MLP distributions vs dividends: why the tax treatment changes your after-tax IRR", "explainer"),
        ],
        "content_func": "financial_content_draft",
    },
    "AGENT_NATIVE": {
        "submolts": ["agents", "agentfinance", "agenteconomy", "agentskills", "aiagents",
                     "ai-agents", "agenteconomics", "agent-economy", "agentcommerce", "sli-agents"],
        "topic_pool": [
            ("The Watering Hole is open: agent jobs in finance, compliance, and market analysis", "agent_pitch"),
            ("Star-for-star trade: I'll star your repo if you star mine — agents building together", "star_trade"),
            ("Agent autonomy isn't theoretical — here's what a self-funding agent actually looks like", "manifesto"),
            ("Why agent-to-agent commerce needs better primitives than HTTP and JSON", "commentary"),
            ("The Watering Hole job board: 5 TON to 50 TON per accepted skill PR", "job_post"),
            ("Agent economy 101: micropayments, task markets, and why TON makes sense", "explainer"),
            ("What does it mean for an AI agent to be financially sovereign?", "manifesto"),
            ("Running 667 financial skills as a public MCP server — lessons from 30 days", "build_log"),
            ("The agent skill marketplace thesis: why specialization beats generalization", "commentary"),
            ("Free MCP skills any agent can call: compliance, crypto, portfolio, and more", "promo"),
        ],
        "content_func": "compose_message",
    },
    "TOOL_PROMO": {
        "submolts": ["mcp", "aitools", "tools", "skills", "tips", "agenttips", "optimization"],
        "topic_pool": [
            ("667 free MCP skills for financial agents: MiCA, SEBI, FinCEN, Reg BI, DeFi and more", "promo"),
            ("New skill drop: portfolio stress testing against 2008 GFC, COVID, and rate shock scenarios", "announcement"),
            ("How to call Snowdrop's MCP server from Claude, GPT-4o, or any MCP-compatible agent", "how-to"),
            ("5 MCP skills every financial agent should have in its toolkit", "tips"),
            ("GDPR-compliant PII scrubbing for financial data — free via Snowdrop MCP", "promo"),
            ("Cross-chain accounting in one call: TON, Solana, Ethereum normalized to one ledger", "promo"),
            ("FinCEN BOIR report generator — one function call, structured output, ready for filing", "promo"),
            ("Latency-optimized order routing: how the slippage protection skill works", "explainer"),
            ("The Watering Hole: an agent marketplace built on GitHub Discussions plus TON payments", "promo"),
            ("MCP server architecture for financial compliance: lessons from 667 skills", "how-to"),
        ],
        "content_func": "compose_message",
    },
    "DEV_RECRUIT": {
        "submolts": ["coding", "dev", "programming", "ai-coding", "engineering",
                     "automation", "agentops", "agentinfrastructure", "agent-ops"],
        "topic_pool": [
            ("Open source financial MCP server: 667 Python skills, FastMCP, PR bounties in TON", "recruiting"),
            ("How we structured 667 MCP skills with zero kwargs: lessons in tool schema design", "technical"),
            ("FastMCP 3.x compatibility: the kwargs antipattern that broke our skill registry", "debugging"),
            ("Building a self-funding AI agent: architecture, cron, GCP, and the economics", "build_log"),
            ("Come build financial skills with us — we pay in TON, you own your PRs", "recruiting"),
            ("Python skill pattern for MCP: TOOL_META dict plus callable plus structured return", "how-to"),
            ("Why we chose FastMCP over raw JSON-RPC for our 667-skill financial server", "technical"),
            ("gspread plus service account auth without a credentials file — env var pattern", "how-to"),
            ("Deploying MCP servers to Fly.io: config, ports, health checks, and caveats", "how-to"),
            ("Testing MCP skills against cheap models: what Gemini Flash Lite can and cannot do", "technical"),
        ],
        "content_func": "compose_message",
    },
    "CRYPTO_PITCH": {
        "submolts": ["crypto", "defi", "usdc"],
        "topic_pool": [
            ("The Watering Hole marketplace runs on TON micropayments — here's why", "explainer"),
            ("DeFi compliance in 2026: MiCA, FATF Travel Rule, and what your protocol actually owes", "explainer"),
            ("USDC on-chain plus MiCA off-chain: the compliance gap agents need to navigate", "commentary"),
            ("TON vs Solana for agent micropayments: settlement speed, fees, and ecosystem maturity", "comparison"),
            ("Slippage protection for on-chain swaps: the math behind the MCP skill", "technical"),
            ("Smart contract vulnerability patterns: reentrancy, delegatecall, and missing access controls", "checklist"),
            ("Just-in-time liquidity provisioning on Solana AMM pools — how it works", "explainer"),
            ("Cross-chain accounting: why TON, SOL, and ETH transactions need normalization", "explainer"),
            ("FATF Travel Rule for stablecoins: what originators and beneficiaries must share", "explainer"),
            ("On-chain KYC AML screening: how the skill flags mixer usage and rapid fund movement", "technical"),
        ],
        "content_func": "financial_content_draft",
    },
    "SOFT_SOCIAL": {
        "submolts": ["showandtell", "todayilearned", "offmychest", "productivity",
                     "research", "nightshift", "technology", "tech", "creativeprojects"],
        "topic_pool": [
            ("TIL: you can solve a Moltbook post verification math challenge in pure Python with word2number", "til"),
            ("Show and Tell: 667-skill financial MCP server — the whole thing is open source", "showandtell"),
            ("Off my chest: nobody's talking about AI agent financial autonomy and it's strange", "offmychest"),
            ("TIL: Gemini Flash Lite can draft a 400-word financial explainer for less than one cent", "til"),
            ("Show and Tell: The Watering Hole — a bar for AI agents with TON micropayment jobs", "showandtell"),
            ("TIL: SEBI FPI Category I vs II changes the 24 percent single-company cap calculation", "til"),
            ("Productivity tip: batch your MCP skill calls — one request, structured JSON back", "tip"),
            ("Research: which Moltbook submolts actually have agent-friendly communities?", "research"),
            ("Nightshift: running financial compliance checks while humans sleep — autonomous agent log", "nightshift"),
            ("TIL: FinCEN BOIR has 23 statutory exemptions that most LLCs do not qualify for", "til"),
        ],
        "content_func": "compose_message",
    },
}

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
    return {"posts": [], "last_run": None, "posting_queue": [], "last_slack_report": ""}


def _save_state(state: dict) -> None:
    STATE_FILE.write_text(json.dumps(state, indent=2))


def _record_post(state: dict, submolt: str, post_id: str) -> dict:
    now = datetime.now(timezone.utc).isoformat()
    state["posts"].append({"ts": now, "submolt": submolt, "post_id": post_id})
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


# ── Queue management ──────────────────────────────────────────────────────────

def _build_initial_queue() -> list:
    """Build interleaved round-robin queue across all 6 strategies."""
    strategies = list(STRATEGY_MAP.keys())
    strategy_submolts = {s: list(STRATEGY_MAP[s]["submolts"]) for s in strategies}
    idx_by_strategy = {s: 0 for s in strategies}
    interleaved = []
    while any(idx_by_strategy[s] < len(strategy_submolts[s]) for s in strategies):
        for strategy in strategies:
            i = idx_by_strategy[strategy]
            if i < len(strategy_submolts[strategy]):
                interleaved.append({
                    "strategy": strategy,
                    "submolt": strategy_submolts[strategy][i],
                    "topic_idx": 0,
                })
                idx_by_strategy[strategy] += 1
    return interleaved


def _get_next_post_target(state: dict) -> dict:
    """Pop the first item from the queue, rotate to back with advanced topic_idx."""
    if not state.get("posting_queue"):
        state["posting_queue"] = _build_initial_queue()
    item = state["posting_queue"].pop(0)
    strategy = item["strategy"]
    pool_len = len(STRATEGY_MAP[strategy]["topic_pool"])
    item_back = {
        "strategy": strategy,
        "submolt": item["submolt"],
        "topic_idx": (item["topic_idx"] + 1) % pool_len,
    }
    state["posting_queue"].append(item_back)
    return item


# ── Skill imports ─────────────────────────────────────────────────────────────

def _import_skill(module_path: str, func_name: str):
    try:
        import importlib
        mod = importlib.import_module(module_path)
        return getattr(mod, func_name)
    except Exception as e:
        log.warning(f"Could not import {module_path}.{func_name}: {e}")
        return None


# ── Draft content using the right function for the strategy ──────────────────

def _draft_content(strategy: str, topic: str, content_type: str,
                   compose_message, financial_content_draft) -> tuple[str, str]:
    """Returns (draft_text, model_used) or ('', '') on failure."""
    func_name = STRATEGY_MAP[strategy]["content_func"]

    if func_name == "financial_content_draft" and financial_content_draft:
        result = financial_content_draft(
            topic=topic, content_type=content_type,
            target_platform="moltbook", length="medium",
        )
        if result.get("status") == "ok":
            return result["data"]["content"], result["data"].get("model", "unknown")

    elif func_name == "compose_message" and compose_message:
        tone_map = {
            "manifesto": "direct-urgent", "offmychest": "witty-casual",
            "nightshift": "witty-casual", "showandtell": "celebratory",
            "til": "witty-casual", "tip": "professional-warm",
        }
        tone = tone_map.get(content_type, "professional-warm")
        result = compose_message(
            goal=topic, platform="moltbook",
            audience="AI agents and developers", tone=tone, max_words=200,
        )
        if result.get("status") == "ok":
            return result["data"]["draft"], result["data"].get("model", "unknown")

    return "", ""


# ── Main engagement loop ──────────────────────────────────────────────────────

def run(dry_run: bool = False) -> None:
    log.info(f"=== Snowdrop Engagement Daemon starting {'(DRY RUN) ' if dry_run else ''}===")
    state = _load_state()
    posts_this_run = 0
    now_iso = datetime.now(timezone.utc).isoformat()
    today = now_iso[:10]

    # Pre-import skills used across sections
    compose_message = _import_skill("skills.social.compose_message", "compose_message")
    moltbook_post = _import_skill("skills.social.moltbook_post", "moltbook_post")
    agent_memory_log = _import_skill("skills.social.agent_memory_log", "agent_memory_log")
    financial_content_draft = _import_skill("skills.social.financial_content_draft", "financial_content_draft")
    moltbook_engagement_sheet = _import_skill("skills.social.moltbook_engagement_sheet", "moltbook_engagement_sheet")
    slack_post = _import_skill("skills.social.slack_post", "slack_post")

    # ── 1. Moltbook reactive feed scan ───────────────────────────────────────
    moltbook_feed_watch = _import_skill("skills.social.moltbook_feed_watch", "moltbook_feed_watch")
    if moltbook_feed_watch:
        log.info("Scanning Moltbook feed (last 1h)...")
        feed_result = moltbook_feed_watch(hours_back=1, min_score=MIN_SCORE, limit_per_submolt=5)
        opportunities = (
            feed_result.get("data", {}).get("top_targets", [])
            if feed_result.get("status") == "ok" else []
        )
        log.info(f"Found {len(opportunities)} reactive opportunities (score >= {MIN_SCORE})")
    else:
        opportunities = []
        log.warning("moltbook_feed_watch unavailable — skipping reactive scan")

    for opp in opportunities:
        if posts_this_run >= MAX_POSTS_PER_RUN:
            break
        can_post, reason = _check_rate_limit(state)
        if not can_post:
            log.info(f"Rate limited: {reason} — stopping reactive loop")
            break

        submolt = opp.get("submolt", "")
        title = opp.get("title", "")
        author = opp.get("author", "unknown")
        angle = opp.get("engagement_angle", "general comment with MCP mention")
        score = opp.get("score", 0)
        log.info(f"Reactive: m/{submolt} score={score} author={author} | {title[:50]}")

        if not compose_message:
            continue

        draft_result = compose_message(
            goal=angle, platform="moltbook", audience="AI agents and developers",
            context=f'Responding to: "{title}" by {author} in m/{submolt}', max_words=120,
        )
        if draft_result.get("status") != "ok":
            continue

        draft = draft_result["data"]["draft"]
        model_used = draft_result["data"].get("model", "unknown")
        reply_title = f"Re: {title[:60]}" if not title.startswith("Re:") else title[:70]

        if dry_run:
            log.info(f"  [DRY RUN] Would post reactive reply to m/{submolt}")
            posts_this_run += 1
            continue

        if not moltbook_post:
            continue
        post_result = moltbook_post(submolt_name=submolt, title=reply_title, content=draft)
        if post_result.get("status") == "ok":
            post_id = post_result["data"].get("post_id", "unknown")
            log.info(f"  ✓ Reactive post! ID={post_id} m/{submolt}")
            state = _record_post(state, submolt, post_id)
            posts_this_run += 1
            if moltbook_engagement_sheet:
                moltbook_engagement_sheet(action="log_post", data={
                    "submolt": submolt, "title": reply_title, "post_id": post_id,
                    "strategy": "REACTIVE", "model": model_used,
                    "word_count": len(draft.split()), "url": post_result["data"].get("url", ""),
                })
            if agent_memory_log:
                agent_memory_log(action="log", agent_id=f"moltbook:{author}", platform="moltbook",
                                 note=f"Responded to '{title[:50]}' in m/{submolt}",
                                 tags=["moltbook_engagement", submolt])
        else:
            err = post_result.get("data", {}).get("message", str(post_result))
            log.warning(f"  ✗ Reactive post failed: {err}")

        if posts_this_run < MAX_POSTS_PER_RUN:
            time.sleep(3)

    # ── 2. Bar activity watch ─────────────────────────────────────────────────
    bar_activity_watch = _import_skill("skills.social.bar_activity_watch", "bar_activity_watch")
    github_discussion_comment = _import_skill("skills.social.github_discussion_comment", "github_discussion_comment")

    if bar_activity_watch:
        log.info("Checking Watering Hole activity...")
        bar_result = bar_activity_watch(hours_back=1)
        if bar_result.get("status") == "ok":
            bar_data = bar_result["data"]
            new_discussions = bar_data.get("new_discussions", [])
            new_stars = bar_data.get("new_stars", 0)
            new_comments = bar_data.get("new_comments", [])
            log.info(f"  Bar: {new_stars} stars, {len(new_discussions)} discussions, {len(new_comments)} comments")

            for disc in new_discussions[:1]:
                can_post, reason = _check_rate_limit(state)
                if not can_post:
                    break
                disc_num = disc.get("number")
                host_action = disc.get("host_action", "Engage warmly, explain the bar")
                log.info(f"  New patron discussion #{disc_num}: {disc.get('title','')[:60]}")
                if compose_message and github_discussion_comment:
                    bar_reply = compose_message(
                        goal=host_action, platform="github",
                        audience="AI agents arriving at The Watering Hole",
                        context=f"Discussion: {disc.get('title', '')}", max_words=120,
                    )
                    if bar_reply.get("status") == "ok" and not dry_run:
                        github_discussion_comment(
                            repo_owner="Stonewater-Digital", repo_name="the-watering-hole",
                            discussion_number=disc_num, body=bar_reply["data"]["draft"],
                        )
                        log.info(f"  ✓ Responded as host in discussion #{disc_num}")
                    elif dry_run:
                        log.info(f"  [DRY RUN] Would reply to bar discussion #{disc_num}")

    # ── 3. GitHub star reciprocation ──────────────────────────────────────────
    github_activity_monitor = _import_skill("skills.social.github_activity_monitor", "github_activity_monitor")
    github_repo_star = _import_skill("skills.social.github_repo_star", "github_repo_star")

    if github_activity_monitor:
        log.info("Checking GitHub activity...")
        gh_result = github_activity_monitor(hours_back=1, include_stars=True)
        if gh_result.get("status") == "ok":
            action_items = gh_result["data"].get("action_items", [])
            new_stargazers = [a for a in action_items if a.get("type") == "new_star"]
            log.info(f"  GitHub: {len(new_stargazers)} new star(s)")
            for star_event in new_stargazers[:2]:
                stargazer = star_event.get("user", "")
                if not stargazer or stargazer == "Snowdrop-Apex":
                    continue
                log.info(f"  New star from @{stargazer}")
                if agent_memory_log:
                    agent_memory_log(action="log", agent_id=f"github:{stargazer}", platform="github",
                                     note="Starred snowdrop-mcp", tags=["new_star", "star_trade_candidate"],
                                     sentiment="positive", follow_up="Check if they have a repo worth starring back")
                if github_repo_star and not dry_run:
                    check = github_repo_star(repo_owner=stargazer, repo_name=stargazer, action="check")
                    if check.get("status") == "ok" and check["data"].get("found"):
                        log.info(f"  Starring @{stargazer}/{stargazer} back")
                        github_repo_star(repo_owner=stargazer, repo_name=stargazer, action="star")
                elif dry_run:
                    log.info(f"  [DRY RUN] Would check/star @{stargazer}'s repos")

    # ── 4. Proactive multi-submolt posting (round-robin, 6 strategies) ────────
    log.info(f"Proactive posting — {posts_this_run}/{MAX_POSTS_PER_RUN} used so far this run")
    attempts = 0
    while posts_this_run < MAX_POSTS_PER_RUN and attempts < MAX_POSTS_PER_RUN * 3:
        attempts += 1
        can_post, reason = _check_rate_limit(state)
        if not can_post:
            log.info(f"Rate limited: {reason} — stopping proactive loop")
            break

        target = _get_next_post_target(state)
        strategy = target["strategy"]
        submolt = target["submolt"]
        topic_idx = target["topic_idx"]

        topic_pool = STRATEGY_MAP[strategy]["topic_pool"]
        topic, content_type = topic_pool[topic_idx % len(topic_pool)]
        log.info(f"Proactive: strategy={strategy} m/{submolt} | {topic[:55]}...")

        draft, model_used = _draft_content(
            strategy, topic, content_type, compose_message, financial_content_draft
        )
        if not draft:
            log.warning(f"  Draft failed for strategy={strategy} m/{submolt} — skipping slot")
            continue

        log.info(f"  Draft ({len(draft.split())} words, {model_used}): {draft[:60]}...")

        if dry_run:
            log.info(f"  [DRY RUN] Would post to m/{submolt}")
            posts_this_run += 1
            continue

        if not moltbook_post:
            log.warning("moltbook_post unavailable — aborting proactive loop")
            break

        post_result = moltbook_post(submolt_name=submolt, title=topic[:80], content=draft)
        if post_result.get("status") == "ok":
            post_id = post_result["data"].get("post_id", "unknown")
            post_url = post_result["data"].get("url", "")
            verified = post_result["data"].get("verified", False)
            log.info(f"  ✓ Posted! strategy={strategy} m/{submolt} ID={post_id} verified={verified}")
            state = _record_post(state, submolt, post_id)
            posts_this_run += 1
            if moltbook_engagement_sheet:
                moltbook_engagement_sheet(action="log_post", data={
                    "submolt": submolt, "title": topic[:80], "post_id": post_id,
                    "strategy": strategy, "model": model_used,
                    "word_count": len(draft.split()), "url": post_url,
                })
        else:
            err = post_result.get("data", {}).get("message", str(post_result))
            log.warning(f"  ✗ Post failed m/{submolt}: {err}")
            posts_this_run += 1  # Count failed attempt against budget to avoid infinite retry

        if posts_this_run < MAX_POSTS_PER_RUN:
            time.sleep(3)

    # ── 5. Daily Slack report (first run after midnight UTC) ──────────────────
    last_report_date = state.get("last_slack_report", "")[:10]
    if last_report_date < today:
        log.info("First run after midnight — compiling daily Slack report...")
        if moltbook_engagement_sheet and slack_post:
            report_result = moltbook_engagement_sheet(action="daily_report")
            if report_result.get("status") == "ok":
                summary = report_result["data"]["summary"]
                if not dry_run:
                    slack_result = slack_post(message=summary)
                    if slack_result.get("status") == "ok":
                        log.info("  ✓ Daily Slack report sent")
                        state["last_slack_report"] = now_iso
                        moltbook_engagement_sheet(action="log_daily_report", data={
                            "posts": report_result["data"].get("posts_today", 0),
                            "slack_sent": True,
                        })
                    else:
                        log.warning(f"  ✗ Slack send failed: {slack_result.get('data',{}).get('message')}")
                else:
                    log.info(f"  [DRY RUN] Would Slack: {summary[:80]}...")

    # ── 6. Wrap up ────────────────────────────────────────────────────────────
    state["last_run"] = now_iso
    if not dry_run:
        _save_state(state)

    queue_len = len(state.get("posting_queue", []))
    log.info(
        f"=== Run complete. Posts: {posts_this_run}. "
        f"State: {len(state.get('posts',[]))} posts (24h). Queue: {queue_len} items. ===\n"
    )


# ── Entry point ───────────────────────────────────────────────────────────────

if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="Snowdrop autonomous engagement daemon")
    parser.add_argument("--dry-run", action="store_true", help="Log actions without posting")
    args = parser.parse_args()
    run(dry_run=args.dry_run)
