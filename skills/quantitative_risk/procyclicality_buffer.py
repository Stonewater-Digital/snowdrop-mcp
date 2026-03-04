"""
Executive Summary: Countercyclical capital buffer computation from credit-to-GDP gap and jurisdictional rates.
Inputs: credit_to_gdp_ratio (float), long_term_trend (float), jurisdictions (list[dict]), risk_weighted_assets (float)
Outputs: credit_gap (float), national_buffer_rate (float), institution_ccyb_rate (float), buffer_amount (float)
MCP Tool Name: procyclicality_buffer
"""
import logging
from datetime import datetime, timezone
from typing import Any, List

logger = logging.getLogger("snowdrop.skills")

TOOL_META = {
    "name": "procyclicality_buffer",
    "description": "Implements Basel CCyB mapping from credit-to-GDP gap and aggregates jurisdictional CCyB exposure-weighted rates.",
    "inputSchema": {
        "type": "object",
        "properties": {
            "credit_to_gdp_ratio": {"type": "number", "description": "Current credit-to-GDP ratio."},
            "long_term_trend": {"type": "number", "description": "HP-filter trend of credit-to-GDP."},
            "jurisdictions": {
                "type": "array",
                "description": "Exposure shares per jurisdiction with local CCyB rate.",
                "items": {
                    "type": "object",
                    "properties": {
                        "jurisdiction": {"type": "string", "description": "Jurisdiction name"},
                        "exposure_share_pct": {"type": "number", "description": "Exposure share percentage"},
                        "ccyb_rate_pct": {"type": "number", "description": "Jurisdiction CCyB rate"},
                    },
                    "required": ["jurisdiction", "exposure_share_pct", "ccyb_rate_pct"],
                },
            },
            "risk_weighted_assets": {
                "type": "number",
                "description": "Risk-weighted assets to translate CCyB rate into buffer.",
                "default": 0.0,
            },
        },
        "required": ["credit_to_gdp_ratio", "long_term_trend", "jurisdictions"],
    },
    "outputSchema": {
        "type": "object",
        "properties": {
            "status": {"type": "string", "description": "status"},
            "data": {"type": "object", "description": "CCyB metrics"},
            "timestamp": {"type": "string", "description": "timestamp"},
        },
        "required": ["status", "timestamp"],
    },
}


def procyclicality_buffer(
    credit_to_gdp_ratio: float,
    long_term_trend: float,
    jurisdictions: List[dict[str, Any]],
    risk_weighted_assets: float = 0.0,
    **_: Any,
) -> dict[str, Any]:
    try:
        if not jurisdictions:
            raise ValueError("jurisdictions required")
        credit_gap = credit_to_gdp_ratio - long_term_trend
        if credit_gap <= 2:
            national_buffer = 0.0
        elif credit_gap >= 10:
            national_buffer = 2.5
        else:
            national_buffer = (credit_gap - 2) * (2.5 / 8)
        institution_rate = 0.0
        for entry in jurisdictions:
            institution_rate += (entry["exposure_share_pct"] / 100.0) * entry["ccyb_rate_pct"]
        buffer_amount = risk_weighted_assets * (institution_rate / 100.0)
        data = {
            "credit_gap": round(credit_gap, 2),
            "national_buffer_rate_pct": round(national_buffer, 2),
            "institution_ccyb_rate_pct": round(institution_rate, 2),
            "buffer_amount": round(buffer_amount, 2),
            "jurisdiction_breakdown": jurisdictions,
        }
        return {
            "status": "success",
            "data": data,
            "timestamp": datetime.now(timezone.utc).isoformat(),
        }
    except (ValueError, TypeError, ZeroDivisionError) as e:
        logger.error(f"procyclicality_buffer failed: {e}")
        _log_lesson(f"procyclicality_buffer: {e}")
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
