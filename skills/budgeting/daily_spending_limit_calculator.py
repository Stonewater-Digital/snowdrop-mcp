"""Calculate daily and weekly spending limits from a monthly budget.

MCP Tool Name: daily_spending_limit_calculator
"""
from __future__ import annotations
from datetime import datetime, timezone
from typing import Any

TOOL_META: dict[str, Any] = {
    "name": "daily_spending_limit_calculator",
    "description": "Converts a monthly budget into daily and weekly spending limits.",
    "inputSchema": {
        "type": "object",
        "properties": {
            "monthly_budget": {
                "type": "number",
                "description": "Total monthly discretionary budget in dollars.",
            },
            "days_in_month": {
                "type": "integer",
                "description": "Number of days in the current month (default: 30).",
            },
        },
        "required": ["monthly_budget"],
    },
}


def daily_spending_limit_calculator(
    monthly_budget: float, days_in_month: int = 30
) -> dict[str, Any]:
    """Converts monthly budget into daily and weekly spending limits."""
    try:
        if monthly_budget <= 0:
            return {
                "status": "error",
                "data": {"error": "Monthly budget must be a positive number."},
                "timestamp": datetime.now(timezone.utc).isoformat(),
            }
        if days_in_month <= 0:
            return {
                "status": "error",
                "data": {"error": "Days in month must be a positive number."},
                "timestamp": datetime.now(timezone.utc).isoformat(),
            }

        daily = round(monthly_budget / days_in_month, 2)
        weekly = round(daily * 7, 2)
        biweekly = round(daily * 14, 2)
        weeks_in_month = round(days_in_month / 7, 2)

        return {
            "status": "ok",
            "data": {
                "monthly_budget": monthly_budget,
                "days_in_month": days_in_month,
                "daily_limit": daily,
                "weekly_limit": weekly,
                "biweekly_limit": biweekly,
                "weeks_in_month": weeks_in_month,
                "tip": "Track daily spending against this limit. If you underspend one day, the surplus rolls to the next. Review weekly to stay on track.",
            },
            "timestamp": datetime.now(timezone.utc).isoformat(),
        }
    except Exception as exc:
        return {
            "status": "error",
            "data": {"error": str(exc)},
            "timestamp": datetime.now(timezone.utc).isoformat(),
        }
