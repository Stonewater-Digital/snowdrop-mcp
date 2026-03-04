"""
Execuve Summary: Computes On-Balance Volume (OBV) to relate price direction with volume.
Inputs: closes (list[float]), volumes (list[float])
Outputs: obv_series (list[float]), current_obv (float), obv_trend (str), price_obv_divergence (str)
MCP Tool Name: obv_calculator
"""
import logging
import math
from datetime import datetime, timezone
from typing import Any

logger = logging.getLogger("snowdrop.skills")

TOOL_META = {
    "name": "obv_calculator",
    "description": "Computes cumulative On-Balance Volume to confirm price trends vs volume flows.",
    "inputSchema": {
        "type": "object",
        "properties": {
            "closes": {"type": "array", "description": "Closing prices (oldest first)."},
            "volumes": {"type": "array", "description": "Volume per period aligned with closes."}
        },
        "required": ["closes", "volumes"]
    },
    "outputSchema": {
        "type": "object",
        "properties": {
            "status": {"type": "string"},
            "timestamp": {"type": "string"},
            "data": {"type": "object"}
        },
        "required": ["status", "timestamp"]
    }
}


def obv_calculator(**kwargs: Any) -> dict:
    """Implements Joseph Granville's OBV by adding/subtracting volume based on price closes."""
    try:
        closes = kwargs.get("closes")
        volumes = kwargs.get("volumes")

        if not isinstance(closes, list) or not isinstance(volumes, list):
            raise ValueError("closes and volumes must be lists")
        if len(closes) != len(volumes) or len(closes) < 2:
            raise ValueError("closes and volumes must align and have at least two points")

        closes_f = []
        volumes_f = []
        for c, v in zip(closes, volumes):
            if not isinstance(c, (int, float)) or not isinstance(v, (int, float)):
                raise TypeError("closes and volumes must be numeric")
            closes_f.append(float(c))
            volumes_f.append(float(v))

        obv_series = [0.0]
        for idx in range(1, len(closes_f)):
            if closes_f[idx] > closes_f[idx - 1]:
                obv_series.append(obv_series[-1] + volumes_f[idx])
            elif closes_f[idx] < closes_f[idx - 1]:
                obv_series.append(obv_series[-1] - volumes_f[idx])
            else:
                obv_series.append(obv_series[-1])

        current_obv = obv_series[-1]
        slope = current_obv - obv_series[-2]
        if slope > 0:
            obv_trend = "rising"
        elif slope < 0:
            obv_trend = "falling"
        else:
            obv_trend = "flat"

        price_obv_divergence = "none"
        price_change = closes_f[-1] - closes_f[-2]
        if price_change > 0 and slope < 0:
            price_obv_divergence = "bearish"
        elif price_change < 0 and slope > 0:
            price_obv_divergence = "bullish"

        return {
            "status": "success",
            "data": {
                "obv_series": obv_series,
                "current_obv": current_obv,
                "obv_trend": obv_trend,
                "price_obv_divergence": price_obv_divergence
            },
            "timestamp": datetime.now(timezone.utc).isoformat()
        }
    except (ValueError, TypeError, ZeroDivisionError) as e:
        logger.error(f"obv_calculator failed: {e}")
        _log_lesson(f"obv_calculator: {e}")
        return {
            "status": "error",
            "error": str(e),
            "timestamp": datetime.now(timezone.utc).isoformat()
        }


def _log_lesson(message: str) -> None:
    try:
        with open("logs/lessons.md", "a") as f:
            f.write(f"- [{datetime.now(timezone.utc).isoformat()}] {message}\n")
    except OSError:
        pass
