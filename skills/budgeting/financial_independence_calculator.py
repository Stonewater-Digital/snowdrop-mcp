"""Calculate years to financial independence (FIRE number).

MCP Tool Name: financial_independence_calculator
"""
from __future__ import annotations
import math
from datetime import datetime, timezone
from typing import Any

TOOL_META: dict[str, Any] = {
    "name": "financial_independence_calculator",
    "description": "Calculates your FI number (25x annual expenses) and estimates years to financial independence using compound growth.",
    "inputSchema": {
        "type": "object",
        "properties": {
            "annual_expenses": {
                "type": "number",
                "description": "Current annual living expenses in dollars.",
            },
            "current_savings": {
                "type": "number",
                "description": "Current total invested savings/portfolio in dollars.",
            },
            "annual_savings": {
                "type": "number",
                "description": "Amount saved and invested per year in dollars.",
            },
            "expected_return": {
                "type": "number",
                "description": "Expected annual real (inflation-adjusted) investment return as a decimal (default: 0.07 for 7%).",
            },
        },
        "required": ["annual_expenses", "current_savings", "annual_savings"],
    },
}


def financial_independence_calculator(
    annual_expenses: float,
    current_savings: float,
    annual_savings: float,
    expected_return: float = 0.07,
) -> dict[str, Any]:
    """Calculates years to financial independence."""
    try:
        if annual_expenses <= 0:
            return {
                "status": "error",
                "data": {"error": "Annual expenses must be a positive number."},
                "timestamp": datetime.now(timezone.utc).isoformat(),
            }
        if annual_savings <= 0:
            return {
                "status": "error",
                "data": {"error": "Annual savings must be a positive number."},
                "timestamp": datetime.now(timezone.utc).isoformat(),
            }

        fi_number = round(annual_expenses * 25, 2)
        safe_withdrawal_rate = 4.0

        if current_savings >= fi_number:
            return {
                "status": "ok",
                "data": {
                    "fi_number": fi_number,
                    "current_savings": current_savings,
                    "status": "ALREADY FINANCIALLY INDEPENDENT",
                    "surplus": round(current_savings - fi_number, 2),
                    "safe_withdrawal_annual": round(current_savings * 0.04, 2),
                    "safe_withdrawal_monthly": round(current_savings * 0.04 / 12, 2),
                },
                "timestamp": datetime.now(timezone.utc).isoformat(),
            }

        # Calculate years to FI using iterative approach
        balance = current_savings
        years = 0
        max_years = 100

        while balance < fi_number and years < max_years:
            balance = balance * (1 + expected_return) + annual_savings
            years += 1

        savings_rate = round((annual_savings / (annual_expenses + annual_savings)) * 100, 2)
        gap = round(fi_number - current_savings, 2)
        progress = round((current_savings / fi_number) * 100, 2)

        return {
            "status": "ok",
            "data": {
                "fi_number": fi_number,
                "safe_withdrawal_rate_pct": safe_withdrawal_rate,
                "current_savings": current_savings,
                "gap_to_fi": gap,
                "progress_pct": progress,
                "annual_savings": annual_savings,
                "savings_rate_pct": savings_rate,
                "expected_return_pct": round(expected_return * 100, 2),
                "estimated_years_to_fi": years if years < max_years else "100+ (not achievable at current rate)",
                "projected_portfolio_at_fi": round(balance, 2),
                "note": "Based on the 4% Rule (Trinity Study). FI number = 25x annual expenses. Real returns (after inflation) used for projection.",
            },
            "timestamp": datetime.now(timezone.utc).isoformat(),
        }
    except Exception as exc:
        return {
            "status": "error",
            "data": {"error": str(exc)},
            "timestamp": datetime.now(timezone.utc).isoformat(),
        }
