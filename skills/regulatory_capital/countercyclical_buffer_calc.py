"""
Executive Summary: Institution-specific countercyclical buffer from jurisdictional CCyB rates.
Inputs: exposures (list[dict]), risk_weighted_assets (float)
Outputs: ccyb_rate_pct (float), buffer_amount (float), jurisdiction_breakdown (list[dict])
MCP Tool Name: countercyclical_buffer_calc
"""
import logging
from datetime import datetime, timezone
from typing import Any, List

logger = logging.getLogger("snowdrop.skills")

TOOL_META = {
    "name": "countercyclical_buffer_calc",
    "description": "Weights jurisdiction CCyB rates by credit exposures to derive bank-specific buffer.",
    "inputSchema": {
        "type": "object",
        "properties": {
            "exposures": {
                "type": "array",
                "description": "Exposures with CCyB rate info.",
                "items": {
                    "type": "object",
                    "properties": {
                        "jurisdiction": {"type": "string", "description": "Country name"},
                        "exposure": {"type": "number", "description": "Credit exposure amount"},
                        "ccyb_rate_pct": {"type": "number", "description": "Jurisdiction CCyB rate"},
                    },
                    "required": ["jurisdiction", "exposure", "ccyb_rate_pct"],
                },
            },
            "risk_weighted_assets": {"type": "number", "description": "Total RWA for translating rate to buffer amount."},
        },
        "required": ["exposures", "risk_weighted_assets"],
    },
    "outputSchema": {
        "type": "object",
        "properties": {
            "status": {"type": "string", "description": "status"},
            "data": {"type": "object", "description": "CCyB output"},
            "timestamp": {"type": "string", "description": "timestamp"},
        },
        "required": ["status", "timestamp"],
    },
}


def countercyclical_buffer_calc(
    exposures: List[dict[str, Any]],
    risk_weighted_assets: float,
    **_: Any,
) -> dict[str, Any]:
    try:
        total_exposure = sum(item["exposure"] for item in exposures)
        weighted_rate = sum(item["exposure"] * item["ccyb_rate_pct"] for item in exposures)
        ccyb_rate = weighted_rate / total_exposure if total_exposure else 0.0
        buffer_amount = risk_weighted_assets * ccyb_rate / 100.0
        data = {
            "ccyb_rate_pct": round(ccyb_rate, 2),
            "buffer_amount": round(buffer_amount, 2),
            "jurisdiction_breakdown": exposures,
        }
        return {
            "status": "success",
            "data": data,
            "timestamp": datetime.now(timezone.utc).isoformat(),
        }
    except (ValueError, TypeError, ZeroDivisionError) as e:
        logger.error(f"countercyclical_buffer_calc failed: {e}")
        _log_lesson(f"countercyclical_buffer_calc: {e}")
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
