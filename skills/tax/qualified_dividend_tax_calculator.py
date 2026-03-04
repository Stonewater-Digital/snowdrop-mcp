"""Calculate tax on qualified dividends using 0/15/20% rate tiers.

MCP Tool Name: qualified_dividend_tax_calculator
"""
from __future__ import annotations
from datetime import datetime, timezone
from typing import Any

TOOL_META: dict[str, Any] = {
    "name": "qualified_dividend_tax_calculator",
    "description": "Calculate tax on qualified dividends at preferential 0%, 15%, or 20% rates based on taxable income and filing status (2024 thresholds).",
    "inputSchema": {
        "type": "object",
        "properties": {
            "dividend_amount": {
                "type": "number",
                "description": "Total qualified dividend amount in USD.",
            },
            "taxable_income": {
                "type": "number",
                "description": "Total taxable income including dividends in USD.",
            },
            "filing_status": {
                "type": "string",
                "description": "Filing status.",
                "enum": ["single", "married_filing_jointly", "married_filing_separately", "head_of_household"],
                "default": "single",
            },
        },
        "required": ["dividend_amount", "taxable_income"],
    },
}

# 2024 qualified dividend / long-term CG thresholds
_THRESHOLDS: dict[str, list[tuple[float, float]]] = {
    "single": [
        (47025, 0.00),
        (518900, 0.15),
        (float("inf"), 0.20),
    ],
    "married_filing_jointly": [
        (94050, 0.00),
        (583750, 0.15),
        (float("inf"), 0.20),
    ],
    "married_filing_separately": [
        (47025, 0.00),
        (291850, 0.15),
        (float("inf"), 0.20),
    ],
    "head_of_household": [
        (63000, 0.00),
        (551350, 0.15),
        (float("inf"), 0.20),
    ],
}

# NIIT thresholds
_NIIT_THRESHOLDS = {
    "single": 200000,
    "married_filing_jointly": 250000,
    "married_filing_separately": 125000,
    "head_of_household": 200000,
}
_NIIT_RATE = 0.038


def qualified_dividend_tax_calculator(
    dividend_amount: float,
    taxable_income: float,
    filing_status: str = "single",
) -> dict[str, Any]:
    """Calculate tax on qualified dividends."""
    try:
        filing_status = filing_status.lower().strip()
        if filing_status not in _THRESHOLDS:
            return {
                "status": "error",
                "data": {"error": f"Invalid filing_status '{filing_status}'."},
                "timestamp": datetime.now(timezone.utc).isoformat(),
            }
        if dividend_amount < 0 or taxable_income < 0:
            return {
                "status": "error",
                "data": {"error": "Amounts must be non-negative."},
                "timestamp": datetime.now(timezone.utc).isoformat(),
            }

        thresholds = _THRESHOLDS[filing_status]

        # Determine rate based on taxable income
        # Dividends are stacked on top of ordinary income
        ordinary_income = taxable_income - dividend_amount
        ordinary_income = max(ordinary_income, 0)

        remaining_div = dividend_amount
        total_tax = 0.0
        breakdown: list[dict[str, Any]] = []
        prev_limit = 0.0

        for limit, rate in thresholds:
            if remaining_div <= 0:
                break
            # How much room is left in this bracket after ordinary income
            bracket_top = limit
            bracket_bottom = prev_limit
            if ordinary_income >= bracket_top:
                prev_limit = limit
                continue
            start = max(ordinary_income, bracket_bottom)
            room = bracket_top - start
            taxed_here = min(remaining_div, room)
            if taxed_here > 0:
                tax_here = taxed_here * rate
                total_tax += tax_here
                breakdown.append({
                    "rate_pct": round(rate * 100, 1),
                    "dividend_taxed": round(taxed_here, 2),
                    "tax": round(tax_here, 2),
                })
                remaining_div -= taxed_here
            prev_limit = limit

        # NIIT check
        niit_threshold = _NIIT_THRESHOLDS[filing_status]
        magi_over = max(taxable_income - niit_threshold, 0)
        niit_taxable = min(dividend_amount, magi_over)
        niit = niit_taxable * _NIIT_RATE if niit_taxable > 0 else 0.0

        return {
            "status": "ok",
            "data": {
                "dividend_amount": round(dividend_amount, 2),
                "taxable_income": round(taxable_income, 2),
                "filing_status": filing_status,
                "dividend_tax": round(total_tax, 2),
                "niit": round(niit, 2),
                "total_tax": round(total_tax + niit, 2),
                "effective_rate_pct": round((total_tax + niit) / dividend_amount * 100, 2) if dividend_amount > 0 else 0.0,
                "bracket_breakdown": breakdown,
            },
            "timestamp": datetime.now(timezone.utc).isoformat(),
        }
    except Exception as exc:
        return {
            "status": "error",
            "data": {"error": str(exc)},
            "timestamp": datetime.now(timezone.utc).isoformat(),
        }
