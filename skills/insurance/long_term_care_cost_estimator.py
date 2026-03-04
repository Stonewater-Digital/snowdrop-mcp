"""Estimate future long-term care costs with inflation adjustment.

MCP Tool Name: long_term_care_cost_estimator
"""
from __future__ import annotations
from datetime import datetime, timezone
from typing import Any

TOOL_META: dict[str, Any] = {
    "name": "long_term_care_cost_estimator",
    "description": "Estimate future long-term care costs adjusted for inflation. Calculates daily and total costs at the time care is needed.",
    "inputSchema": {
        "type": "object",
        "properties": {
            "daily_rate": {"type": "number", "description": "Current average daily LTC rate (default 300).", "default": 300},
            "years_of_care": {"type": "number", "description": "Expected years of care needed (default 3).", "default": 3},
            "inflation_rate": {"type": "number", "description": "Annual LTC cost inflation rate as decimal (default 0.03).", "default": 0.03},
            "years_until_need": {"type": "integer", "description": "Years from now until care is needed (default 20).", "default": 20},
        },
        "required": [],
    },
}


def long_term_care_cost_estimator(
    daily_rate: float = 300,
    years_of_care: float = 3,
    inflation_rate: float = 0.03,
    years_until_need: int = 20,
) -> dict[str, Any]:
    """Estimate future long-term care costs."""
    try:
        future_daily = daily_rate * (1 + inflation_rate) ** years_until_need
        annual_cost = future_daily * 365
        total_cost = annual_cost * years_of_care
        monthly_cost = annual_cost / 12

        return {
            "status": "ok",
            "data": {
                "current_daily_rate": daily_rate,
                "inflation_rate_pct": round(inflation_rate * 100, 2),
                "years_until_need": years_until_need,
                "years_of_care": years_of_care,
                "future_daily_rate": round(future_daily, 2),
                "future_monthly_cost": round(monthly_cost, 2),
                "future_annual_cost": round(annual_cost, 2),
                "total_estimated_cost": round(total_cost, 2),
            },
            "timestamp": datetime.now(timezone.utc).isoformat(),
        }
    except Exception as exc:
        return {
            "status": "error",
            "data": {"error": str(exc)},
            "timestamp": datetime.now(timezone.utc).isoformat(),
        }
