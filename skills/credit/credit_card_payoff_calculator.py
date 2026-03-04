"""Calculate months to pay off a credit card balance with fixed payments.

MCP Tool Name: credit_card_payoff_calculator
"""
from __future__ import annotations
import math
from datetime import datetime, timezone
from typing import Any

TOOL_META: dict[str, Any] = {
    "name": "credit_card_payoff_calculator",
    "description": "Calculate how many months to pay off a credit card balance with a fixed monthly payment, and total interest paid.",
    "inputSchema": {
        "type": "object",
        "properties": {
            "balance": {"type": "number", "description": "Current card balance."},
            "apr": {"type": "number", "description": "Annual Percentage Rate as decimal."},
            "monthly_payment": {"type": "number", "description": "Fixed monthly payment amount."},
        },
        "required": ["balance", "apr", "monthly_payment"],
    },
}


def credit_card_payoff_calculator(
    balance: float, apr: float, monthly_payment: float
) -> dict[str, Any]:
    """Calculate payoff timeline for a credit card."""
    try:
        if balance <= 0:
            return {
                "status": "ok",
                "data": {"message": "No balance to pay off."},
                "timestamp": datetime.now(timezone.utc).isoformat(),
            }
        if monthly_payment <= 0:
            return {
                "status": "error",
                "data": {"error": "monthly_payment must be positive."},
                "timestamp": datetime.now(timezone.utc).isoformat(),
            }

        r = apr / 12

        if r == 0:
            months = math.ceil(balance / monthly_payment)
            total_interest = 0.0
        else:
            # Check if payment covers at least interest
            min_interest = balance * r
            if monthly_payment <= min_interest:
                return {
                    "status": "error",
                    "data": {
                        "error": f"Payment ${monthly_payment:.2f} does not cover monthly interest ${min_interest:.2f}. Balance will never be paid off."
                    },
                    "timestamp": datetime.now(timezone.utc).isoformat(),
                }
            months = math.ceil(
                -math.log(1 - balance * r / monthly_payment) / math.log(1 + r)
            )
            total_paid = monthly_payment * months
            total_interest = total_paid - balance

        return {
            "status": "ok",
            "data": {
                "balance": balance,
                "apr_pct": round(apr * 100, 4),
                "monthly_payment": monthly_payment,
                "months_to_payoff": months,
                "years_to_payoff": round(months / 12, 1),
                "total_interest": round(total_interest, 2),
                "total_paid": round(balance + total_interest, 2),
            },
            "timestamp": datetime.now(timezone.utc).isoformat(),
        }
    except Exception as exc:
        return {
            "status": "error",
            "data": {"error": str(exc)},
            "timestamp": datetime.now(timezone.utc).isoformat(),
        }
