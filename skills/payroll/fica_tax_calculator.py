"""Calculate FICA taxes (Social Security + Medicare) including self-employment.

MCP Tool Name: fica_tax_calculator
"""
from __future__ import annotations
from datetime import datetime, timezone
from typing import Any

TOOL_META: dict[str, Any] = {
    "name": "fica_tax_calculator",
    "description": "Calculate FICA taxes: Social Security (6.2% up to $168,600), Medicare (1.45%), and Additional Medicare Tax (0.9% over $200k). Doubles rates for self-employed.",
    "inputSchema": {
        "type": "object",
        "properties": {
            "gross_income": {
                "type": "number",
                "description": "Gross earned income in USD.",
            },
            "self_employed": {
                "type": "boolean",
                "description": "Whether the taxpayer is self-employed (pays both employer and employee shares).",
                "default": False,
            },
        },
        "required": ["gross_income"],
    },
}

_SS_RATE = 0.062
_MEDICARE_RATE = 0.0145
_ADDITIONAL_MEDICARE_RATE = 0.009
_SS_WAGE_BASE_2024 = 168600
_ADDITIONAL_MEDICARE_THRESHOLD = 200000  # Single filer


def fica_tax_calculator(
    gross_income: float,
    self_employed: bool = False,
) -> dict[str, Any]:
    """Calculate FICA taxes."""
    try:
        if gross_income < 0:
            return {
                "status": "error",
                "data": {"error": "gross_income must be non-negative."},
                "timestamp": datetime.now(timezone.utc).isoformat(),
            }

        multiplier = 2.0 if self_employed else 1.0

        # Self-employed: only 92.35% of net SE income is subject to FICA
        if self_employed:
            se_taxable = gross_income * 0.9235
        else:
            se_taxable = gross_income

        # Social Security
        ss_taxable = min(se_taxable, _SS_WAGE_BASE_2024)
        ss_tax = ss_taxable * _SS_RATE * multiplier

        # Medicare
        medicare_tax = se_taxable * _MEDICARE_RATE * multiplier

        # Additional Medicare Tax (employee-only, no employer match)
        additional_medicare_income = max(se_taxable - _ADDITIONAL_MEDICARE_THRESHOLD, 0)
        additional_medicare = additional_medicare_income * _ADDITIONAL_MEDICARE_RATE

        total_fica = ss_tax + medicare_tax + additional_medicare

        # Self-employed deduction: can deduct 50% of SE tax
        se_deduction = total_fica * 0.5 if self_employed else 0

        effective_rate = (total_fica / gross_income * 100) if gross_income > 0 else 0

        return {
            "status": "ok",
            "data": {
                "gross_income": round(gross_income, 2),
                "self_employed": self_employed,
                "se_taxable_income": round(se_taxable, 2) if self_employed else None,
                "social_security": {
                    "taxable_wages": round(ss_taxable, 2),
                    "wage_base": _SS_WAGE_BASE_2024,
                    "rate_pct": round(_SS_RATE * multiplier * 100, 2),
                    "tax": round(ss_tax, 2),
                },
                "medicare": {
                    "rate_pct": round(_MEDICARE_RATE * multiplier * 100, 2),
                    "tax": round(medicare_tax, 2),
                },
                "additional_medicare": {
                    "threshold": _ADDITIONAL_MEDICARE_THRESHOLD,
                    "income_over_threshold": round(additional_medicare_income, 2),
                    "rate_pct": round(_ADDITIONAL_MEDICARE_RATE * 100, 2),
                    "tax": round(additional_medicare, 2),
                },
                "total_fica": round(total_fica, 2),
                "se_deduction": round(se_deduction, 2),
                "effective_fica_rate_pct": round(effective_rate, 2),
            },
            "timestamp": datetime.now(timezone.utc).isoformat(),
        }
    except Exception as exc:
        return {
            "status": "error",
            "data": {"error": str(exc)},
            "timestamp": datetime.now(timezone.utc).isoformat(),
        }
