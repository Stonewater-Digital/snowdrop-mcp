"""
Executive Summary: TLAC adequacy metrics comparing eligible capital to RWA and leverage exposure requirements.
Inputs: cet1 (float), at1 (float), tier2 (float), eligible_senior (float), rwa (float), leverage_exposure (float)
Outputs: tlac_rwa_ratio (float), tlac_leverage_ratio (float), surplus_deficit (dict)
MCP Tool Name: tlac_calculator
"""
import logging
from datetime import datetime, timezone
from typing import Any

logger = logging.getLogger("snowdrop.skills")

TOOL_META = {
    "name": "tlac_calculator",
    "description": "Calculates TLAC ratios vs 18% RWA and 6.75% leverage thresholds (US G-SIB).",
    "inputSchema": {
        "type": "object",
        "properties": {
            "cet1": {"type": "number", "description": "Common equity tier 1"},
            "at1": {"type": "number", "description": "Additional tier 1 capital"},
            "tier2": {"type": "number", "description": "Tier 2 capital"},
            "eligible_senior": {"type": "number", "description": "Eligible long-term debt"},
            "rwa": {"type": "number", "description": "Risk-weighted assets"},
            "leverage_exposure": {"type": "number", "description": "Total leverage exposure"},
        },
        "required": ["cet1", "at1", "tier2", "eligible_senior", "rwa", "leverage_exposure"],
    },
    "outputSchema": {
        "type": "object",
        "properties": {
            "status": {"type": "string", "description": "status"},
            "data": {"type": "object", "description": "TLAC metrics"},
            "timestamp": {"type": "string", "description": "timestamp"},
        },
        "required": ["status", "timestamp"],
    },
}


def tlac_calculator(
    cet1: float,
    at1: float,
    tier2: float,
    eligible_senior: float,
    rwa: float,
    leverage_exposure: float,
    rwa_requirement_pct: float = 18.0,
    leverage_requirement_pct: float = 6.75,
    **_: Any,
) -> dict[str, Any]:
    try:
        tlac = cet1 + at1 + tier2 + eligible_senior
        tlac_rwa_ratio = tlac / rwa if rwa else 0.0
        tlac_leverage_ratio = tlac / leverage_exposure if leverage_exposure else 0.0
        rwa_surplus = tlac_rwa_ratio * 100 - rwa_requirement_pct
        leverage_surplus = tlac_leverage_ratio * 100 - leverage_requirement_pct
        data = {
            "tlac_rwa_ratio_pct": round(tlac_rwa_ratio * 100, 2),
            "tlac_leverage_ratio_pct": round(tlac_leverage_ratio * 100, 2),
            "total_tlac": round(tlac, 2),
            "surplus_deficit": {
                "rwa_pct": round(rwa_surplus, 2),
                "leverage_pct": round(leverage_surplus, 2),
            },
        }
        return {
            "status": "success",
            "data": data,
            "timestamp": datetime.now(timezone.utc).isoformat(),
        }
    except (ValueError, TypeError, ZeroDivisionError) as e:
        logger.error(f"tlac_calculator failed: {e}")
        _log_lesson(f"tlac_calculator: {e}")
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
