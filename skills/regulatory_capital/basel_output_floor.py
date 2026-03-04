"""
Executive Summary: Basel III output floor comparing IRB RWA to 72.5% of standardized RWA.
Inputs: irb_rwa (float), standardized_rwa (float)
Outputs: floored_rwa (float), floor_binding (bool), capital_impact (float)
MCP Tool Name: basel_output_floor
"""
import logging
from datetime import datetime, timezone
from typing import Any

logger = logging.getLogger("snowdrop.skills")

TOOL_META = {
    "name": "basel_output_floor",
    "description": "Applies 72.5% output floor to IRB RWA and quantifies capital impact.",
    "inputSchema": {
        "type": "object",
        "properties": {
            "irb_rwa": {"type": "number", "description": "Internal ratings-based RWA."},
            "standardized_rwa": {"type": "number", "description": "Standardized approach RWA."},
        },
        "required": ["irb_rwa", "standardized_rwa"],
    },
    "outputSchema": {
        "type": "object",
        "properties": {
            "status": {"type": "string", "description": "status"},
            "data": {"type": "object", "description": "Floor output"},
            "timestamp": {"type": "string", "description": "timestamp"},
        },
        "required": ["status", "timestamp"],
    },
}


def basel_output_floor(irb_rwa: float, standardized_rwa: float, **_: Any) -> dict[str, Any]:
    try:
        floor = 0.725 * standardized_rwa
        floored_rwa = max(irb_rwa, floor)
        binding = floor > irb_rwa
        capital_impact = (floored_rwa - irb_rwa) * 0.08
        data = {
            "floored_rwa": round(floored_rwa, 2),
            "floor_binding": binding,
            "capital_impact": round(capital_impact, 2),
            "floor_value": round(floor, 2),
        }
        return {
            "status": "success",
            "data": data,
            "timestamp": datetime.now(timezone.utc).isoformat(),
        }
    except (ValueError, TypeError, ZeroDivisionError) as e:
        logger.error(f"basel_output_floor failed: {e}")
        _log_lesson(f"basel_output_floor: {e}")
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
