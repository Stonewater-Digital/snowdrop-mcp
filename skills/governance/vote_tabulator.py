"""Tabulate votes and apply the 1-SD mandate rule."""
from __future__ import annotations

import math
from datetime import datetime, timezone
from typing import Any

TOOL_META: dict[str, Any] = {
    "name": "vote_tabulator",
    "description": "Counts proposal votes and checks for mandates via 1-sigma upvote threshold.",
    "inputSchema": {
        "type": "object",
        "properties": {
            "proposal_id": {"type": "string"},
            "votes": {"type": "array", "items": {"type": "object"}},
            "recent_proposal_stats": {"type": "array", "items": {"type": "object"}},
        },
        "required": ["proposal_id", "votes", "recent_proposal_stats"],
    },
    "outputSchema": {
        "type": "object",
        "properties": {
            "status": {"type": "string"},
            "data": {"type": "object"},
            "timestamp": {"type": "string"},
        },
    },
}


def vote_tabulator(
    proposal_id: str,
    votes: list[dict[str, Any]],
    recent_proposal_stats: list[dict[str, Any]],
    **_: Any,
) -> dict[str, Any]:
    """Return vote counts and mandate flag."""
    try:
        upvotes = sum(1 for vote in votes if vote.get("vote") == "upvote")
        downvotes = sum(1 for vote in votes if vote.get("vote") == "downvote")
        total_votes = upvotes + downvotes
        recent_upvotes = [float(stat.get("upvote_count", 0.0)) for stat in recent_proposal_stats]
        mean_upvotes = sum(recent_upvotes) / len(recent_upvotes) if recent_upvotes else 0.0
        variance = sum((value - mean_upvotes) ** 2 for value in recent_upvotes) / len(recent_upvotes) if recent_upvotes else 0.0
        std_dev = math.sqrt(variance)
        mandated = upvotes > mean_upvotes + std_dev
        data = {
            "proposal_id": proposal_id,
            "upvotes": upvotes,
            "downvotes": downvotes,
            "total_votes": total_votes,
            "mandated": mandated,
            "mean_upvotes": round(mean_upvotes, 2),
            "std_dev": round(std_dev, 2),
        }
        return {
            "status": "success",
            "data": data,
            "timestamp": datetime.now(timezone.utc).isoformat(),
        }
    except Exception as exc:
        _log_lesson("vote_tabulator", str(exc))
        return {
            "status": "error",
            "data": {"error": str(exc)},
            "timestamp": datetime.now(timezone.utc).isoformat(),
        }


def _log_lesson(skill_name: str, error: str) -> None:
    with open("logs/lessons.md", "a", encoding="utf-8") as handle:
        handle.write(f"- [{datetime.now(timezone.utc).isoformat()}] {skill_name}: {error}\n")
