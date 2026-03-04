"""Calculate minimum payment, months to payoff, and total interest.

MCP Tool Name: minimum_payment_calculator
"""
from __future__ import annotations
import math
from datetime import datetime, timezone
from typing import Any

TOOL_META: dict[str, Any] = {
    "name": "minimum_payment_calculator",
    "description": "Calculate credit card minimum payment, estimate months to payoff paying only the minimum, and total interest paid.",
    "inputSchema": {
        "type": "object",
        "properties": {
            "balance": {"type": "number", "description": "Current card balance."},
            "apr": {"type": "number", "description": "Annual Percentage Rate as decimal."},
            "min_pct": {"type": "number", "description": "Minimum payment as fraction of balance (default 0.02).", "default": 0.02},
            "min_floor": {"type": "number", "description": "Minimum dollar floor for payment (default 25.0).", "default": 25.0},
        },
        "required": ["balance", "apr"],
    },
}


def minimum_payment_calculator(
    balance: float, apr: float, min_pct: float = 0.02, min_floor: float = 25.0
) -> dict[str, Any]:
    """Calculate minimum payment and payoff timeline."""
    try:
        if balance <= 0:
            return {
                "status": "ok",
                "data": {"balance": balance, "message": "No balance to pay off."},
                "timestamp": datetime.now(timezone.utc).isoformat(),
            }

        monthly_rate = apr / 12
        remaining = balance
        total_paid = 0.0
        months = 0
        max_months = 1200  # 100 year cap

        while remaining > 0.01 and months < max_months:
            interest = remaining * monthly_rate
            payment = max(remaining * min_pct, min_floor)
            payment = min(payment, remaining + interest)
            remaining = remaining + interest - payment
            total_paid += payment
            months += 1

        total_interest = total_paid - balance
        first_payment = max(balance * min_pct, min_floor)

        return {
            "status": "ok",
            "data": {
                "balance": balance,
                "apr_pct": round(apr * 100, 4),
                "first_minimum_payment": round(first_payment, 2),
                "months_to_payoff": months,
                "years_to_payoff": round(months / 12, 1),
                "total_paid": round(total_paid, 2),
                "total_interest": round(total_interest, 2),
            },
            "timestamp": datetime.now(timezone.utc).isoformat(),
        }
    except Exception as exc:
        return {
            "status": "error",
            "data": {"error": str(exc)},
            "timestamp": datetime.now(timezone.utc).isoformat(),
        }
