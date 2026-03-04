"""
Execuve Summary: Computes Chaikin Money Flow to gauge buying or selling pressure.
Inputs: highs (list[float]), lows (list[float]), closes (list[float]), volumes (list[float]), period (int)
Outputs: cmf_series (list[float]), current_cmf (float), buying_selling_pressure (str), signal (str)
MCP Tool Name: chaikin_money_flow
"""
import logging
import math
from datetime import datetime, timezone
from typing import Any

logger = logging.getLogger("snowdrop.skills")

TOOL_META = {
    "name": "chaikin_money_flow",
    "description": "Calculates Chaikin Money Flow (CMF) over a specified period to quantify accumulation or distribution.",
    "inputSchema": {
        "type": "object",
        "properties": {
            "highs": {"type": "array", "description": "High prices."},
            "lows": {"type": "array", "description": "Low prices."},
            "closes": {"type": "array", "description": "Close prices."},
            "volumes": {"type": "array", "description": "Volume per bar."},
            "period": {"type": "integer", "description": "Lookback for CMF (default 20)."}
        },
        "required": ["highs", "lows", "closes", "volumes", "period"]
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


def chaikin_money_flow(**kwargs: Any) -> dict:
    """Computes CMF by summing money flow volume over the selected period divided by total volume."""
    try:
        highs = kwargs.get("highs")
        lows = kwargs.get("lows")
        closes = kwargs.get("closes")
        volumes = kwargs.get("volumes")
        period = kwargs.get("period")

        for series in (highs, lows, closes, volumes):
            if not isinstance(series, list) or len(series) == 0:
                raise ValueError("series must be non-empty lists")
        if not (len(highs) == len(lows) == len(closes) == len(volumes)):
            raise ValueError("series must align")
        if not isinstance(period, int) or period <= 0:
            raise ValueError("period must be positive integer")
        if period > len(highs):
            raise ValueError("period cannot exceed number of data points")

        money_flow_volumes = []
        volume_values = []
        for h, l, c, v in zip(highs, lows, closes, volumes):
            if not isinstance(h, (int, float)) or not isinstance(l, (int, float)) or not isinstance(c, (int, float)) or not isinstance(v, (int, float)):
                raise TypeError("price and volume inputs must be numeric")
            if h == l:
                multiplier = 0.0
            else:
                multiplier = (((c - l) - (h - c)) / (h - l))
            money_flow_volumes.append(multiplier * float(v))
            volume_values.append(float(v))

        cmf_series = []
        for idx in range(len(money_flow_volumes)):
            if idx + 1 < period:
                cmf_series.append(math.nan)
                continue
            flow_sum = sum(money_flow_volumes[idx - period + 1:idx + 1])
            volume_sum = sum(volume_values[idx - period + 1:idx + 1])
            cmf_series.append(flow_sum / volume_sum if volume_sum != 0 else math.nan)

        current_cmf = cmf_series[-1]
        if math.isnan(current_cmf):
            raise ValueError("insufficient data for CMF")
        if current_cmf > 0:
            pressure = "buying"
            signal = "accumulation"
        elif current_cmf < 0:
            pressure = "selling"
            signal = "distribution"
        else:
            pressure = "neutral"
            signal = "neutral"

        return {
            "status": "success",
            "data": {
                "cmf_series": cmf_series,
                "current_cmf": current_cmf,
                "buying_selling_pressure": pressure,
                "signal": signal
            },
            "timestamp": datetime.now(timezone.utc).isoformat()
        }
    except (ValueError, TypeError, ZeroDivisionError) as e:
        logger.error(f"chaikin_money_flow failed: {e}")
        _log_lesson(f"chaikin_money_flow: {e}")
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
