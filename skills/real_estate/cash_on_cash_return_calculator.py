"""Calculate cash-on-cash return for a real estate investment.

MCP Tool Name: cash_on_cash_return_calculator
"""
from __future__ import annotations
from datetime import datetime, timezone
from typing import Any

TOOL_META: dict[str, Any] = {
    "name": "cash_on_cash_return_calculator",
    "description": "Calculate cash-on-cash return: annual pre-tax cash flow divided by total cash invested.",
    "inputSchema": {
        "type": "object",
        "properties": {
            "annual_cash_flow": {
                "type": "number",
                "description": "Annual pre-tax cash flow in USD (after debt service).",
            },
            "total_cash_invested": {
                "type": "number",
                "description": "Total cash invested (down payment + closing costs + rehab) in USD.",
            },
        },
        "required": ["annual_cash_flow", "total_cash_invested"],
    },
}


def cash_on_cash_return_calculator(
    annual_cash_flow: float,
    total_cash_invested: float,
) -> dict[str, Any]:
    """Calculate cash-on-cash return."""
    try:
        if total_cash_invested <= 0:
            return {
                "status": "error",
                "data": {"error": "total_cash_invested must be positive."},
                "timestamp": datetime.now(timezone.utc).isoformat(),
            }

        coc = annual_cash_flow / total_cash_invested * 100
        monthly_cash_flow = annual_cash_flow / 12

        return {
            "status": "ok",
            "data": {
                "annual_cash_flow": round(annual_cash_flow, 2),
                "monthly_cash_flow": round(monthly_cash_flow, 2),
                "total_cash_invested": round(total_cash_invested, 2),
                "cash_on_cash_return_pct": round(coc, 3),
            },
            "timestamp": datetime.now(timezone.utc).isoformat(),
        }
    except Exception as exc:
        return {
            "status": "error",
            "data": {"error": str(exc)},
            "timestamp": datetime.now(timezone.utc).isoformat(),
        }
