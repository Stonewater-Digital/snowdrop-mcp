"""Categorize and prioritize trade breaks."""
from __future__ import annotations

from datetime import datetime, timezone
from typing import Any

PRIORITY_RULES = {
    "cash": 3,
    "position": 2,
    "booking": 1,
}

TOOL_META: dict[str, Any] = {
    "name": "trade_break_resolver",
    "description": "Scores trade breaks by aging and category to prioritize remediation.",
    "inputSchema": {
        "type": "object",
        "properties": {
            "breaks": {
                "type": "array",
                "items": {
                    "type": "object",
                    "properties": {
                        "break_id": {"type": "string"},
                        "category": {"type": "string"},
                        "age_days": {"type": "number"},
                    },
                    "required": ["break_id", "category", "age_days"],
                },
            }
        },
        "required": ["breaks"],
    },
    "outputSchema": {
        "type": "object", "properties": {"status": {"type": "string"}, "data": {"type": "object"}, "timestamp": {"type": "string"}}},
}


def trade_break_resolver(breaks: list[dict[str, Any]], **_: Any) -> dict[str, Any]:
    """Return prioritized break list."""
    try:
        prioritized = []
        for item in breaks:
            category = item.get("category", "position").lower()
            base_score = PRIORITY_RULES.get(category, 1)
            score = base_score * (1 + item.get("age_days", 0) / 5)
            prioritized.append(
                {
                    "break_id": item.get("break_id"),
                    "category": category,
                    "priority_score": round(score, 2),
                }
            )
        prioritized.sort(key=lambda entry: entry["priority_score"], reverse=True)
        data = {"prioritized_breaks": prioritized}
        return {"status": "success", "data": data, "timestamp": datetime.now(timezone.utc).isoformat()}
    except Exception as exc:
        _log_lesson("trade_break_resolver", str(exc))
        return {"status": "error", "data": {"error": str(exc)}, "timestamp": datetime.now(timezone.utc).isoformat()}


def _log_lesson(skill_name: str, error: str) -> None:
    with open("logs/lessons.md", "a", encoding="utf-8") as handle:
        handle.write(f"- [{datetime.now(timezone.utc).isoformat()}] {skill_name}: {error}\n")
