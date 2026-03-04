"""
Execuve Summary: Constructs Keltner Channels using EMA centerline and ATR envelopes.
Inputs: highs (list[float]), lows (list[float]), closes (list[float]), ema_period (int), atr_period (int), multiplier (float)
Outputs: upper_channel (float), middle_line (float), lower_channel (float), channel_width (float), price_position (str)
MCP Tool Name: keltner_channels
"""
import logging
import math
from datetime import datetime, timezone
from typing import Any

logger = logging.getLogger("snowdrop.skills")

TOOL_META = {
    "name": "keltner_channels",
    "description": "Calculates Keltner Channels: EMA midline with ATR-based upper and lower envelopes.",
    "inputSchema": {
        "type": "object",
        "properties": {
            "highs": {"type": "array", "description": "High prices."},
            "lows": {"type": "array", "description": "Low prices."},
            "closes": {"type": "array", "description": "Close prices."},
            "ema_period": {"type": "integer", "description": "EMA lookback (default 20)."},
            "atr_period": {"type": "integer", "description": "ATR lookback (default 10)."},
            "multiplier": {"type": "number", "description": "ATR multiplier (default 2)."}
        },
        "required": ["highs", "lows", "closes", "ema_period", "atr_period", "multiplier"]
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


def keltner_channels(**kwargs: Any) -> dict:
    """Applies EMA on closes and combines with ATR envelopes to form Keltner Channels."""
    try:
        highs = kwargs.get("highs")
        lows = kwargs.get("lows")
        closes = kwargs.get("closes")
        ema_period = kwargs.get("ema_period")
        atr_period = kwargs.get("atr_period")
        multiplier = kwargs.get("multiplier")

        for series in (highs, lows, closes):
            if not isinstance(series, list) or len(series) < 2:
                raise ValueError("price series must be lists")
        if not (len(highs) == len(lows) == len(closes)):
            raise ValueError("highs, lows, closes must align")
        for label, value in (("ema_period", ema_period), ("atr_period", atr_period)):
            if not isinstance(value, int) or value <= 1:
                raise ValueError(f"{label} must be integer > 1")
        if not isinstance(multiplier, (int, float)) or multiplier <= 0:
            raise ValueError("multiplier must be positive")

        highs_f = []
        lows_f = []
        closes_f = []
        for h, l, c in zip(highs, lows, closes):
            if not isinstance(h, (int, float)) or not isinstance(l, (int, float)) or not isinstance(c, (int, float)):
                raise TypeError("series must be numeric")
            highs_f.append(float(h))
            lows_f.append(float(l))
            closes_f.append(float(c))

        alpha = 2 / (ema_period + 1)
        ema_series = [math.nan] * len(closes_f)
        seed = sum(closes_f[:ema_period]) / ema_period
        ema_series[ema_period - 1] = seed
        ema_last = seed
        for idx in range(ema_period, len(closes_f)):
            ema_last = alpha * closes_f[idx] + (1 - alpha) * ema_last
            ema_series[idx] = ema_last

        tr_list = [0.0]
        for idx in range(1, len(highs_f)):
            tr = max(highs_f[idx] - lows_f[idx], abs(highs_f[idx] - closes_f[idx - 1]), abs(lows_f[idx] - closes_f[idx - 1]))
            tr_list.append(tr)

        atr_series = [math.nan] * len(tr_list)
        initial_atr = sum(tr_list[1:atr_period + 1]) / atr_period
        atr_series[atr_period] = initial_atr
        prev_atr = initial_atr
        for idx in range(atr_period + 1, len(tr_list)):
            prev_atr = (prev_atr * (atr_period - 1) + tr_list[idx]) / atr_period
            atr_series[idx] = prev_atr

        middle_line = ema_series[-1]
        current_atr = atr_series[-1]
        if math.isnan(middle_line) or math.isnan(current_atr):
            raise ValueError("insufficient data for Keltner Channels")

        upper_channel = middle_line + multiplier * current_atr
        lower_channel = middle_line - multiplier * current_atr
        channel_width = upper_channel - lower_channel
        latest_close = closes_f[-1]
        if latest_close > upper_channel:
            position = "above"
        elif latest_close < lower_channel:
            position = "below"
        else:
            position = "inside"

        return {
            "status": "success",
            "data": {
                "upper_channel": upper_channel,
                "middle_line": middle_line,
                "lower_channel": lower_channel,
                "channel_width": channel_width,
                "price_position": position
            },
            "timestamp": datetime.now(timezone.utc).isoformat()
        }
    except (ValueError, TypeError, ZeroDivisionError) as e:
        logger.error(f"keltner_channels failed: {e}")
        _log_lesson(f"keltner_channels: {e}")
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
