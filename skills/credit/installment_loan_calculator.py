"""Calculate installment loan payment and amortization summary.

MCP Tool Name: installment_loan_calculator
"""
from __future__ import annotations
from datetime import datetime, timezone
from typing import Any

TOOL_META: dict[str, Any] = {
    "name": "installment_loan_calculator",
    "description": "Calculate monthly payment, total interest, and amortization summary for a fixed-rate installment loan.",
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


def installment_loan_calculator(
    principal: float, apr: float, term_months: int
) -> dict[str, Any]:
    """Calculate installment loan payment and summary."""
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

        # Amortization summary: first, middle, and last payments
        balance = principal
        summary = []
        checkpoints = {1, term_months // 2, term_months}
        for month in range(1, term_months + 1):
            interest = balance * r
            princ = pmt - interest
            if month == term_months:
                princ = balance
            balance -= princ
            if month in checkpoints:
                summary.append({
                    "month": month,
                    "payment": round(pmt, 2),
                    "principal_portion": round(princ, 2),
                    "interest_portion": round(interest, 2),
                    "remaining_balance": round(max(balance, 0), 2),
                })

        return {
            "status": "ok",
            "data": {
                "principal": principal,
                "apr_pct": round(apr * 100, 4),
                "term_months": term_months,
                "monthly_payment": round(pmt, 2),
                "total_paid": round(total_paid, 2),
                "total_interest": round(total_interest, 2),
                "amortization_summary": summary,
            },
            "timestamp": datetime.now(timezone.utc).isoformat(),
        }
    except Exception as exc:
        return {
            "status": "error",
            "data": {"error": str(exc)},
            "timestamp": datetime.now(timezone.utc).isoformat(),
        }
