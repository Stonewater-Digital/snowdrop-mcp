"""Compute operating expense ratio for REITs."""
from __future__ import annotations

from datetime import datetime, timezone
from typing import Any

TOOL_META: dict[str, Any] = {
    "name": "operating_expense_ratio",
    "description": "Calculates operating expense ratio and efficiency gap versus target.",
    "inputSchema": {
        "type": "object",
        "properties": {
            "operating_expenses": {"type": "number"},
            "gross_revenue": {"type": "number"},
            "target_ratio_pct": {"type": "number", "default": 35.0},
        },
        "required": ["operating_expenses", "gross_revenue"],
    },
    "outputSchema": {"type": "object", "properties": {"status": {"type": "string"}, "data": {"type": "object"}, "timestamp": {"type": "string"}}},
}


def operating_expense_ratio(
    operating_expenses: float,
    gross_revenue: float,
    target_ratio_pct: float = 35.0,
    **_: Any,
) -> dict[str, Any]:
    """Return operating expense ratio and headroom."""
    try:
        ratio = operating_expenses / gross_revenue * 100 if gross_revenue else 0.0
        gap = target_ratio_pct - ratio
        data = {
            "operating_expense_ratio_pct": round(ratio, 2),
            "efficiency_headroom_pct": round(gap, 2),
            "warning": ratio > target_ratio_pct,
        }
        return {"status": "success", "data": data, "timestamp": datetime.now(timezone.utc).isoformat()}
    except Exception as exc:
        _log_lesson("operating_expense_ratio", str(exc))
        return {"status": "error", "data": {"error": str(exc)}, "timestamp": datetime.now(timezone.utc).isoformat()}


def _log_lesson(skill_name: str, error: str) -> None:
    with open("logs/lessons.md", "a", encoding="utf-8") as handle:
        handle.write(f"- [{datetime.now(timezone.utc).isoformat()}] {skill_name}: {error}\n")
