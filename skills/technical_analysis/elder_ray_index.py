"""
Execuve Summary: Calculates Elder Ray bull and bear power relative to trend EMA.
Inputs: highs (list[float]), lows (list[float]), closes (list[float]), ema_period (int)
Outputs: bull_power (float), bear_power (float), ema_line (list[float]), signal (str), divergence (str)
MCP Tool Name: elder_ray_index
"""
import logging
import math
from datetime import datetime, timezone
from typing import Any

logger = logging.getLogger("snowdrop.skills")

TOOL_META = {
    "name": "elder_ray_index",
    "description": "Computes Elder-Ray Bull/Bear Power relative to an EMA trend baseline.",
    "inputSchema": {
        "type": "object",
        "properties": {
            "highs": {"type": "array", "description": "High prices."},
            "lows": {"type": "array", "description": "Low prices."},
            "closes": {"type": "array", "description": "Close prices."},
            "ema_period": {"type": "integer", "description": "EMA period (default 13)."}
        },
        "required": ["highs", "lows", "closes", "ema_period"]
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


def elder_ray_index(**kwargs: Any) -> dict:
    """Implements Alexander Elder's Bull/Bear Power metrics around an EMA trendline."""
    try:
        highs = kwargs.get("highs")
        lows = kwargs.get("lows")
        closes = kwargs.get("closes")
        ema_period = kwargs.get("ema_period")

        for series in (highs, lows, closes):
            if not isinstance(series, list) or len(series) < 2:
                raise ValueError("price series must be lists")
        if not (len(highs) == len(lows) == len(closes)):
            raise ValueError("series must align")
        if not isinstance(ema_period, int) or ema_period <= 1:
            raise ValueError("ema_period must be integer > 1")
        if ema_period > len(closes):
            raise ValueError("ema_period cannot exceed length")

        highs_f = []
        lows_f = []
        closes_f = []
        for h, l, c in zip(highs, lows, closes):
            if not isinstance(h, (int, float)) or not isinstance(l, (int, float)) or not isinstance(c, (int, float)):
                raise TypeError("data must be numeric")
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

        current_ema = ema_series[-1]
        if math.isnan(current_ema):
            raise ValueError("insufficient data for EMA")
        bull_power = highs_f[-1] - current_ema
        bear_power = lows_f[-1] - current_ema

        if bull_power > 0 and bear_power > 0:
            signal = "buy"
        elif bull_power < 0 and bear_power < 0:
            signal = "sell"
        else:
            signal = "neutral"

        divergence = "none"
        if len(closes_f) >= ema_period * 2:
            recent_high = max(highs_f[-ema_period:])
            prior_high = max(highs_f[-2 * ema_period:-ema_period])
            recent_bull_peak = max(high - ema for high, ema in zip(highs_f[-ema_period:], ema_series[-ema_period:]) if not math.isnan(ema))
            prior_bull_peak = max(high - ema for high, ema in zip(highs_f[-2 * ema_period:-ema_period], ema_series[-2 * ema_period:-ema_period]) if not math.isnan(ema))
            if recent_high > prior_high and recent_bull_peak < prior_bull_peak:
                divergence = "bearish"
            recent_low = min(lows_f[-ema_period:])
            prior_low = min(lows_f[-2 * ema_period:-ema_period])
            recent_bear_trough = min(low - ema for low, ema in zip(lows_f[-ema_period:], ema_series[-ema_period:]) if not math.isnan(ema))
            prior_bear_trough = min(low - ema for low, ema in zip(lows_f[-2 * ema_period:-ema_period], ema_series[-2 * ema_period:-ema_period]) if not math.isnan(ema))
            if recent_low < prior_low and recent_bear_trough > prior_bear_trough:
                divergence = "bullish"

        return {
            "status": "success",
            "data": {
                "bull_power": bull_power,
                "bear_power": bear_power,
                "ema_line": ema_series,
                "signal": signal,
                "divergence": divergence
            },
            "timestamp": datetime.now(timezone.utc).isoformat()
        }
    except (ValueError, TypeError, ZeroDivisionError) as e:
        logger.error(f"elder_ray_index failed: {e}")
        _log_lesson(f"elder_ray_index: {e}")
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
