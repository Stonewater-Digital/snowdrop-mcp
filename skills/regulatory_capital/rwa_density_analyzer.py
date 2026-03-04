"""
Executive Summary: RWA density analytics comparing RWAs to exposures by portfolio segments.
Inputs: segments (list[dict])
Outputs: density_by_segment (list[dict]), portfolio_density_pct (float), outliers (list[str])
MCP Tool Name: rwa_density_analyzer
"""
import logging
from datetime import datetime, timezone
from typing import Any, List

logger = logging.getLogger("snowdrop.skills")

TOOL_META = {
    "name": "rwa_density_analyzer",
    "description": "Computes RWA/exposure percentages and flags segments deviating from portfolio average.",
    "inputSchema": {
        "type": "object",
        "properties": {
            "segments": {
                "type": "array",
                "description": "List of segments with exposure and RWA amounts.",
                "items": {
                    "type": "object",
                    "properties": {
                        "segment": {"type": "string", "description": "Segment name"},
                        "exposure": {"type": "number", "description": "Exposure amount"},
                        "rwa": {"type": "number", "description": "Risk-weighted assets"},
                    },
                    "required": ["segment", "exposure", "rwa"],
                },
            }
        },
        "required": ["segments"],
    },
    "outputSchema": {
        "type": "object",
        "properties": {
            "status": {"type": "string", "description": "status"},
            "data": {"type": "object", "description": "Density metrics"},
            "timestamp": {"type": "string", "description": "timestamp"},
        },
        "required": ["status", "timestamp"],
    },
}


def rwa_density_analyzer(segments: List[dict[str, Any]], **_: Any) -> dict[str, Any]:
    try:
        if not segments:
            raise ValueError("segments required")
        total_exposure = sum(item["exposure"] for item in segments)
        total_rwa = sum(item["rwa"] for item in segments)
        portfolio_density = (total_rwa / total_exposure) * 100 if total_exposure else 0.0
        densities = []
        outliers = []
        for item in segments:
            density = (item["rwa"] / item["exposure"]) * 100 if item["exposure"] else 0.0
            densities.append(
                {
                    "segment": item["segment"],
                    "density_pct": round(density, 2),
                    "exposure": round(item["exposure"], 2),
                    "rwa": round(item["rwa"], 2),
                }
            )
            if abs(density - portfolio_density) > 10:
                outliers.append(item["segment"])
        data = {
            "density_by_segment": densities,
            "portfolio_density_pct": round(portfolio_density, 2),
            "outlier_segments": outliers,
        }
        return {
            "status": "success",
            "data": data,
            "timestamp": datetime.now(timezone.utc).isoformat(),
        }
    except (ValueError, TypeError, ZeroDivisionError) as e:
        logger.error(f"rwa_density_analyzer failed: {e}")
        _log_lesson(f"rwa_density_analyzer: {e}")
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
