"""Calculate credit card interest for a billing period using daily rate method.

MCP Tool Name: credit_card_interest_calculator
"""
from __future__ import annotations
from datetime import datetime, timezone
from typing import Any

TOOL_META: dict[str, Any] = {
    "name": "credit_card_interest_calculator",
    "description": "Calculate credit card interest accrued over a billing period using the daily periodic rate method: daily_rate = APR/365, interest = balance * daily_rate * days.",
    "inputSchema": {
        "type": "object",
        "properties": {
            "balance": {"type": "number", "description": "Average daily balance."},
            "apr": {"type": "number", "description": "Annual Percentage Rate as decimal."},
            "days_in_period": {"type": "integer", "description": "Number of days in billing period (default 30).", "default": 30},
        },
        "required": ["balance", "apr"],
    },
}


def credit_card_interest_calculator(
    balance: float, apr: float, days_in_period: int = 30
) -> dict[str, Any]:
    """Calculate credit card interest for a billing period."""
    try:
        if balance < 0:
            return {
                "status": "error",
                "data": {"error": "balance must be non-negative."},
                "timestamp": datetime.now(timezone.utc).isoformat(),
            }
        if days_in_period <= 0:
            return {
                "status": "error",
                "data": {"error": "days_in_period must be positive."},
                "timestamp": datetime.now(timezone.utc).isoformat(),
            }

        daily_rate = apr / 365
        interest = balance * daily_rate * days_in_period

        return {
            "status": "ok",
            "data": {
                "balance": balance,
                "apr_pct": round(apr * 100, 4),
                "daily_rate": round(daily_rate, 8),
                "days_in_period": days_in_period,
                "interest_charged": round(interest, 2),
                "annualized_cost": round(interest * (365 / days_in_period), 2),
            },
            "timestamp": datetime.now(timezone.utc).isoformat(),
        }
    except Exception as exc:
        return {
            "status": "error",
            "data": {"error": str(exc)},
            "timestamp": datetime.now(timezone.utc).isoformat(),
        }
