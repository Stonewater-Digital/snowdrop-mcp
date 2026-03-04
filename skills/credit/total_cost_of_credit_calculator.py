"""Calculate total cost of credit for a fixed-rate loan.

MCP Tool Name: total_cost_of_credit_calculator
"""
from __future__ import annotations
from datetime import datetime, timezone
from typing import Any

TOOL_META: dict[str, Any] = {
    "name": "total_cost_of_credit_calculator",
    "description": "Calculate total cost of credit: total paid, total interest, and effective rate for a fixed-rate loan.",
    "inputSchema": {
        "type": "object",
        "properties": {
            "principal": {"type": "number", "description": "Loan principal."},
            "apr": {"type": "number", "description": "Annual rate as decimal."},
            "term_months": {"type": "integer", "description": "Loan term in months."},
        },
        "required": ["principal", "apr", "term_months"],
    },
}


def total_cost_of_credit_calculator(
    principal: float, apr: float, term_months: int
) -> dict[str, Any]:
    """Calculate total cost of credit for a loan."""
    try:
        if principal <= 0 or term_months <= 0:
            return {
                "status": "error",
                "data": {"error": "principal and term_months must be positive."},
                "timestamp": datetime.now(timezone.utc).isoformat(),
            }

        r = apr / 12
        if apr == 0:
            pmt = principal / term_months
        else:
            pmt = principal * r * (1 + r) ** term_months / ((1 + r) ** term_months - 1)

        total_paid = pmt * term_months
        total_interest = total_paid - principal
        effective_rate = (total_interest / principal) * 100

        return {
            "status": "ok",
            "data": {
                "principal": principal,
                "apr_pct": round(apr * 100, 4),
                "term_months": term_months,
                "monthly_payment": round(pmt, 2),
                "total_paid": round(total_paid, 2),
                "total_interest": round(total_interest, 2),
                "effective_total_rate_pct": round(effective_rate, 2),
            },
            "timestamp": datetime.now(timezone.utc).isoformat(),
        }
    except Exception as exc:
        return {
            "status": "error",
            "data": {"error": str(exc)},
            "timestamp": datetime.now(timezone.utc).isoformat(),
        }
