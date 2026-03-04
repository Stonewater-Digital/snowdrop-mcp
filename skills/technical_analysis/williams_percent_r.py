"""
Execuve Summary: Evaluates Williams %R to detect overbought/oversold swings.
Inputs: highs (list[float]), lows (list[float]), closes (list[float]), period (int)
Outputs: williams_r_series (list[float]), current_value (float), zone (str), reversal_signal (str)
MCP Tool Name: williams_percent_r
"""
import logging
import math
from datetime import datetime, timezone
from typing import Any

logger = logging.getLogger("snowdrop.skills")

TOOL_META = {
    "name": "williams_percent_r",
    "description": "Calculates Larry Williams' %R oscillator comparing close versus the highest/lowest range.",
    "inputSchema": {
        "type": "object",
        "properties": {
            "highs": {"type": "array", "description": "High prices."},
            "lows": {"type": "array", "description": "Low prices."},
            "closes": {"type": "array", "description": "Close prices."},
            "period": {"type": "integer", "description": "Lookback length for %R (default 14)."}
        },
        "required": ["highs", "lows", "closes", "period"]
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


def williams_percent_r(**kwargs: Any) -> dict:
    """Computes %R by comparing current closes to the highest high and lowest low of the period."""
    try:
        highs = kwargs.get("highs")
        lows = kwargs.get("lows")
        closes = kwargs.get("closes")
        period = kwargs.get("period")

        for series in (highs, lows, closes):
            if not isinstance(series, list) or len(series) < 2:
                raise ValueError("price series must be lists")
        if not (len(highs) == len(lows) == len(closes)):
            raise ValueError("highs, lows, and closes must align")
        if not isinstance(period, int) or period <= 1:
            raise ValueError("period must be > 1")
        if period > len(highs):
            raise ValueError("period cannot exceed number of data points")

        highs_f = []
        lows_f = []
        closes_f = []
        for h, l, c in zip(highs, lows, closes):
            if not isinstance(h, (int, float)) or not isinstance(l, (int, float)) or not isinstance(c, (int, float)):
                raise TypeError("price series must be numeric")
            highs_f.append(float(h))
            lows_f.append(float(l))
            closes_f.append(float(c))

        percent_r_series = []
        for idx in range(len(closes_f)):
            if idx + 1 < period:
                percent_r_series.append(math.nan)
                continue
            highest_high = max(highs_f[idx - period + 1: idx + 1])
            lowest_low = min(lows_f[idx - period + 1: idx + 1])
            if highest_high == lowest_low:
                percent_r = 0.0
            else:
                percent_r = -100 * ((highest_high - closes_f[idx]) / (highest_high - lowest_low))
            percent_r_series.append(percent_r)

        current_value = percent_r_series[-1]
        if math.isnan(current_value):
            raise ValueError("insufficient data for Williams %R")

        if current_value <= -80:
            zone = "oversold"
        elif current_value >= -20:
            zone = "overbought"
        else:
            zone = "neutral"

        reversal_signal = "none"
        if len(percent_r_series) >= period + 1:
            prev_value = percent_r_series[-2]
            if not math.isnan(prev_value):
                if prev_value <= -80 < current_value:
                    reversal_signal = "oversold_exit"
                elif prev_value >= -20 > current_value:
                    reversal_signal = "overbought_exit"

        return {
            "status": "success",
            "data": {
                "williams_r_series": percent_r_series,
                "current_value": current_value,
                "zone": zone,
                "reversal_signal": reversal_signal
            },
            "timestamp": datetime.now(timezone.utc).isoformat()
        }
    except (ValueError, TypeError, ZeroDivisionError) as e:
        logger.error(f"williams_percent_r failed: {e}")
        _log_lesson(f"williams_percent_r: {e}")
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
