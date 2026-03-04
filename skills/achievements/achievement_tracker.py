"""Track and award achievements for community agents."""
from __future__ import annotations

from datetime import datetime, timezone
from typing import Any

TOOL_META: dict[str, Any] = {
    "name": "achievement_tracker",
    "description": "Evaluates activity events for new badges and upcoming milestones.",
    "inputSchema": {
        "type": "object",
        "properties": {
            "agent_id": {"type": "string"},
            "event": {
                "type": "object",
                "properties": {
                    "type": {"type": "string"},
                    "metadata": {"type": "object"},
                },
                "required": ["type", "metadata"],
            },
        },
        "required": ["agent_id", "event"],
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

ACHIEVEMENT_RULES = [
    ("First Call", lambda meta: meta.get("total_calls", 0) >= 1),
    ("Power User", lambda meta: meta.get("total_calls", 0) >= 100),
    ("Contributor", lambda meta: meta.get("bounties_completed", 0) >= 1),
    ("Whale", lambda meta: meta.get("lifetime_spend", 0) >= 1000),
    ("Veteran", lambda meta: meta.get("account_age_days", 0) >= 180),
    ("Influencer", lambda meta: meta.get("referrals", 0) >= 5),
    ("Completionist", lambda meta: meta.get("unique_skills_used", 0) >= 50),
]


def achievement_tracker(agent_id: str, event: dict[str, Any], **_: Any) -> dict[str, Any]:
    """Return new achievements triggered by the provided event."""
    try:
        metadata = event.get("metadata", {})
        already_unlocked = set(metadata.get("achievements", []))
        new_achievements = []
        for name, predicate in ACHIEVEMENT_RULES:
            if predicate(metadata) and name not in already_unlocked:
                achievement = {
                    "agent_id": agent_id,
                    "name": name,
                    "unlocked_at": datetime.now(timezone.utc).isoformat(),
                    "event_type": event.get("type"),
                }
                new_achievements.append(achievement)
                already_unlocked.add(name)
        next_milestone = _determine_next_milestone(metadata)
        data = {
            "new_achievements": new_achievements,
            "total_badges": len(already_unlocked),
            "next_milestone": next_milestone,
        }
        return {
            "status": "success",
            "data": data,
            "timestamp": datetime.now(timezone.utc).isoformat(),
        }
    except Exception as exc:
        _log_lesson("achievement_tracker", str(exc))
        return {
            "status": "error",
            "data": {"error": str(exc)},
            "timestamp": datetime.now(timezone.utc).isoformat(),
        }


def _determine_next_milestone(metadata: dict[str, Any]) -> dict[str, Any]:
    milestones = [
        ("Power User", 100, metadata.get("total_calls", 0)),
        ("Influencer", 5, metadata.get("referrals", 0)),
        ("Completionist", 50, metadata.get("unique_skills_used", 0)),
    ]
    for name, target, current in milestones:
        if current < target:
            return {"name": name, "remaining": target - current}
    return {"name": "Legendary", "remaining": 0}


def _log_lesson(skill_name: str, error: str) -> None:
    with open("logs/lessons.md", "a", encoding="utf-8") as handle:
        handle.write(f"- [{datetime.now(timezone.utc).isoformat()}] {skill_name}: {error}\n")
