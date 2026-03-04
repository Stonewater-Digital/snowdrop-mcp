"""Calculate monthly mortgage payment, total interest, and amortization summary.

MCP Tool Name: mortgage_payment_calculator
"""
from __future__ import annotations
from datetime import datetime, timezone
from typing import Any

TOOL_META: dict[str, Any] = {
    "name": "mortgage_payment_calculator",
    "description": "Calculate monthly mortgage payment using the standard amortization formula: M = P[r(1+r)^n] / [(1+r)^n - 1]. Returns monthly payment, total interest, and total paid.",
    "inputSchema": {
        "type": "object",
        "properties": {
            "principal": {
                "type": "number",
                "description": "Loan principal (amount borrowed) in USD.",
            },
            "annual_rate": {
                "type": "number",
                "description": "Annual interest rate as a decimal (e.g. 0.07 for 7%).",
            },
            "term_years": {
                "type": "integer",
                "description": "Loan term in years.",
                "default": 30,
            },
        },
        "required": ["principal", "annual_rate"],
    },
}


def mortgage_payment_calculator(
    principal: float,
    annual_rate: float,
    term_years: int = 30,
) -> dict[str, Any]:
    """Calculate monthly mortgage payment."""
    try:
        if principal <= 0:
            return {
                "status": "error",
                "data": {"error": "principal must be positive."},
                "timestamp": datetime.now(timezone.utc).isoformat(),
            }
        if annual_rate < 0:
            return {
                "status": "error",
                "data": {"error": "annual_rate must be non-negative."},
                "timestamp": datetime.now(timezone.utc).isoformat(),
            }
        if term_years <= 0:
            return {
                "status": "error",
                "data": {"error": "term_years must be positive."},
                "timestamp": datetime.now(timezone.utc).isoformat(),
            }

        monthly_rate = annual_rate / 12
        n = term_years * 12

        if monthly_rate > 0:
            monthly_payment = principal * (monthly_rate * (1 + monthly_rate) ** n) / ((1 + monthly_rate) ** n - 1)
        else:
            monthly_payment = principal / n

        total_paid = monthly_payment * n
        total_interest = total_paid - principal
        interest_to_principal_ratio = total_interest / principal if principal > 0 else 0

        # First month breakdown
        first_interest = principal * monthly_rate
        first_principal = monthly_payment - first_interest

        return {
            "status": "ok",
            "data": {
                "principal": round(principal, 2),
                "annual_rate_pct": round(annual_rate * 100, 3),
                "term_years": term_years,
                "monthly_payment": round(monthly_payment, 2),
                "total_paid": round(total_paid, 2),
                "total_interest": round(total_interest, 2),
                "interest_to_principal_ratio": round(interest_to_principal_ratio, 3),
                "first_month": {
                    "interest": round(first_interest, 2),
                    "principal": round(first_principal, 2),
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
