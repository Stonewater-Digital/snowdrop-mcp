"""Calculate marginal tax rate using 2024 US federal income tax brackets.

MCP Tool Name: marginal_tax_rate_calculator
"""
from __future__ import annotations
from datetime import datetime, timezone
from typing import Any

TOOL_META: dict[str, Any] = {
    "name": "marginal_tax_rate_calculator",
    "description": "Calculate marginal federal tax rate and bracket breakdown for 2024 US tax brackets given taxable income and filing status.",
    "inputSchema": {
        "type": "object",
        "properties": {
            "taxable_income": {
                "type": "number",
                "description": "Total taxable income in USD.",
            },
            "filing_status": {
                "type": "string",
                "description": "Filing status: single, married_filing_jointly, married_filing_separately, or head_of_household.",
                "enum": [
                    "single",
                    "married_filing_jointly",
                    "married_filing_separately",
                    "head_of_household",
                ],
                "default": "single",
            },
        },
        "required": ["taxable_income"],
    },
}

# 2024 US federal income tax brackets
_BRACKETS: dict[str, list[tuple[float, float]]] = {
    "single": [
        (11600, 0.10),
        (47150, 0.12),
        (100525, 0.22),
        (191950, 0.24),
        (243725, 0.32),
        (609350, 0.35),
        (float("inf"), 0.37),
    ],
    "married_filing_jointly": [
        (23200, 0.10),
        (94300, 0.12),
        (201050, 0.22),
        (383900, 0.24),
        (487450, 0.32),
        (731200, 0.35),
        (float("inf"), 0.37),
    ],
    "married_filing_separately": [
        (11600, 0.10),
        (47150, 0.12),
        (100525, 0.22),
        (191950, 0.24),
        (243725, 0.32),
        (365600, 0.35),
        (float("inf"), 0.37),
    ],
    "head_of_household": [
        (16550, 0.10),
        (63100, 0.12),
        (100500, 0.22),
        (191950, 0.24),
        (243700, 0.32),
        (609350, 0.35),
        (float("inf"), 0.37),
    ],
}


def marginal_tax_rate_calculator(
    taxable_income: float,
    filing_status: str = "single",
) -> dict[str, Any]:
    """Calculate marginal federal tax rate and bracket breakdown."""
    try:
        filing_status = filing_status.lower().strip()
        if filing_status not in _BRACKETS:
            return {
                "status": "error",
                "data": {
                    "error": f"Invalid filing_status '{filing_status}'. Must be one of: {list(_BRACKETS.keys())}",
                },
                "timestamp": datetime.now(timezone.utc).isoformat(),
            }
        if taxable_income < 0:
            return {
                "status": "error",
                "data": {"error": "taxable_income must be non-negative."},
                "timestamp": datetime.now(timezone.utc).isoformat(),
            }

        brackets = _BRACKETS[filing_status]
        breakdown: list[dict[str, Any]] = []
        remaining = taxable_income
        total_tax = 0.0
        prev_limit = 0.0
        marginal_rate = 0.0

        for limit, rate in brackets:
            if remaining <= 0:
                break
            bracket_width = limit - prev_limit
            taxable_in_bracket = min(remaining, bracket_width)
            tax_in_bracket = taxable_in_bracket * rate
            total_tax += tax_in_bracket
            marginal_rate = rate
            breakdown.append(
                {
                    "bracket": f"{prev_limit:,.0f} - {limit:,.0f}" if limit != float("inf") else f"{prev_limit:,.0f}+",
                    "rate": round(rate * 100, 1),
                    "taxable_in_bracket": round(taxable_in_bracket, 2),
                    "tax_in_bracket": round(tax_in_bracket, 2),
                }
            )
            remaining -= taxable_in_bracket
            prev_limit = limit

        effective_rate = (total_tax / taxable_income * 100) if taxable_income > 0 else 0.0

        return {
            "status": "ok",
            "data": {
                "taxable_income": round(taxable_income, 2),
                "filing_status": filing_status,
                "marginal_rate_pct": round(marginal_rate * 100, 1),
                "effective_rate_pct": round(effective_rate, 2),
                "total_federal_tax": round(total_tax, 2),
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
