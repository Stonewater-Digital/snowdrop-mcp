"""Calculate effective tax rate from total tax paid and total income.

MCP Tool Name: effective_tax_rate_calculator
"""
from __future__ import annotations
from datetime import datetime, timezone
from typing import Any

TOOL_META: dict[str, Any] = {
    "name": "effective_tax_rate_calculator",
    "description": "Calculate effective tax rate from total tax paid and total income. Compares effective rate to marginal rate for context.",
    "inputSchema": {
        "type": "object",
        "properties": {
            "total_tax_paid": {
                "type": "number",
                "description": "Total tax paid (federal, or total including state/local).",
            },
            "total_income": {
                "type": "number",
                "description": "Total income (gross or adjusted gross income).",
            },
        },
        "required": ["total_tax_paid", "total_income"],
    },
}

# 2024 marginal brackets (single) for reference
_SINGLE_BRACKETS = [
    (11600, 0.10), (47150, 0.12), (100525, 0.22), (191950, 0.24),
    (243725, 0.32), (609350, 0.35), (float("inf"), 0.37),
]


def effective_tax_rate_calculator(
    total_tax_paid: float,
    total_income: float,
) -> dict[str, Any]:
    """Calculate effective tax rate."""
    try:
        if total_income == 0:
            return {
                "status": "error",
                "data": {"error": "Total income cannot be zero."},
                "timestamp": datetime.now(timezone.utc).isoformat(),
            }

        effective_rate = total_tax_paid / total_income * 100

        # Determine approximate marginal bracket (single filer reference)
        marginal_rate = 0.0
        for threshold, rate in _SINGLE_BRACKETS:
            marginal_rate = rate
            if total_income <= threshold:
                break

        spread = marginal_rate * 100 - effective_rate

        if effective_rate < 10:
            assessment = "Very low effective tax rate"
        elif effective_rate < 15:
            assessment = "Below-average effective tax rate"
        elif effective_rate < 20:
            assessment = "Near-average effective tax rate for middle income"
        elif effective_rate < 25:
            assessment = "Above-average effective tax rate"
        elif effective_rate < 30:
            assessment = "High effective tax rate"
        else:
            assessment = "Very high effective tax rate"

        return {
            "status": "ok",
            "data": {
                "total_tax_paid": round(total_tax_paid, 2),
                "total_income": round(total_income, 2),
                "effective_tax_rate_pct": round(effective_rate, 2),
                "marginal_bracket_pct_single_ref": round(marginal_rate * 100, 0),
                "spread_marginal_minus_effective": round(spread, 2),
                "assessment": assessment,
                "interpretation": (
                    f"Your effective tax rate is {effective_rate:.2f}%, meaning you pay "
                    f"${total_tax_paid:,.2f} on ${total_income:,.2f} of income. "
                    f"Your marginal rate (for a single filer) would be {marginal_rate*100:.0f}%, "
                    f"but progressive brackets mean your effective rate is {spread:.1f} percentage points lower."
                ),
                "note": "The effective rate is always lower than the marginal rate due to progressive taxation. "
                "Only income above each bracket threshold is taxed at the higher rate. "
                "Marginal rate shown is for single filers — adjust for your filing status.",
            },
            "timestamp": datetime.now(timezone.utc).isoformat(),
        }
    except Exception as exc:
        return {
            "status": "error",
            "data": {"error": str(exc)},
            "timestamp": datetime.now(timezone.utc).isoformat(),
        }
