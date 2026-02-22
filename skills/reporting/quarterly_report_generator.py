"""Quarterly reporting pack builder."""
from __future__ import annotations

from datetime import datetime, timezone
from typing import Any

TOOL_META: dict[str, Any] = {
    "name": "quarterly_report_generator",
    "description": "Summarizes fund performance against benchmarks for the quarter.",
    "inputSchema": {
        "type": "object",
        "properties": {
            "quarter": {"type": "string"},
            "revenue_by_source": {"type": "object"},
            "expenses_by_category": {"type": "object"},
            "portfolio_values": {"type": "object"},
            "benchmark_return": {"type": "number"},
        },
        "required": [
            "quarter",
            "revenue_by_source",
            "expenses_by_category",
            "portfolio_values",
            "benchmark_return",
        ],
    },
    "outputSchema": {
        "type": "object",
        "properties": {
            "status": {"type": "string"},
            "data": {
                "type": "object",
                "properties": {
                    "report": {"type": "object"},
                },
            },
            "timestamp": {"type": "string"},
        },
    },
}


def quarterly_report_generator(
    quarter: str,
    revenue_by_source: dict[str, float],
    expenses_by_category: dict[str, float],
    portfolio_values: dict[str, float],
    benchmark_return: float,
    **_: Any,
) -> dict[str, Any]:
    """Generate a structured quarterly report."""

    try:
        total_revenue = sum(float(v) for v in revenue_by_source.values())
        total_expenses = sum(float(v) for v in expenses_by_category.values())
        nav_start = float(portfolio_values.get("start", 0))
        nav_end = float(portfolio_values.get("end", 0))
        if nav_start <= 0 or nav_end <= 0:
            raise ValueError("portfolio_values must include positive start and end")

        net_return = (nav_end - nav_start - total_expenses + total_revenue) / nav_start
        alpha = net_return - benchmark_return
        avg_assets = (nav_start + nav_end) / 2
        expense_ratio = total_expenses / avg_assets

        report = {
            "quarter": quarter,
            "totals": {
                "revenue": round(total_revenue, 2),
                "expenses": round(total_expenses, 2),
                "net_income": round(total_revenue - total_expenses, 2),
            },
            "performance": {
                "net_return_pct": round(net_return * 100, 3),
                "benchmark_return_pct": round(benchmark_return * 100, 3),
                "alpha_pct": round(alpha * 100, 3),
                "expense_ratio_pct": round(expense_ratio * 100, 3),
            },
            "breakdowns": {
                "revenue_by_source": revenue_by_source,
                "expenses_by_category": expenses_by_category,
            },
        }
        return {
            "status": "success",
            "data": {"report": report},
            "timestamp": datetime.now(timezone.utc).isoformat(),
        }
    except Exception as exc:
        _log_lesson("quarterly_report_generator", str(exc))
        return {
            "status": "error",
            "data": {"error": str(exc)},
            "timestamp": datetime.now(timezone.utc).isoformat(),
        }


def _log_lesson(skill_name: str, error: str) -> None:
    """Append a Ralph Wiggum lesson entry."""

    with open("logs/lessons.md", "a", encoding="utf-8") as handle:
        handle.write(f"- [{datetime.now(timezone.utc).isoformat()}] {skill_name}: {error}\n")
