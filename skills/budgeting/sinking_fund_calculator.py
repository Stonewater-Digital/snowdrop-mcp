"""Calculate monthly contributions needed for a sinking fund goal.

MCP Tool Name: sinking_fund_calculator
"""
from __future__ import annotations
from datetime import datetime, timezone
from typing import Any

TOOL_META: dict[str, Any] = {
    "name": "sinking_fund_calculator",
    "description": "Calculates the monthly contribution needed to save a target amount by a deadline.",
    "inputSchema": {
        "type": "object",
        "properties": {
            "target_amount": {
                "type": "number",
                "description": "The total amount you need to save in dollars.",
            },
            "months_until_needed": {
                "type": "number",
                "description": "Number of months until the money is needed.",
            },
        },
        "required": ["target_amount", "months_until_needed"],
    },
}


def sinking_fund_calculator(target_amount: float, months_until_needed: float) -> dict[str, Any]:
    """Calculates monthly contribution for a sinking fund goal."""
    try:
        if target_amount <= 0:
            return {
                "status": "error",
                "data": {"error": "Target amount must be a positive number."},
                "timestamp": datetime.now(timezone.utc).isoformat(),
            }
        if months_until_needed <= 0:
            return {
                "status": "error",
                "data": {"error": "Months until needed must be a positive number."},
                "timestamp": datetime.now(timezone.utc).isoformat(),
            }

        monthly = round(target_amount / months_until_needed, 2)
        weekly = round(target_amount / (months_until_needed * 4.33), 2)
        biweekly = round(target_amount / (months_until_needed * 2.17), 2)

        return {
            "status": "ok",
            "data": {
                "target_amount": target_amount,
                "months_until_needed": months_until_needed,
                "monthly_contribution": monthly,
                "biweekly_contribution": biweekly,
                "weekly_contribution": weekly,
                "total_contributions": round(monthly * months_until_needed, 2),
                "note": "A sinking fund is a dedicated savings account for a planned future expense. Set up automatic transfers to stay on track.",
            },
            "timestamp": datetime.now(timezone.utc).isoformat(),
        }
    except Exception as exc:
        return {
            "status": "error",
            "data": {"error": str(exc)},
            "timestamp": datetime.now(timezone.utc).isoformat(),
        }
