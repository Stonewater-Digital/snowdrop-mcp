"""Analyze mortgage refinance: compare payments, breakeven, and total savings.

MCP Tool Name: mortgage_refinance_analyzer
"""
from __future__ import annotations
from datetime import datetime, timezone
from typing import Any

TOOL_META: dict[str, Any] = {
    "name": "mortgage_refinance_analyzer",
    "description": "Analyze whether refinancing a mortgage is worthwhile. Compare current vs new monthly payments, calculate breakeven month for closing costs, and total savings over the loan.",
    "inputSchema": {
        "type": "object",
        "properties": {
            "current_balance": {"type": "number", "description": "Remaining loan balance."},
            "current_rate": {"type": "number", "description": "Current annual rate as decimal."},
            "current_remaining_months": {"type": "integer", "description": "Months remaining on current loan."},
            "new_rate": {"type": "number", "description": "New annual rate as decimal."},
            "new_term_months": {"type": "integer", "description": "Term of the new loan in months."},
            "closing_costs": {"type": "number", "description": "Total closing costs for refinance."},
        },
        "required": [
            "current_balance", "current_rate", "current_remaining_months",
            "new_rate", "new_term_months", "closing_costs",
        ],
    },
}


def _pmt(principal: float, annual_rate: float, months: int) -> float:
    if annual_rate == 0:
        return principal / months
    r = annual_rate / 12
    return principal * r * (1 + r) ** months / ((1 + r) ** months - 1)


def mortgage_refinance_analyzer(
    current_balance: float,
    current_rate: float,
    current_remaining_months: int,
    new_rate: float,
    new_term_months: int,
    closing_costs: float,
) -> dict[str, Any]:
    """Analyze mortgage refinance opportunity."""
    try:
        if current_balance <= 0 or current_remaining_months <= 0 or new_term_months <= 0:
            return {
                "status": "error",
                "data": {"error": "Balance and term values must be positive."},
                "timestamp": datetime.now(timezone.utc).isoformat(),
            }

        current_pmt = _pmt(current_balance, current_rate, current_remaining_months)
        new_pmt = _pmt(current_balance, new_rate, new_term_months)
        monthly_savings = current_pmt - new_pmt

        current_total = current_pmt * current_remaining_months
        new_total = new_pmt * new_term_months + closing_costs
        total_savings = current_total - new_total

        breakeven_months = None
        if monthly_savings > 0:
            breakeven_months = round(closing_costs / monthly_savings, 1)

        return {
            "status": "ok",
            "data": {
                "current_monthly_payment": round(current_pmt, 2),
                "new_monthly_payment": round(new_pmt, 2),
                "monthly_savings": round(monthly_savings, 2),
                "current_total_remaining": round(current_total, 2),
                "new_total_cost": round(new_total, 2),
                "total_savings": round(total_savings, 2),
                "closing_costs": closing_costs,
                "breakeven_months": breakeven_months,
                "recommendation": "Refinance" if total_savings > 0 else "Keep current loan",
            },
            "timestamp": datetime.now(timezone.utc).isoformat(),
        }
    except Exception as exc:
        return {
            "status": "error",
            "data": {"error": str(exc)},
            "timestamp": datetime.now(timezone.utc).isoformat(),
        }
