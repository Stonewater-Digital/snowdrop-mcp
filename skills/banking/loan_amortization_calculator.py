"""Generate a full loan amortization schedule.

MCP Tool Name: loan_amortization_calculator
"""
from __future__ import annotations
from datetime import datetime, timezone
from typing import Any

TOOL_META: dict[str, Any] = {
    "name": "loan_amortization_calculator",
    "description": "Generate a full amortization schedule for a fixed-rate loan showing month, payment, principal, interest, and remaining balance for each period.",
    "inputSchema": {
        "type": "object",
        "properties": {
            "principal": {"type": "number", "description": "Loan principal amount."},
            "annual_rate": {"type": "number", "description": "Annual interest rate as decimal."},
            "term_months": {"type": "integer", "description": "Loan term in months."},
        },
        "required": ["principal", "annual_rate", "term_months"],
    },
}


def loan_amortization_calculator(
    principal: float, annual_rate: float, term_months: int
) -> dict[str, Any]:
    """Generate full amortization schedule."""
    try:
        if principal <= 0 or term_months <= 0:
            return {
                "status": "error",
                "data": {"error": "principal and term_months must be positive."},
                "timestamp": datetime.now(timezone.utc).isoformat(),
            }

        r = annual_rate / 12
        if annual_rate == 0:
            pmt = principal / term_months
        else:
            pmt = principal * r * (1 + r) ** term_months / ((1 + r) ** term_months - 1)

        schedule = []
        balance = principal
        total_interest = 0.0

        for month in range(1, term_months + 1):
            interest = balance * r
            princ = pmt - interest
            if month == term_months:
                # Final payment adjustment to zero out balance
                princ = balance
                pmt_final = princ + interest
            else:
                pmt_final = pmt
            balance -= princ
            total_interest += interest
            schedule.append({
                "month": month,
                "payment": round(pmt_final, 2),
                "principal": round(princ, 2),
                "interest": round(interest, 2),
                "balance": round(max(balance, 0), 2),
            })

        return {
            "status": "ok",
            "data": {
                "principal": principal,
                "annual_rate_pct": round(annual_rate * 100, 4),
                "term_months": term_months,
                "monthly_payment": round(pmt, 2),
                "total_interest": round(total_interest, 2),
                "total_paid": round(principal + total_interest, 2),
                "schedule": schedule,
            },
            "timestamp": datetime.now(timezone.utc).isoformat(),
        }
    except Exception as exc:
        return {
            "status": "error",
            "data": {"error": str(exc)},
            "timestamp": datetime.now(timezone.utc).isoformat(),
        }
