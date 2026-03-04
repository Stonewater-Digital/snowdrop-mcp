"""Calculate federal income tax withholding per pay period.

MCP Tool Name: withholding_calculator
"""
from __future__ import annotations
from datetime import datetime, timezone
from typing import Any

TOOL_META: dict[str, Any] = {
    "name": "withholding_calculator",
    "description": "Calculate federal income tax withholding per pay period by annualizing gross pay, applying 2024 tax brackets, and dividing back to per-period amounts.",
    "inputSchema": {
        "type": "object",
        "properties": {
            "gross_pay": {
                "type": "number",
                "description": "Gross pay for the period in USD.",
            },
            "pay_period": {
                "type": "string",
                "description": "Pay period frequency.",
                "enum": ["weekly", "biweekly", "semimonthly", "monthly", "annually"],
                "default": "biweekly",
            },
            "w4_filing_status": {
                "type": "string",
                "description": "W-4 filing status.",
                "enum": ["single", "married_filing_jointly"],
                "default": "single",
            },
            "allowances": {
                "type": "integer",
                "description": "Number of withholding allowances (pre-2020 W-4 style). Each reduces taxable by ~$4,300.",
                "default": 0,
            },
        },
        "required": ["gross_pay"],
    },
}

_PERIODS_PER_YEAR = {
    "weekly": 52,
    "biweekly": 26,
    "semimonthly": 24,
    "monthly": 12,
    "annually": 1,
}

_ALLOWANCE_VALUE = 4300  # Approximate per-allowance deduction

# 2024 brackets (same structure as marginal_tax_rate_calculator)
_BRACKETS = {
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
}


def _calc_tax(income: float, brackets: list[tuple[float, float]]) -> float:
    """Calculate tax through progressive brackets."""
    tax = 0.0
    prev = 0.0
    for limit, rate in brackets:
        taxable = min(income, limit) - prev
        if taxable <= 0:
            break
        tax += taxable * rate
        prev = limit
    return tax


def withholding_calculator(
    gross_pay: float,
    pay_period: str = "biweekly",
    w4_filing_status: str = "single",
    allowances: int = 0,
) -> dict[str, Any]:
    """Calculate federal income tax withholding per pay period."""
    try:
        pay_period = pay_period.lower().strip()
        w4_filing_status = w4_filing_status.lower().strip()

        if pay_period not in _PERIODS_PER_YEAR:
            return {
                "status": "error",
                "data": {"error": f"Invalid pay_period '{pay_period}'."},
                "timestamp": datetime.now(timezone.utc).isoformat(),
            }
        if w4_filing_status not in _BRACKETS:
            return {
                "status": "error",
                "data": {"error": f"Invalid w4_filing_status '{w4_filing_status}'. Use 'single' or 'married_filing_jointly'."},
                "timestamp": datetime.now(timezone.utc).isoformat(),
            }
        if gross_pay < 0:
            return {
                "status": "error",
                "data": {"error": "gross_pay must be non-negative."},
                "timestamp": datetime.now(timezone.utc).isoformat(),
            }

        periods = _PERIODS_PER_YEAR[pay_period]
        annualized = gross_pay * periods

        # Standard deduction
        std_deduction = 14600 if w4_filing_status == "single" else 29200
        allowance_deduction = allowances * _ALLOWANCE_VALUE

        taxable = max(annualized - std_deduction - allowance_deduction, 0)
        annual_tax = _calc_tax(taxable, _BRACKETS[w4_filing_status])
        per_period_withholding = annual_tax / periods

        return {
            "status": "ok",
            "data": {
                "gross_pay": round(gross_pay, 2),
                "pay_period": pay_period,
                "periods_per_year": periods,
                "annualized_gross": round(annualized, 2),
                "standard_deduction": round(std_deduction, 2),
                "allowance_deduction": round(allowance_deduction, 2),
                "annualized_taxable": round(taxable, 2),
                "annual_federal_tax": round(annual_tax, 2),
                "per_period_withholding": round(per_period_withholding, 2),
                "w4_filing_status": w4_filing_status,
                "allowances": allowances,
            },
            "timestamp": datetime.now(timezone.utc).isoformat(),
        }
    except Exception as exc:
        return {
            "status": "error",
            "data": {"error": str(exc)},
            "timestamp": datetime.now(timezone.utc).isoformat(),
        }
