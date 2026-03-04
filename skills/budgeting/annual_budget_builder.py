"""Construct annual budgets from revenue and expense assumptions."""
from __future__ import annotations

from datetime import datetime, timezone
from typing import Any

TOOL_META: dict[str, Any] = {
    "name": "annual_budget_builder",
    "description": "Projects monthly revenue/expense totals with growth assumptions for 12 months.",
    "inputSchema": {
        "type": "object",
        "properties": {
            "revenue_assumptions": {
                "type": "array",
                "items": {"type": "object"},
            },
            "expense_categories": {
                "type": "array",
                "items": {"type": "object"},
            },
            "fiscal_year_start": {
                "type": "string",
                "description": "ISO date of fiscal year start.",
            },
        },
        "required": ["revenue_assumptions", "expense_categories", "fiscal_year_start"],
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


def annual_budget_builder(
    revenue_assumptions: list[dict[str, Any]],
    expense_categories: list[dict[str, Any]],
    fiscal_year_start: str,
    **_: Any,
) -> dict[str, Any]:
    """Project an annual budget from revenue and expense assumptions."""
    try:
        try:
            fy_start = datetime.fromisoformat(fiscal_year_start).date()
        except ValueError as exc:  # noqa: B904
            raise ValueError("fiscal_year_start must be ISO date") from exc

        monthly_budget: list[dict[str, Any]] = []
        annual_revenue = 0.0
        annual_expenses = 0.0
        break_even_month: int | None = None

        revenue_state = [
            {
                "source": item.get("source", "unknown"),
                "amount": float(item.get("monthly_amount", 0.0)),
                "growth": float(item.get("growth_rate_pct", 0.0)) / 100,
            }
            for item in revenue_assumptions
        ]
        expense_state = [
            {
                "category": item.get("category", "misc"),
                "amount": float(item.get("monthly_amount", 0.0)),
                "growth": float(item.get("growth_rate_pct", 0.0)) / 100,
                "fixed": bool(item.get("fixed", False)),
            }
            for item in expense_categories
        ]

        for month_idx in range(12):
            month_label = (fy_start.replace(day=1) + _month_delta(month_idx)).strftime("%Y-%m")
            month_revenue = sum(item["amount"] for item in revenue_state)
            month_expense = sum(item["amount"] for item in expense_state)
            net = month_revenue - month_expense
            if break_even_month is None and net >= 0:
                break_even_month = month_idx + 1

            monthly_budget.append(
                {
                    "month": month_label,
                    "revenue": round(month_revenue, 2),
                    "expenses": round(month_expense, 2),
                    "net": round(net, 2),
                }
            )
            annual_revenue += month_revenue
            annual_expenses += month_expense

            for item in revenue_state:
                item["amount"] *= 1 + item["growth"]
            for item in expense_state:
                if not item["fixed"]:
                    item["amount"] *= 1 + item["growth"]

        data = {
            "monthly_budget": monthly_budget,
            "annual_revenue": round(annual_revenue, 2),
            "annual_expenses": round(annual_expenses, 2),
            "annual_net": round(annual_revenue - annual_expenses, 2),
            "break_even_month": break_even_month,
        }
        return {
            "status": "success",
            "data": data,
            "timestamp": datetime.now(timezone.utc).isoformat(),
        }
    except Exception as exc:  # noqa: BLE001
        _log_lesson("annual_budget_builder", str(exc))
        return {
            "status": "error",
            "data": {"error": str(exc)},
            "timestamp": datetime.now(timezone.utc).isoformat(),
        }


def _month_delta(offset: int):
    from datetime import timedelta

    # approximate month delta by 30-day increments; precise shifts handled via replace in caller
    return timedelta(days=30 * offset)


def _log_lesson(skill_name: str, error: str) -> None:
    with open("logs/lessons.md", "a", encoding="utf-8") as handle:
        handle.write(f"- [{datetime.now(timezone.utc).isoformat()}] {skill_name}: {error}\n")
