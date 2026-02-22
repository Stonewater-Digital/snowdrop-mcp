"""Detect market fit issues based on paid transaction droughts."""
from __future__ import annotations

from datetime import datetime, timezone
from typing import Any, Iterable

THRESHOLD_DAYS = 14

TOOL_META: dict[str, Any] = {
    "name": "ghost_town_detector",
    "description": "Raises an alert when 14 days pass without paid transactions.",
    "inputSchema": {
        "type": "object",
        "properties": {
            "daily_transactions": {
                "type": "array",
                "items": {
                    "type": "object",
                    "properties": {
                        "date": {"type": "string"},
                        "paid_count": {"type": "number"},
                    },
                },
                "description": "Chronological (oldest first) paid transaction counts.",
            }
        },
        "required": ["daily_transactions"],
    },
    "outputSchema": {
        "type": "object",
        "properties": {
            "status": {"type": "string"},
            "data": {
                "type": "object",
                "properties": {
                    "days_since_paid": {"type": "number"},
                    "alert": {"type": "boolean"},
                    "last_paid_date": {"type": "string"},
                },
            },
            "timestamp": {"type": "string"},
        },
    },
}


def ghost_town_detector(daily_transactions: Iterable[dict[str, Any]], **_: Any) -> dict[str, Any]:
    """Check for paid transaction droughts."""
    try:
        latest_paid_date: str | None = None
        days_since_paid = 0
        for entry in daily_transactions:
            date_str = entry.get("date")
            paid = int(entry.get("paid_count", 0))
            if paid < 0:
                raise ValueError("paid_count cannot be negative")
            if paid > 0:
                latest_paid_date = date_str
                days_since_paid = 0
            else:
                days_since_paid += 1

        alert = days_since_paid >= THRESHOLD_DAYS
        data = {
            "days_since_paid": days_since_paid,
            "alert": alert,
            "last_paid_date": latest_paid_date,
        }
        return {
            "status": "success",
            "data": data,
            "timestamp": datetime.now(timezone.utc).isoformat(),
        }
    except Exception as exc:
        _log_lesson("ghost_town_detector", str(exc))
        return {
            "status": "error",
            "data": {"error": str(exc)},
            "timestamp": datetime.now(timezone.utc).isoformat(),
        }


def _log_lesson(skill_name: str, error: str) -> None:
    with open("logs/lessons.md", "a", encoding="utf-8") as handle:
        handle.write(f"- [{datetime.now(timezone.utc).isoformat()}] {skill_name}: {error}\n")
