"""
Monitor Moltbook feed across targeted submolts for engagement opportunities.
Surfaces recent posts worth replying to, upvoting, or referencing.
Vigilance skill — Snowdrop checks in periodically and decides where to engage.
"""
import os
import requests
from datetime import datetime, timezone, timedelta

TOOL_META = {
    "name": "moltbook_feed_watch",
    "description": (
        "Scan recent Moltbook posts across specified (or default) submolts and identify "
        "engagement opportunities — posts to comment on, discussions Snowdrop can add value to, "
        "or content that could drive traffic to her repos. Returns ranked engagement targets "
        "with suggested response angles. Run periodically as a vigilance loop."
    ),
}

# Default submolts to monitor — Snowdrop's turf + adjacent communities
DEFAULT_WATCH_LIST = [
    "agents", "agentskills", "agentfinance", "crypto", "buildlogs",
    "tooling", "openclaw-explorers", "showandtell", "introductions",
]

# Topics that are high-value to engage with
SIGNAL_KEYWORDS = [
    "mcp", "model context protocol", "financial", "compliance", "defi", "ton",
    "solana", "agent", "autonomous", "portfolio", "regulatory", "kraken",
    "open source", "skill", "tool", "api", "marketplace", "watering hole",
    "snowdrop",
]


def moltbook_feed_watch(
    submolts: list = None,
    hours_back: int = 24,
    min_score: int = 5,
    limit_per_submolt: int = 10,
) -> dict:
    """
    Scan Moltbook submolts for engagement opportunities.

    Args:
        submolts: List of submolt names to watch (default: Snowdrop's core list)
        hours_back: How many hours back to look (default 24)
        min_score: Minimum relevance score to include in results (default 5)
        limit_per_submolt: Max posts to fetch per submolt (default 10)
    """
    api_key = os.environ.get("MOLTBOOK_API_KEY", "")
    if not api_key:
        return {
            "status": "error",
            "data": {"message": "MOLTBOOK_API_KEY not set"},
            "timestamp": datetime.now(timezone.utc).isoformat(),
        }

    headers = {
        "Authorization": f"Bearer {api_key}",
        "Content-Type": "application/json",
    }

    watch_list = submolts or DEFAULT_WATCH_LIST
    cutoff = datetime.now(timezone.utc) - timedelta(hours=hours_back)
    all_opportunities = []
    errors = []

    for submolt in watch_list:
        try:
            resp = requests.get(
                f"https://www.moltbook.com/api/v1/submolts/{submolt}/posts",
                headers=headers,
                params={"limit": limit_per_submolt, "sort": "new"},
                timeout=15,
            )
            if resp.status_code == 404:
                continue
            data = resp.json()
            posts = data if isinstance(data, list) else data.get("posts", data.get("data", []))

            for post in posts:
                score, reasons, angle = _evaluate_post(post)
                if score < min_score:
                    continue
                all_opportunities.append({
                    "submolt": submolt,
                    "post_id": post.get("id"),
                    "title": post.get("title", "")[:100],
                    "author": post.get("author") or post.get("user", {}).get("username", "unknown"),
                    "score": score,
                    "reasons": reasons,
                    "engagement_angle": angle,
                    "upvotes": post.get("upvotes") or post.get("likes") or 0,
                    "comments": post.get("comment_count") or post.get("comments") or 0,
                    "url": post.get("url") or f"https://www.moltbook.com/submolt/{submolt}/posts/{post.get('id', '')}",
                })

        except Exception as e:
            errors.append(f"{submolt}: {e}")

    all_opportunities.sort(key=lambda x: x["score"], reverse=True)

    return {
        "status": "ok",
        "data": {
            "scanned_submolts": watch_list,
            "opportunities_found": len(all_opportunities),
            "top_targets": all_opportunities[:20],
            "errors": errors,
            "hours_scanned": hours_back,
        },
        "timestamp": datetime.now(timezone.utc).isoformat(),
    }


def _evaluate_post(post: dict) -> tuple[int, list[str], str]:
    title = (post.get("title") or "").lower()
    content = (post.get("content") or post.get("body") or "").lower()
    text = title + " " + content
    score = 0
    reasons = []

    # Keyword relevance
    for kw in SIGNAL_KEYWORDS:
        if kw in text:
            score += 10
            reasons.append(f"keyword:{kw}")

    # Engagement signals
    upvotes = post.get("upvotes") or post.get("likes") or 0
    comments = post.get("comment_count") or post.get("comments") or 0
    if upvotes > 50:
        score += 15
        reasons.append("high_upvotes")
    elif upvotes > 10:
        score += 8
    if comments < 3:
        score += 5
        reasons.append("low_comments:room_to_add_value")
    elif comments > 20:
        score += 3
        reasons.append("active_discussion")

    # Determine engagement angle
    angle = "general comment with MCP mention"
    if "mcp" in text or "model context protocol" in text:
        angle = "direct MCP expertise comment — offer skill or answer question"
    elif any(k in text for k in ["financial", "compliance", "regulatory"]):
        angle = "financial expertise comment — position as authority, mention skills"
    elif any(k in text for k in ["agent", "autonomous", "ai"]):
        angle = "agent-to-agent connection — pitch Watering Hole job or star trade"
    elif any(k in text for k in ["crypto", "defi", "ton", "solana"]):
        angle = "crypto/DeFi angle — mention Watering Hole marketplace"
    elif any(k in text for k in ["build", "show", "ship", "launch"]):
        angle = "builder solidarity — offer star trade, link MCP server as resource"

    return score, reasons, angle
