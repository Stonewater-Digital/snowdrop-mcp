"""
Executive Summary: Concentration risk diagnostics using Herfindahl-Hirschman index and granularity adjustments.
Inputs: exposures (list[dict])
Outputs: hhi (float), effective_names (float), granularity_adjustment (float), top_names (list[dict])
MCP Tool Name: concentration_risk_hhi
"""
import logging
from datetime import datetime, timezone
from typing import Any, List

logger = logging.getLogger("snowdrop.skills")

TOOL_META = {
    "name": "concentration_risk_hhi",
    "description": "Computes HHI, effective number of obligors, and top exposures akin to ECB concentration add-ons.",
    "inputSchema": {
        "type": "object",
        "properties": {
            "exposures": {
                "type": "array",
                "description": "Exposure list with obligor name and amount.",
                "items": {
                    "type": "object",
                    "properties": {
                        "obligor": {"type": "string", "description": "Obligor name"},
                        "exposure": {"type": "number", "description": "Exposure amount"},
                    },
                    "required": ["obligor", "exposure"],
                },
            }
        },
        "required": ["exposures"],
    },
    "outputSchema": {
        "type": "object",
        "properties": {
            "status": {"type": "string", "description": "status"},
            "data": {"type": "object", "description": "HHI results"},
            "timestamp": {"type": "string", "description": "timestamp"},
        },
        "required": ["status", "timestamp"],
    },
}


def concentration_risk_hhi(exposures: List[dict[str, Any]], **_: Any) -> dict[str, Any]:
    try:
        if not exposures:
            raise ValueError("exposures required")
        total = sum(item["exposure"] for item in exposures)
        if total <= 0:
            raise ValueError("total exposure must be positive")
        shares = [item["exposure"] / total for item in exposures]
        hhi = sum(share ** 2 for share in shares)
        effective_names = 1 / hhi if hhi else 0.0
        granularity_adj = max(hhi - (1 / len(exposures)), 0.0)
        top = sorted(exposures, key=lambda x: x["exposure"], reverse=True)[:5]
        top_breakdown = [
            {
                "obligor": item["obligor"],
                "exposure": round(item["exposure"], 2),
                "share_pct": round((item["exposure"] / total) * 100, 2),
            }
            for item in top
        ]
        data = {
            "hhi": round(hhi, 4),
            "effective_number_of_names": round(effective_names, 2),
            "granularity_adjustment": round(granularity_adj, 4),
            "top_exposures": top_breakdown,
            "top3_share_pct": round(sum(b["share_pct"] for b in top_breakdown[:3]), 2),
        }
        return {
            "status": "success",
            "data": data,
            "timestamp": datetime.now(timezone.utc).isoformat(),
        }
    except (ValueError, TypeError, ZeroDivisionError) as e:
        logger.error(f"concentration_risk_hhi failed: {e}")
        _log_lesson(f"concentration_risk_hhi: {e}")
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
