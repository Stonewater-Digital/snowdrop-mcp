"""Compare multiple loan offers by monthly payment, total paid, and total interest.

MCP Tool Name: loan_comparison_calculator
"""
from __future__ import annotations
import math
from datetime import datetime, timezone
from typing import Any

TOOL_META: dict[str, Any] = {
    "name": "loan_comparison_calculator",
    "description": "Compare multiple loan offers side-by-side. For each loan compute monthly payment, total paid, and total interest, then rank by total cost.",
    "inputSchema": {
        "type": "object",
        "properties": {
            "loans": {
                "type": "array",
                "description": "List of loan offers to compare.",
                "items": {
                    "type": "object",
                    "properties": {
                        "name": {"type": "string", "description": "Loan label."},
                        "principal": {"type": "number", "description": "Loan amount."},
                        "rate": {"type": "number", "description": "Annual interest rate as decimal (e.g., 0.065)."},
                        "term_months": {"type": "integer", "description": "Loan term in months."},
                    },
                    "required": ["name", "principal", "rate", "term_months"],
                },
            },
        },
        "required": ["loans"],
    },
}


def _monthly_payment(principal: float, annual_rate: float, term_months: int) -> float:
    """Standard fixed-rate amortization payment."""
    if annual_rate == 0:
        return principal / term_months
    r = annual_rate / 12
    return principal * r * (1 + r) ** term_months / ((1 + r) ** term_months - 1)


def loan_comparison_calculator(loans: list[dict[str, Any]]) -> dict[str, Any]:
    """Compare multiple loan offers by total cost."""
    try:
        if not loans:
            return {
                "status": "error",
                "data": {"error": "loans list must not be empty."},
                "timestamp": datetime.now(timezone.utc).isoformat(),
            }

        results = []
        for loan in loans:
            p = loan["principal"]
            r = loan["rate"]
            t = loan["term_months"]
            if p <= 0 or t <= 0:
                continue
            pmt = _monthly_payment(p, r, t)
            total_paid = pmt * t
            total_interest = total_paid - p
            results.append({
                "name": loan["name"],
                "principal": p,
                "annual_rate_pct": round(r * 100, 4),
                "term_months": t,
                "monthly_payment": round(pmt, 2),
                "total_paid": round(total_paid, 2),
                "total_interest": round(total_interest, 2),
            })

        results.sort(key=lambda x: x["total_paid"])
        for rank, item in enumerate(results, 1):
            item["rank"] = rank

        return {
            "status": "ok",
            "data": {"comparisons": results, "cheapest": results[0]["name"] if results else None},
            "timestamp": datetime.now(timezone.utc).isoformat(),
        }
    except Exception as exc:
        return {
            "status": "error",
            "data": {"error": str(exc)},
            "timestamp": datetime.now(timezone.utc).isoformat(),
        }
