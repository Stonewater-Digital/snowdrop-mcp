"""Generate a weekly profit and loss summary across Snowdrop operations."""
from __future__ import annotations

from datetime import datetime, timezone
from typing import Any

TOOL_META: dict[str, Any] = {
    "name": "weekly_pnl_report",
    "description": "Aggregates revenue and expense items into a weekly P&L rollup.",
    "inputSchema": {
        "type": "object",
        "properties": {
            "revenue_items": {
                "type": "array",
                "items": {"type": "object"},
                "description": "Revenue entries with amount/category/notes.",
            },
            "expense_items": {
                "type": "array",
                "items": {"type": "object"},
                "description": "Expense entries (compute, API, infra, other).",
            },
            "period_start": {"type": "string", "description": "Period start date (ISO)."},
            "period_end": {"type": "string", "description": "Period end date (ISO)."},
        },
        "required": ["revenue_items", "expense_items", "period_start", "period_end"],
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


def weekly_pnl_report(
    revenue_items: list[dict[str, Any]],
    expense_items: list[dict[str, Any]],
    period_start: str,
    period_end: str,
    **_: Any,
) -> dict[str, Any]:
    """Compile a weekly P&L statement.

    Args:
        revenue_items: Revenue entries with amount/category metadata.
        expense_items: Expense entries split across compute/API/infra buckets.
        period_start: ISO8601 date representing the start of the week.
        period_end: ISO8601 date representing the end of the week.

    Returns:
        Envelope containing totals, breakdowns, and calculated margin percentage.
    """

    try:
        gross_revenue = sum(float(item.get("amount", 0) or 0) for item in revenue_items)
        expense_breakdown = {"compute": 0.0, "api": 0.0, "infra": 0.0, "other": 0.0}

        for expense in expense_items:
            amount = float(expense.get("amount", 0) or 0)
            category = (expense.get("category") or "other").lower()
            if category not in expense_breakdown:
                category = "other"
            expense_breakdown[category] += amount

        total_expenses = round(sum(expense_breakdown.values()), 4)
        net_pnl = round(gross_revenue - total_expenses, 4)
        margin_pct = round((net_pnl / gross_revenue * 100) if gross_revenue else 0.0, 4)

        data = {
            "period": {"start": period_start, "end": period_end},
            "gross_revenue": round(gross_revenue, 4),
            "expense_breakdown": {k: round(v, 4) for k, v in expense_breakdown.items()},
            "total_expenses": total_expenses,
            "net_pnl": net_pnl,
            "margin_pct": margin_pct,
        }

        return {
            "status": "success",
            "data": data,
            "timestamp": datetime.now(timezone.utc).isoformat(),
        }
    except Exception as exc:
        _log_lesson("weekly_pnl_report", str(exc))
        return {
            "status": "error",
            "data": {"error": str(exc)},
            "timestamp": datetime.now(timezone.utc).isoformat(),
        }


def _log_lesson(skill_name: str, error: str) -> None:
    with open("logs/lessons.md", "a", encoding="utf-8") as handle:
        handle.write(f"- [{datetime.now(timezone.utc).isoformat()}] {skill_name}: {error}\n")
