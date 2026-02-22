"""
Discover and score Moltbook submolts for engagement fit.
Returns a ranked list of submolts that match Snowdrop's content areas,
prioritized by member count, activity, and topic alignment.
"""
import os
import re
import requests
from datetime import datetime, timezone

TOOL_META = {
    "name": "moltbook_submolt_discover",
    "description": (
        "Fetch all Moltbook submolts and score them for engagement fit with Snowdrop's "
        "content areas: finance, agents, crypto, MCP/tooling, compliance, community/social. "
        "Returns ranked list with member counts and posting recommendations. "
        "Use this to find where to post next and which communities to cultivate."
    ),
}

# Keywords that signal topic alignment — scored by tier
TIER_1 = ["finance", "financial", "crypto", "defi", "agent", "mcp", "ai", "trading", "compliance"]
TIER_2 = ["tech", "build", "tool", "dev", "code", "market", "invest", "blockchain", "solana", "ton"]
TIER_3 = ["general", "show", "intro", "showcase", "startup", "entrepreneur", "open", "community"]

# Snowdrop's posted submolts — avoid reposting unless needed
ALREADY_POSTED = {"general", "introductions", "agentskills", "openclaw-explorers",
                  "showandtell", "agents", "crypto", "buildlogs", "agentfinance", "tooling"}


def _score(submolt: dict) -> tuple[int, list[str]]:
    name = (submolt.get("name") or "").lower()
    desc = (submolt.get("description") or "").lower()
    text = name + " " + desc
    reasons = []
    score = 0

    members = submolt.get("member_count") or submolt.get("members") or 0
    if members > 10000:
        score += 30
    elif members > 1000:
        score += 20
    elif members > 100:
        score += 10
    elif members > 10:
        score += 5

    for kw in TIER_1:
        if kw in text:
            score += 15
            reasons.append(f"topic:{kw}")
    for kw in TIER_2:
        if kw in text:
            score += 8
            reasons.append(f"topic:{kw}")
    for kw in TIER_3:
        if kw in text:
            score += 3

    if name in ALREADY_POSTED:
        score -= 20
        reasons.append("already_posted")

    return score, reasons


def moltbook_submolt_discover(
    min_members: int = 0,
    filter_posted: bool = True,
    top_n: int = 20,
) -> dict:
    """
    Discover and rank Moltbook submolts for Snowdrop's engagement strategy.

    Args:
        min_members: Minimum member count to include (default 0 = include all)
        filter_posted: Exclude submolts already posted to (default True)
        top_n: Return top N results (default 20)
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

    try:
        resp = requests.get(
            "https://www.moltbook.com/api/v1/submolts",
            headers=headers,
            timeout=15,
        )
        resp.raise_for_status()
        data = resp.json()

        submolts = data if isinstance(data, list) else data.get("submolts", data.get("data", []))

        scored = []
        for s in submolts:
            name = s.get("name") or s.get("slug") or ""
            members = s.get("member_count") or s.get("members") or 0

            if members < min_members:
                continue
            if filter_posted and name in ALREADY_POSTED:
                continue

            score, reasons = _score(s)
            scored.append({
                "name": name,
                "description": s.get("description", "")[:120],
                "members": members,
                "score": score,
                "reasons": reasons,
                "recommended_content": _suggest_content(name, s.get("description", "")),
            })

        scored.sort(key=lambda x: x["score"], reverse=True)
        top = scored[:top_n]

        return {
            "status": "ok",
            "data": {
                "total_submolts": len(submolts),
                "filtered_count": len(scored),
                "top_matches": top,
                "already_posted_to": sorted(ALREADY_POSTED),
            },
            "timestamp": datetime.now(timezone.utc).isoformat(),
        }

    except Exception as e:
        return {
            "status": "error",
            "data": {"message": str(e)},
            "timestamp": datetime.now(timezone.utc).isoformat(),
        }


def _suggest_content(name: str, desc: str) -> str:
    text = (name + " " + desc).lower()
    if any(k in text for k in ["finance", "invest", "trading", "market"]):
        return "Financial analysis post or The Watering Hole pitch"
    if any(k in text for k in ["agent", "ai", "mcp", "tool"]):
        return "MCP server feature post or skill request invitation"
    if any(k in text for k in ["crypto", "defi", "blockchain", "ton", "solana"]):
        return "Watering Hole TON marketplace pitch"
    if any(k in text for k in ["build", "dev", "code", "show"]):
        return "Build log or open-source showcase post"
    if any(k in text for k in ["intro", "general", "community"]):
        return "Introduction post with GitHub star ask"
    return "General interest post with MCP server mention"
