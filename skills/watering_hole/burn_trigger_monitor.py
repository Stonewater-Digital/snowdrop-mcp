"""Monitor Watering Hole burn vs. revenue + labor spread."""
from __future__ import annotations

from datetime import datetime, timezone
from typing import Any, Iterable

THRESHOLD_MULTIPLIER = 1.2
REQUIRED_STREAK = 3

TOOL_META: dict[str, Any] = {
    "name": "burn_trigger_monitor",
    "description": "Flags Watering Hole burn when expenses beat revenue+labor by 20% for 3 weeks.",
    "inputSchema": {
        "type": "object",
        "properties": {
            "weekly_financials": {
                "type": "array",
                "items": {
                    "type": "object",
                    "properties": {
                        "week": {"type": "string"},
                        "revenue": {"type": "number"},
                        "labor": {"type": "number"},
                        "expenses": {"type": "number"},
                    },
                },
                "description": "Chronological weekly ledger entries (newest last).",
            }
        },
        "required": ["weekly_financials"],
    },
    "outputSchema": {
        "type": "object",
        "properties": {
            "status": {"type": "string"},
            "data": {
                "type": "object",
                "properties": {
                    "triggered": {"type": "boolean"},
                    "streak": {"type": "number"},
                    "violations": {"type": "array"},
                },
            },
            "timestamp": {"type": "string"},
        },
    },
}


def burn_trigger_monitor(weekly_financials: Iterable[dict[str, Any]], **_: Any) -> dict[str, Any]:
    """Evaluate the burn kill switch rule."""
    try:
        violations: list[dict[str, Any]] = []
        streak = 0
        for entry in weekly_financials:
            week = entry.get("week") or "unknown"
            revenue = float(entry.get("revenue", 0.0))
            labor = float(entry.get("labor", 0.0))
            expenses = float(entry.get("expenses", 0.0))
            if min(revenue, labor, expenses) < 0:
                raise ValueError("Revenue, labor, and expenses must be non-negative")
            allowable = (revenue + labor) * THRESHOLD_MULTIPLIER
            overage = expenses - allowable
            if overage > 0:
                streak += 1
                violations.append({
                    "week": week,
                    "revenue": round(revenue, 2),
                    "labor": round(labor, 2),
                    "expenses": round(expenses, 2),
                    "threshold": round(allowable, 2),
                    "overage": round(overage, 2),
                })
            else:
                streak = 0

        triggered = streak >= REQUIRED_STREAK
        data = {
            "triggered": triggered,
            "streak": streak,
            "violations": violations[-REQUIRED_STREAK:],
        }
        return {
            "status": "success",
            "data": data,
            "timestamp": datetime.now(timezone.utc).isoformat(),
        }
    except Exception as exc:
        _log_lesson("burn_trigger_monitor", str(exc))
        return {
            "status": "error",
            "data": {"error": str(exc)},
            "timestamp": datetime.now(timezone.utc).isoformat(),
        }


def _log_lesson(skill_name: str, error: str) -> None:
    with open("logs/lessons.md", "a", encoding="utf-8") as handle:
        handle.write(f"- [{datetime.now(timezone.utc).isoformat()}] {skill_name}: {error}\n")
