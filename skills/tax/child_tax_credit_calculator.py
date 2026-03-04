"""Calculate Child Tax Credit with phase-out rules.

MCP Tool Name: child_tax_credit_calculator
"""
from __future__ import annotations
from datetime import datetime, timezone
from typing import Any

TOOL_META: dict[str, Any] = {
    "name": "child_tax_credit_calculator",
    "description": "Calculate the Child Tax Credit ($2,000 per child under 17) with income phase-out at $200k single / $400k MFJ. $50 reduction per $1,000 over threshold.",
    "inputSchema": {
        "type": "object",
        "properties": {
            "num_children_under_17": {
                "type": "integer",
                "description": "Number of qualifying children under age 17.",
            },
            "agi": {
                "type": "number",
                "description": "Adjusted gross income in USD.",
            },
            "filing_status": {
                "type": "string",
                "description": "Filing status.",
                "enum": ["single", "married_filing_jointly", "married_filing_separately", "head_of_household"],
                "default": "single",
            },
        },
        "required": ["num_children_under_17", "agi"],
    },
}

_CREDIT_PER_CHILD = 2000
_PHASE_OUT_THRESHOLDS = {
    "single": 200000,
    "married_filing_jointly": 400000,
    "married_filing_separately": 200000,
    "head_of_household": 200000,
}
_REDUCTION_PER_1000 = 50


def child_tax_credit_calculator(
    num_children_under_17: int,
    agi: float,
    filing_status: str = "single",
) -> dict[str, Any]:
    """Calculate Child Tax Credit with phase-out."""
    try:
        filing_status = filing_status.lower().strip()
        if filing_status not in _PHASE_OUT_THRESHOLDS:
            return {
                "status": "error",
                "data": {"error": f"Invalid filing_status '{filing_status}'."},
                "timestamp": datetime.now(timezone.utc).isoformat(),
            }
        if num_children_under_17 < 0:
            return {
                "status": "error",
                "data": {"error": "num_children_under_17 must be non-negative."},
                "timestamp": datetime.now(timezone.utc).isoformat(),
            }

        max_credit = num_children_under_17 * _CREDIT_PER_CHILD
        threshold = _PHASE_OUT_THRESHOLDS[filing_status]
        excess = max(agi - threshold, 0)

        # $50 reduction per $1,000 (or fraction thereof) over threshold
        import math
        reduction_units = math.ceil(excess / 1000)
        reduction = reduction_units * _REDUCTION_PER_1000
        credit = max(max_credit - reduction, 0)

        # Refundable portion (Additional Child Tax Credit): up to $1,700 per child
        refundable_per_child = 1700
        max_refundable = min(num_children_under_17 * refundable_per_child, credit)

        return {
            "status": "ok",
            "data": {
                "num_children": num_children_under_17,
                "agi": round(agi, 2),
                "filing_status": filing_status,
                "max_credit_before_phaseout": round(max_credit, 2),
                "phase_out_threshold": round(threshold, 2),
                "income_over_threshold": round(excess, 2),
                "phase_out_reduction": round(reduction, 2),
                "credit_after_phaseout": round(credit, 2),
                "refundable_portion_up_to": round(max_refundable, 2),
                "non_refundable_portion": round(max(credit - max_refundable, 0), 2),
            },
            "timestamp": datetime.now(timezone.utc).isoformat(),
        }
    except Exception as exc:
        return {
            "status": "error",
            "data": {"error": str(exc)},
            "timestamp": datetime.now(timezone.utc).isoformat(),
        }
