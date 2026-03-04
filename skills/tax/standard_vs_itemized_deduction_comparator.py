"""Compare standard vs itemized deductions and recommend the better option.

MCP Tool Name: standard_vs_itemized_deduction_comparator
"""
from __future__ import annotations
from datetime import datetime, timezone
from typing import Any

TOOL_META: dict[str, Any] = {
    "name": "standard_vs_itemized_deduction_comparator",
    "description": "Compare standard deduction vs itemized deductions (mortgage interest, SALT capped at $10k, charitable, medical over 7.5% AGI) and recommend the higher deduction for 2024.",
    "inputSchema": {
        "type": "object",
        "properties": {
            "filing_status": {
                "type": "string",
                "description": "Filing status.",
                "enum": ["single", "married_filing_jointly", "married_filing_separately", "head_of_household"],
                "default": "single",
            },
            "mortgage_interest": {
                "type": "number",
                "description": "Mortgage interest paid in USD.",
                "default": 0,
            },
            "state_local_taxes": {
                "type": "number",
                "description": "State and local taxes paid (income + property) in USD.",
                "default": 0,
            },
            "charitable": {
                "type": "number",
                "description": "Charitable contributions in USD.",
                "default": 0,
            },
            "medical": {
                "type": "number",
                "description": "Total medical expenses in USD.",
                "default": 0,
            },
            "agi": {
                "type": "number",
                "description": "Adjusted gross income in USD.",
                "default": 100000,
            },
        },
        "required": [],
    },
}

# 2024 standard deduction amounts
_STANDARD_DEDUCTIONS = {
    "single": 14600,
    "married_filing_jointly": 29200,
    "married_filing_separately": 14600,
    "head_of_household": 21900,
}

_SALT_CAP = 10000  # $10,000 SALT cap ($5,000 for MFS)
_MEDICAL_FLOOR_PCT = 0.075  # 7.5% of AGI


def standard_vs_itemized_deduction_comparator(
    filing_status: str = "single",
    mortgage_interest: float = 0,
    state_local_taxes: float = 0,
    charitable: float = 0,
    medical: float = 0,
    agi: float = 100000,
) -> dict[str, Any]:
    """Compare standard vs itemized deductions."""
    try:
        filing_status = filing_status.lower().strip()
        if filing_status not in _STANDARD_DEDUCTIONS:
            return {
                "status": "error",
                "data": {"error": f"Invalid filing_status '{filing_status}'."},
                "timestamp": datetime.now(timezone.utc).isoformat(),
            }

        standard = _STANDARD_DEDUCTIONS[filing_status]

        # SALT deduction capped
        salt_cap = 5000 if filing_status == "married_filing_separately" else _SALT_CAP
        salt_deductible = min(state_local_taxes, salt_cap)

        # Medical: only amount exceeding 7.5% of AGI
        medical_floor = agi * _MEDICAL_FLOOR_PCT
        medical_deductible = max(medical - medical_floor, 0)

        # Charitable: generally limited to 60% of AGI for cash
        charitable_limit = agi * 0.60
        charitable_deductible = min(charitable, charitable_limit)

        total_itemized = mortgage_interest + salt_deductible + charitable_deductible + medical_deductible

        recommendation = "standard" if standard >= total_itemized else "itemized"
        benefit = abs(total_itemized - standard)

        return {
            "status": "ok",
            "data": {
                "filing_status": filing_status,
                "agi": round(agi, 2),
                "standard_deduction": round(standard, 2),
                "itemized_breakdown": {
                    "mortgage_interest": round(mortgage_interest, 2),
                    "salt_paid": round(state_local_taxes, 2),
                    "salt_deductible": round(salt_deductible, 2),
                    "salt_cap_applied": state_local_taxes > salt_cap,
                    "charitable_contributed": round(charitable, 2),
                    "charitable_deductible": round(charitable_deductible, 2),
                    "medical_total": round(medical, 2),
                    "medical_floor_7_5_pct": round(medical_floor, 2),
                    "medical_deductible": round(medical_deductible, 2),
                },
                "total_itemized": round(total_itemized, 2),
                "recommendation": recommendation,
                "additional_benefit": round(benefit, 2),
            },
            "timestamp": datetime.now(timezone.utc).isoformat(),
        }
    except Exception as exc:
        return {
            "status": "error",
            "data": {"error": str(exc)},
            "timestamp": datetime.now(timezone.utc).isoformat(),
        }
