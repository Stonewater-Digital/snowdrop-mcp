"""
Execuve Summary: Calculates the Mass Index to spot potential reversals via range bulges.
Inputs: highs (list[float]), lows (list[float]), ema_period (int), sum_period (int)
Outputs: mass_index_series (list[float]), current_value (float), reversal_bulge_detected (bool), setup_signal (str)
MCP Tool Name: mass_index
"""
import logging
import math
from datetime import datetime, timezone
from typing import Any

logger = logging.getLogger("snowdrop.skills")

TOOL_META = {
    "name": "mass_index",
    "description": "Implements Donald Dorsey's Mass Index using double EMA of high-low range.",
    "inputSchema": {
        "type": "object",
        "properties": {
            "highs": {"type": "array", "description": "High price series."},
            "lows": {"type": "array", "description": "Low price series."},
            "ema_period": {"type": "integer", "description": "EMA period (default 9)."},
            "sum_period": {"type": "integer", "description": "Summation period for bulge detection (default 25)."}
        },
        "required": ["highs", "lows", "ema_period", "sum_period"]
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


def mass_index(**kwargs: Any) -> dict:
    """Calculates EMA of the daily range, applies a second EMA, and sums the ratio to detect bulges."""
    try:
        highs = kwargs.get("highs")
        lows = kwargs.get("lows")
        ema_period = kwargs.get("ema_period")
        sum_period = kwargs.get("sum_period")

        for series in (highs, lows):
            if not isinstance(series, list) or len(series) < 2:
                raise ValueError("highs and lows must be lists")
        if len(highs) != len(lows):
            raise ValueError("highs and lows must align")
        for label, value in (("ema_period", ema_period), ("sum_period", sum_period)):
            if not isinstance(value, int) or value <= 1:
                raise ValueError(f"{label} must be integer > 1")

        ranges = []
        for h, l in zip(highs, lows):
            if not isinstance(h, (int, float)) or not isinstance(l, (int, float)):
                raise TypeError("price inputs must be numeric")
            ranges.append(float(h) - float(l))

        ema1 = _ema(ranges, ema_period)
        ema2 = _ema(ema1, ema_period)
        ratio = []
        for first, second in zip(ema1, ema2):
            if math.isnan(first) or math.isnan(second) or second == 0:
                ratio.append(math.nan)
            else:
                ratio.append(first / second)

        mass_index_series = []
        window: list[float] = []
        for value in ratio:
            if math.isnan(value):
                mass_index_series.append(math.nan)
                continue
            window.append(value)
            if len(window) > sum_period:
                window.pop(0)
            if len(window) == sum_period:
                mass_index_series.append(sum(window))
            else:
                mass_index_series.append(math.nan)

        current_value = mass_index_series[-1]
        if math.isnan(current_value):
            raise ValueError("insufficient data for Mass Index")
        reversal_bulge = current_value > 27
        setup_signal = "waiting"
        past_values = [value for value in mass_index_series if not math.isnan(value)]
        if len(past_values) >= 2:
            if reversal_bulge and past_values[-2] is not None and past_values[-2] <= 27:
                setup_signal = "bulge_trigger"
            elif past_values[-1] < 26.5 and any(value > 27 for value in past_values[-min(sum_period, len(past_values)):]):
                setup_signal = "reversal_watch"

        return {
            "status": "success",
            "data": {
                "mass_index_series": mass_index_series,
                "current_value": current_value,
                "reversal_bulge_detected": reversal_bulge,
                "setup_signal": setup_signal
            },
            "timestamp": datetime.now(timezone.utc).isoformat()
        }
    except (ValueError, TypeError, ZeroDivisionError) as e:
        logger.error(f"mass_index failed: {e}")
        _log_lesson(f"mass_index: {e}")
        return {
            "status": "error",
            "error": str(e),
            "timestamp": datetime.now(timezone.utc).isoformat()
        }


def _ema(values: list[float], period: int) -> list[float]:
    ema = [math.nan] * len(values)
    if len(values) < period:
        return ema
    alpha = 2 / (period + 1)
    # Skip leading NaN values to find valid seed window
    valid_count = 0
    start_idx = 0
    for i, v in enumerate(values):
        if math.isnan(v):
            valid_count = 0
            start_idx = i + 1
        else:
            valid_count += 1
            if valid_count == period:
                seed = sum(values[start_idx:i + 1]) / period
                ema[i] = seed
                prev = seed
                for idx in range(i + 1, len(values)):
                    if math.isnan(values[idx]):
                        break
                    prev = alpha * values[idx] + (1 - alpha) * prev
                    ema[idx] = prev
                return ema
    return ema


def _log_lesson(message: str) -> None:
    try:
        with open("logs/lessons.md", "a") as f:
            f.write(f"- [{datetime.now(timezone.utc).isoformat()}] {message}\n")
    except OSError:
        pass
