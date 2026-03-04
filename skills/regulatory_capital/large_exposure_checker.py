"""
Executive Summary: Basel large exposure monitoring (25% of Tier 1, 15% for G-SIBs).
Inputs: exposures (list[dict]), tier1_capital (float), is_gsib (bool)
Outputs: exposure_ratios (list[dict]), limit_breaches (list[dict])
MCP Tool Name: large_exposure_checker
"""
import logging
from datetime import datetime, timezone
from typing import Any, List

logger = logging.getLogger("snowdrop.skills")

TOOL_META = {
    "name": "large_exposure_checker",
    "description": "Identifies exposures exceeding Basel LE limits (25% Tier1, 15% for G-SIB counterparties).",
    "inputSchema": {
        "type": "object",
        "properties": {
            "exposures": {
                "type": "array",
                "description": "Counterparty exposure and group info.",
                "items": {
                    "type": "object",
                    "properties": {
                        "counterparty": {"type": "string", "description": "Counterparty name"},
                        "exposure": {"type": "number", "description": "Exposure measure"},
                        "connected_group": {"type": "string", "description": "Connected group id"},
                    },
                    "required": ["counterparty", "exposure"],
                },
            },
            "tier1_capital": {"type": "number", "description": "Tier 1 capital used for limit."},
            "is_gsib": {"type": "boolean", "description": "Whether firm is G-SIB (15% limit)."},
        },
        "required": ["exposures", "tier1_capital", "is_gsib"],
    },
    "outputSchema": {
        "type": "object",
        "properties": {
            "status": {"type": "string", "description": "status"},
            "data": {"type": "object", "description": "Large exposure summary"},
            "timestamp": {"type": "string", "description": "timestamp"},
        },
        "required": ["status", "timestamp"],
    },
}


def large_exposure_checker(
    exposures: List[dict[str, Any]],
    tier1_capital: float,
    is_gsib: bool,
    **_: Any,
) -> dict[str, Any]:
    try:
        limit_pct = 15.0 if is_gsib else 25.0
        ratios = []
        breaches = []
        for entry in exposures:
            ratio = entry["exposure"] / tier1_capital if tier1_capital else 0.0
            pct = ratio * 100
            ratios.append(
                {
                    "counterparty": entry["counterparty"],
                    "exposure": round(entry["exposure"], 2),
                    "ratio_pct": round(pct, 2),
                    "limit_pct": limit_pct,
                }
            )
            if pct > limit_pct:
                breaches.append(
                    {
                        "counterparty": entry["counterparty"],
                        "ratio_pct": round(pct, 2),
                        "excess_pct": round(pct - limit_pct, 2),
                    }
                )
        data = {
            "exposure_ratios": ratios,
            "limit_breaches": breaches,
            "limit_pct": limit_pct,
        }
        return {
            "status": "success",
            "data": data,
            "timestamp": datetime.now(timezone.utc).isoformat(),
        }
    except (ValueError, TypeError, ZeroDivisionError) as e:
        logger.error(f"large_exposure_checker failed: {e}")
        _log_lesson(f"large_exposure_checker: {e}")
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
