"""Summarize expenses by cost center and compare to budget."""
from __future__ import annotations

from datetime import datetime, timezone
from typing import Any

TOOL_META: dict[str, Any] = {
    "name": "cost_center_reporter",
    "description": "Aggregates expenses by center with mix and budget deltas.",
    "inputSchema": {
        "type": "object",
        "properties": {
            "expenses": {"type": "array", "items": {"type": "object"}},
            "period": {"type": "string"},
            "budget": {"type": ["object", "null"], "default": None},
        },
        "required": ["expenses", "period"],
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


def cost_center_reporter(
    expenses: list[dict[str, Any]],
    period: str,
    budget: dict[str, float] | None = None,
    **_: Any,
) -> dict[str, Any]:
    """Aggregate costs by center and show variances."""
    try:
        if not expenses:
            raise ValueError("expenses cannot be empty")
        totals: dict[str, float] = {}
        for expense in expenses:
            center = expense.get("cost_center", "unassigned")
            amount = float(expense.get("amount", 0))
            totals[center] = totals.get(center, 0.0) + amount
        total_spend = sum(totals.values())
        pct_breakdown = (
            {center: round(amount / total_spend * 100, 2) for center, amount in totals.items()}
            if total_spend
            else {}
        )
        dominant_center = max(totals, key=totals.get)
        vs_budget = None
        if budget:
            vs_budget = {
                center: round(amount - budget.get(center, 0), 2)
                for center, amount in totals.items()
            }
        data = {
            "by_center": {k: round(v, 2) for k, v in totals.items()},
            "total": round(total_spend, 2),
            "dominant_cost_center": dominant_center,
            "pct_breakdown": pct_breakdown,
            "vs_budget": vs_budget,
        }
        return {
            "status": "success",
            "data": data,
            "timestamp": datetime.now(timezone.utc).isoformat(),
        }
    except Exception as exc:
        _log_lesson("cost_center_reporter", str(exc))
        return {
            "status": "error",
            "data": {"error": str(exc)},
            "timestamp": datetime.now(timezone.utc).isoformat(),
        }


def _log_lesson(skill_name: str, error: str) -> None:
    with open("logs/lessons.md", "a", encoding="utf-8") as handle:
        handle.write(f"- [{datetime.now(timezone.utc).isoformat()}] {skill_name}: {error}\n")
