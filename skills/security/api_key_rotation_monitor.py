"""Monitor API key ages and flag rotation needs."""
from __future__ import annotations

from datetime import datetime, timezone
from typing import Any

TOOL_META: dict[str, Any] = {
    "name": "api_key_rotation_monitor",
    "description": "Scores API keys by age and alerts when max_age_days is breached.",
    "inputSchema": {
        "type": "object",
        "properties": {
            "key_inventory": {
                "type": "array",
                "items": {"type": "object"},
            }
        },
        "required": ["key_inventory"],
    },
    "outputSchema": {
        "type": "object",
        "properties": {
            "status": {"type": "string"},
            "data": {
                "type": "object",
                "properties": {
                    "needs_rotation": {"type": "array", "items": {"type": "object"}},
                },
            },
            "timestamp": {"type": "string"},
        },
    },
}


def api_key_rotation_monitor(key_inventory: list[dict[str, Any]], **_: Any) -> dict[str, Any]:
    """Return keys exceeding their allowed lifetime."""

    try:
        today = datetime.now(timezone.utc).date()
        flagged: list[dict[str, Any]] = []
        for key in key_inventory:
            created = key.get("created_date")
            max_age = int(key.get("max_age_days", 0))
            if not created or max_age <= 0:
                raise ValueError("Each key requires created_date and positive max_age_days")
            created_date = datetime.fromisoformat(str(created)).date()
            age_days = (today - created_date).days
            overdue = age_days - max_age
            if overdue <= 0:
                continue
            flagged.append(
                {
                    "key_name": key.get("key_name"),
                    "age_days": age_days,
                    "days_overdue": overdue,
                    "priority": _priority(overdue),
                }
            )

        return {
            "status": "success",
            "data": {"needs_rotation": flagged},
            "timestamp": datetime.now(timezone.utc).isoformat(),
        }
    except Exception as exc:
        _log_lesson("api_key_rotation_monitor", str(exc))
        return {
            "status": "error",
            "data": {"error": str(exc)},
            "timestamp": datetime.now(timezone.utc).isoformat(),
        }


def _priority(overdue: int) -> str:
    if overdue > 30:
        return "emergency"
    if overdue > 7:
        return "high"
    return "standard"


def _log_lesson(skill_name: str, error: str) -> None:
    """Append a Ralph Wiggum lesson entry."""

    with open("logs/lessons.md", "a", encoding="utf-8") as handle:
        handle.write(f"- [{datetime.now(timezone.utc).isoformat()}] {skill_name}: {error}\n")
