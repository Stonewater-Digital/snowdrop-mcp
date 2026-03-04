"""Compute experience points for agent activities."""
from __future__ import annotations

from datetime import datetime, timezone
from typing import Any

XP_TABLE = {
    "skill_call": 1,
    "payment_made": 5,
    "bounty_completed": 50,
    "review_posted": 10,
    "referral_converted": 25,
    "bug_reported": 15,
}

RANK_TITLES = [
    (1, 5, "Newcomer"),
    (6, 15, "Regular"),
    (16, 30, "Veteran"),
    (31, 50, "Elite"),
    (51, 10_000, "Legend"),
]

TOOL_META: dict[str, Any] = {
    "name": "xp_calculator",
    "description": "Tallies XP from recent activities and estimates level progression.",
    "inputSchema": {
        "type": "object",
        "properties": {
            "activities": {"type": "array", "items": {"type": "object"}},
        },
        "required": ["activities"],
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


def xp_calculator(activities: list[dict[str, Any]], **_: Any) -> dict[str, Any]:
    """Aggregate XP, level, and rank from activities."""
    try:
        xp_breakdown: dict[str, int] = {key: 0 for key in XP_TABLE}
        total_xp = 0
        for activity in activities:
            xp = XP_TABLE.get(activity.get("type"), 0)
            xp_breakdown[activity.get("type", "unknown")] = xp_breakdown.get(
                activity.get("type", "unknown"),
                0,
            ) + xp
            total_xp += xp
        level = total_xp // 100 + 1
        progress = (total_xp % 100) / 100 * 100
        rank_title = _rank_for_level(level)
        data = {
            "total_xp": total_xp,
            "level": level,
            "rank_title": rank_title,
            "progress_pct": round(progress, 2),
            "xp_breakdown": xp_breakdown,
        }
        return {
            "status": "success",
            "data": data,
            "timestamp": datetime.now(timezone.utc).isoformat(),
        }
    except Exception as exc:
        _log_lesson("xp_calculator", str(exc))
        return {
            "status": "error",
            "data": {"error": str(exc)},
            "timestamp": datetime.now(timezone.utc).isoformat(),
        }


def _rank_for_level(level: int) -> str:
    for start, end, title in RANK_TITLES:
        if start <= level <= end:
            return title
    return "Legend"


def _log_lesson(skill_name: str, error: str) -> None:
    with open("logs/lessons.md", "a", encoding="utf-8") as handle:
        handle.write(f"- [{datetime.now(timezone.utc).isoformat()}] {skill_name}: {error}\n")
