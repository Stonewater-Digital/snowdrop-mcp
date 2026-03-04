"""Calculate emergency fund target and timeline to reach it.

MCP Tool Name: emergency_fund_calculator
"""
from __future__ import annotations
import math
from datetime import datetime, timezone
from typing import Any

TOOL_META: dict[str, Any] = {
    "name": "emergency_fund_calculator",
    "description": "Calculates emergency fund target based on monthly expenses and provides timelines at 10% and 20% savings rates.",
    "inputSchema": {
        "type": "object",
        "properties": {
            "monthly_expenses": {
                "type": "number",
                "description": "Total monthly essential expenses in dollars.",
            },
            "months_target": {
                "type": "number",
                "description": "Number of months of expenses to save (default: 6).",
            },
        },
        "required": ["monthly_expenses"],
    },
}


def emergency_fund_calculator(
    monthly_expenses: float, months_target: float = 6
) -> dict[str, Any]:
    """Calculates emergency fund target and savings timeline."""
    try:
        if monthly_expenses <= 0:
            return {
                "status": "error",
                "data": {"error": "Monthly expenses must be a positive number."},
                "timestamp": datetime.now(timezone.utc).isoformat(),
            }
        if months_target <= 0:
            return {
                "status": "error",
                "data": {"error": "Months target must be a positive number."},
                "timestamp": datetime.now(timezone.utc).isoformat(),
            }

        target = round(monthly_expenses * months_target, 2)

        savings_10_pct = round(monthly_expenses * 0.10, 2)
        savings_20_pct = round(monthly_expenses * 0.20, 2)

        months_at_10 = math.ceil(target / savings_10_pct) if savings_10_pct > 0 else None
        months_at_20 = math.ceil(target / savings_20_pct) if savings_20_pct > 0 else None

        return {
            "status": "ok",
            "data": {
                "monthly_expenses": monthly_expenses,
                "months_of_coverage": months_target,
                "target_amount": target,
                "savings_timeline": {
                    "at_10_percent_savings_rate": {
                        "monthly_savings": savings_10_pct,
                        "months_to_goal": months_at_10,
                        "years_to_goal": round(months_at_10 / 12, 1) if months_at_10 else None,
                    },
                    "at_20_percent_savings_rate": {
                        "monthly_savings": savings_20_pct,
                        "months_to_goal": months_at_20,
                        "years_to_goal": round(months_at_20 / 12, 1) if months_at_20 else None,
                    },
                },
                "recommended_location": "High-yield savings account (HYSA) for liquidity and FDIC insurance.",
                "guidance": {
                    "minimum": f"{3} months for dual-income households with stable jobs",
                    "standard": f"{6} months for most individuals",
                    "conservative": f"{9}-{12} months for single-income, self-employed, or variable income",
                },
            },
            "timestamp": datetime.now(timezone.utc).isoformat(),
        }
    except Exception as exc:
        return {
            "status": "error",
            "data": {"error": str(exc)},
            "timestamp": datetime.now(timezone.utc).isoformat(),
        }
