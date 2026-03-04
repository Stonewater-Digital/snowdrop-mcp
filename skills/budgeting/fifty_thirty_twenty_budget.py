"""Calculate a 50/30/20 budget breakdown from monthly income.

MCP Tool Name: fifty_thirty_twenty_budget
"""
from __future__ import annotations
from datetime import datetime, timezone
from typing import Any

TOOL_META: dict[str, Any] = {
    "name": "fifty_thirty_twenty_budget",
    "description": "Applies the 50/30/20 budgeting rule to split monthly income into needs, wants, and savings.",
    "inputSchema": {
        "type": "object",
        "properties": {
            "monthly_income": {
                "type": "number",
                "description": "Gross or net monthly income in dollars.",
            },
        },
        "required": ["monthly_income"],
    },
}


def fifty_thirty_twenty_budget(monthly_income: float) -> dict[str, Any]:
    """Applies the 50/30/20 budgeting rule."""
    try:
        if monthly_income <= 0:
            return {
                "status": "error",
                "data": {"error": "Monthly income must be a positive number."},
                "timestamp": datetime.now(timezone.utc).isoformat(),
            }

        needs = round(monthly_income * 0.50, 2)
        wants = round(monthly_income * 0.30, 2)
        savings = round(monthly_income * 0.20, 2)

        return {
            "status": "ok",
            "data": {
                "monthly_income": monthly_income,
                "needs": {
                    "amount": needs,
                    "percentage": 50,
                    "description": "Essential expenses: housing, utilities, groceries, insurance, minimum debt payments, transportation.",
                },
                "wants": {
                    "amount": wants,
                    "percentage": 30,
                    "description": "Discretionary spending: dining out, entertainment, hobbies, subscriptions, shopping.",
                },
                "savings": {
                    "amount": savings,
                    "percentage": 20,
                    "description": "Savings and debt repayment: emergency fund, retirement contributions, extra debt payments, investments.",
                },
                "annual_savings": round(savings * 12, 2),
                "rule_source": "Senator Elizabeth Warren's 'All Your Worth' (2005). A simple framework for balanced budgeting.",
            },
            "timestamp": datetime.now(timezone.utc).isoformat(),
        }
    except Exception as exc:
        return {
            "status": "error",
            "data": {"error": str(exc)},
            "timestamp": datetime.now(timezone.utc).isoformat(),
        }
