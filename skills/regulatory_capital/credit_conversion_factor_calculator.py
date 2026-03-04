"""
Executive Summary: Off-balance sheet credit conversion factor per Basel rules.
Inputs: facility_type (str), drawn_amount (float), undrawn_commitment (float), regulatory_category (str)
Outputs: ccf_pct (float), credit_equivalent_amount (float), ead_contribution (float)
MCP Tool Name: credit_conversion_factor_calculator
"""
import logging
from datetime import datetime, timezone
from typing import Any

logger = logging.getLogger("snowdrop.skills")

TOOL_META = {
    "name": "credit_conversion_factor_calculator",
    "description": "Assigns Basel CCF based on facility type (commitment, guarantee, trade finance, etc.).",
    "inputSchema": {
        "type": "object",
        "properties": {
            "facility_type": {"type": "string", "description": "Facility description."},
            "drawn_amount": {"type": "number", "description": "Outstandings."},
            "undrawn_commitment": {"type": "number", "description": "Unused line amount."},
            "regulatory_category": {
                "type": "string",
                "description": "Basel category (e.g., irrevocable_commitment, performance_guarantee).",
            },
        },
        "required": ["facility_type", "drawn_amount", "undrawn_commitment", "regulatory_category"],
    },
    "outputSchema": {
        "type": "object",
        "properties": {
            "status": {"type": "string", "description": "status"},
            "data": {"type": "object", "description": "CCF output"},
            "timestamp": {"type": "string", "description": "timestamp"},
        },
        "required": ["status", "timestamp"],
    },
}

CCF_LOOKUP = {
    "irrevocable_commitment": 0.5,
    "unconditionally_cancelable": 0.1,
    "performance_guarantee": 0.5,
    "financial_guarantee": 1.0,
    "trade_letter_of_credit": 0.2,
}


def credit_conversion_factor_calculator(
    facility_type: str,
    drawn_amount: float,
    undrawn_commitment: float,
    regulatory_category: str,
    **_: Any,
) -> dict[str, Any]:
    try:
        ccf = CCF_LOOKUP.get(regulatory_category, 1.0)
        credit_equivalent = undrawn_commitment * ccf
        ead = drawn_amount + credit_equivalent
        data = {
            "facility_type": facility_type,
            "ccf_pct": round(ccf * 100, 2),
            "credit_equivalent_amount": round(credit_equivalent, 2),
            "ead_contribution": round(ead, 2),
        }
        return {
            "status": "success",
            "data": data,
            "timestamp": datetime.now(timezone.utc).isoformat(),
        }
    except (ValueError, TypeError, ZeroDivisionError) as e:
        logger.error(f"credit_conversion_factor_calculator failed: {e}")
        _log_lesson(f"credit_conversion_factor_calculator: {e}")
        return {
            "status": "error",
            "error": str(e),
            "timestamp": datetime.now(timezone.utc).isoformat(),
        }


def _log_lesson(message: str) -> None:
    try:
        with open("logs/lessons.md", "a", encoding="utf-8") as handle:
            handle.write(f"- [{datetime.now(timezone.utc).isoformat()}] {message}\n")
    except OSError:
        pass
