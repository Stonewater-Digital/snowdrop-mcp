"""
Execuve Summary: Computes the Stochastic Oscillator to compare closes versus recent ranges.
Inputs: highs (list[float]), lows (list[float]), closes (list[float]), k_period (int), d_period (int), slowing (int)
Outputs: percent_k (float), percent_d (float), zone (str), crossover_signal (str), fast_stochastic (list[float]), slow_stochastic (list[float])
MCP Tool Name: stochastic_oscillator
"""
import logging
import math
from datetime import datetime, timezone
from typing import Any

logger = logging.getLogger("snowdrop.skills")

TOOL_META = {
    "name": "stochastic_oscillator",
    "description": "Implements George Lane's %K/%D oscillator with configurable slowing to detect momentum shifts.",
    "inputSchema": {
        "type": "object",
        "properties": {
            "highs": {"type": "array", "description": "High prices."},
            "lows": {"type": "array", "description": "Low prices."},
            "closes": {"type": "array", "description": "Close prices."},
            "k_period": {"type": "integer", "description": "Lookback period for %K (default 14)."},
            "d_period": {"type": "integer", "description": "Smoothing period for %D (default 3)."},
            "slowing": {"type": "integer", "description": "Slowing factor for %K (default 3)."}
        },
        "required": ["highs", "lows", "closes", "k_period", "d_period", "slowing"]
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


def stochastic_oscillator(**kwargs: Any) -> dict:
    """Calculates fast %K, applies slowing average, and derives %D signal line."""
    try:
        highs = kwargs.get("highs")
        lows = kwargs.get("lows")
        closes = kwargs.get("closes")
        k_period = kwargs.get("k_period")
        d_period = kwargs.get("d_period")
        slowing = kwargs.get("slowing")

        for series in (highs, lows, closes):
            if not isinstance(series, list) or len(series) < 2:
                raise ValueError("price series must be lists")
        if not (len(highs) == len(lows) == len(closes)):
            raise ValueError("highs, lows, and closes must match length")
        for label, value in (("k_period", k_period), ("d_period", d_period), ("slowing", slowing)):
            if not isinstance(value, int) or value <= 0:
                raise ValueError(f"{label} must be a positive integer")

        highs_f = []
        lows_f = []
        closes_f = []
        for idx in range(len(highs)):
            h = highs[idx]
            l = lows[idx]
            c = closes[idx]
            if not isinstance(h, (int, float)) or not isinstance(l, (int, float)) or not isinstance(c, (int, float)):
                raise TypeError("price series must contain numbers")
            highs_f.append(float(h))
            lows_f.append(float(l))
            closes_f.append(float(c))

        fast_k = []
        for idx in range(len(closes_f)):
            if idx + 1 < k_period:
                fast_k.append(math.nan)
                continue
            highest_high = max(highs_f[idx - k_period + 1: idx + 1])
            lowest_low = min(lows_f[idx - k_period + 1: idx + 1])
            if highest_high == lowest_low:
                fast_k.append(0.0)
            else:
                fast_k.append(((closes_f[idx] - lowest_low) / (highest_high - lowest_low)) * 100)

        slow_k = []
        window: list[float] = []
        for value in fast_k:
            if math.isnan(value):
                slow_k.append(math.nan)
                continue
            window.append(value)
            if len(window) > slowing:
                window.pop(0)
            slow_k.append(sum(window) / len(window))

        percent_d_series = []
        d_window: list[float] = []
        for value in slow_k:
            if math.isnan(value):
                percent_d_series.append(math.nan)
                continue
            d_window.append(value)
            if len(d_window) > d_period:
                d_window.pop(0)
            percent_d_series.append(sum(d_window) / len(d_window))

        current_k = slow_k[-1]
        current_d = percent_d_series[-1]
        if math.isnan(current_k) or math.isnan(current_d):
            raise ValueError("insufficient data for stochastic oscillator")

        if current_k >= 80 and current_d >= 80:
            zone = "overbought"
        elif current_k <= 20 and current_d <= 20:
            zone = "oversold"
        else:
            zone = "neutral"

        def _last_non_nan(values: list[float]) -> float | None:
            for value in reversed(values[:-1]):
                if not math.isnan(value):
                    return value
            return None

        prev_k = _last_non_nan(slow_k)
        prev_d = _last_non_nan(percent_d_series)
        crossover_signal = "neutral"
        if prev_k is not None and prev_d is not None:
            if current_k > current_d and prev_k <= prev_d:
                crossover_signal = "bullish_cross"
            elif current_k < current_d and prev_k >= prev_d:
                crossover_signal = "bearish_cross"

        return {
            "status": "success",
            "data": {
                "percent_k": current_k,
                "percent_d": current_d,
                "zone": zone,
                "crossover_signal": crossover_signal,
                "fast_stochastic": fast_k,
                "slow_stochastic": slow_k
            },
            "timestamp": datetime.now(timezone.utc).isoformat()
        }
    except (ValueError, TypeError, ZeroDivisionError) as e:
        logger.error(f"stochastic_oscillator failed: {e}")
        _log_lesson(f"stochastic_oscillator: {e}")
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
