"""
Executive Summary: Maximum distributable amount calculator referencing CRD IV buffer hierarchy.
Inputs: cet1_ratio_pct (float), combined_buffer_requirement_pct (float), distributable_profits (float), risk_weighted_assets (float)
Outputs: mda (float), restriction_tier (str), payout_capacity_pct (float)
MCP Tool Name: dividend_capacity_analyzer
"""
import logging
from datetime import datetime, timezone
from typing import Any

logger = logging.getLogger("snowdrop.skills")

TOOL_META = {
    "name": "dividend_capacity_analyzer",
    "description": "Determines MDA and dividend restrictions relative to combined capital buffer requirements.",
    "inputSchema": {
        "type": "object",
        "properties": {
            "cet1_ratio_pct": {"type": "number", "description": "Current CET1 ratio."},
            "combined_buffer_requirement_pct": {"type": "number", "description": "Capital conservation + CCyB + G-SIB buffer."},
            "distributable_profits": {"type": "number", "description": "Current year distributable profits."},
            "risk_weighted_assets": {"type": "number", "description": "RWA amount."},
        },
        "required": ["cet1_ratio_pct", "combined_buffer_requirement_pct", "distributable_profits", "risk_weighted_assets"],
    },
    "outputSchema": {
        "type": "object",
        "properties": {
            "status": {"type": "string", "description": "status"},
            "data": {"type": "object", "description": "MDA output"},
            "timestamp": {"type": "string", "description": "timestamp"},
        },
        "required": ["status", "timestamp"],
    },
}


def dividend_capacity_analyzer(
    cet1_ratio_pct: float,
    combined_buffer_requirement_pct: float,
    distributable_profits: float,
    risk_weighted_assets: float,
    **_: Any,
) -> dict[str, Any]:
    try:
        excess_buffer = cet1_ratio_pct - combined_buffer_requirement_pct
        if excess_buffer <= 0:
            mda_multiplier = 0.0
            restriction_tier = "full_restriction"
        elif excess_buffer <= 0.25 * combined_buffer_requirement_pct:
            mda_multiplier = 0.2
            restriction_tier = "tier_1"
        elif excess_buffer <= 0.5 * combined_buffer_requirement_pct:
            mda_multiplier = 0.4
            restriction_tier = "tier_2"
        elif excess_buffer <= 0.75 * combined_buffer_requirement_pct:
            mda_multiplier = 0.6
            restriction_tier = "tier_3"
        else:
            mda_multiplier = 1.0
            restriction_tier = "no_restriction"
        mda_amount = distributable_profits * mda_multiplier
        payout_capacity_pct = (mda_amount / risk_weighted_assets) * 100 if risk_weighted_assets else 0.0
        data = {
            "mda": round(mda_amount, 2),
            "restriction_tier": restriction_tier,
            "payout_capacity_pct": round(payout_capacity_pct, 4),
        }
        return {
            "status": "success",
            "data": data,
            "timestamp": datetime.now(timezone.utc).isoformat(),
        }
    except (ValueError, TypeError, ZeroDivisionError) as e:
        logger.error(f"dividend_capacity_analyzer failed: {e}")
        _log_lesson(f"dividend_capacity_analyzer: {e}")
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
