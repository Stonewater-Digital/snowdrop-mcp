"""
Execuve Summary: Calculates Elder's Force Index combining price change and volume.
Inputs: closes (list[float]), volumes (list[float]), ema_period (int)
Outputs: force_index_series (list[float]), current_value (float), signal (str), zero_line_crossover (str)
MCP Tool Name: force_index
"""
import logging
import math
from datetime import datetime, timezone
from typing import Any

logger = logging.getLogger("snowdrop.skills")

TOOL_META = {
    "name": "force_index",
    "description": "Applies Elder's Force Index with optional EMA smoothing to detect bullish or bearish thrusts.",
    "inputSchema": {
        "type": "object",
        "properties": {
            "closes": {"type": "array", "description": "Close prices."},
            "volumes": {"type": "array", "description": "Volume per bar."},
            "ema_period": {"type": "integer", "description": "EMA smoothing period (default 13)."}
        },
        "required": ["closes", "volumes", "ema_period"]
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


def force_index(**kwargs: Any) -> dict:
    """Computes (Close_t - Close_{t-1}) * Volume_t and smooths with EMA."""
    try:
        closes = kwargs.get("closes")
        volumes = kwargs.get("volumes")
        ema_period = kwargs.get("ema_period")

        if not isinstance(closes, list) or not isinstance(volumes, list) or len(closes) != len(volumes):
            raise ValueError("closes and volumes must be equal-length lists")
        if len(closes) < 2:
            raise ValueError("need at least two closes for Force Index")
        if not isinstance(ema_period, int) or ema_period <= 1:
            raise ValueError("ema_period must be > 1")

        raw_force = [math.nan]
        for idx in range(1, len(closes)):
            c = closes[idx]
            p = closes[idx - 1]
            v = volumes[idx]
            if not isinstance(c, (int, float)) or not isinstance(p, (int, float)) or not isinstance(v, (int, float)):
                raise TypeError("inputs must be numeric")
            raw_force.append((float(c) - float(p)) * float(v))

        force_index_series = _ema(raw_force, ema_period)
        current_value = force_index_series[-1]
        if math.isnan(current_value):
            raise ValueError("insufficient data for Force Index")

        signal = "bullish" if current_value > 0 else ("bearish" if current_value < 0 else "neutral")
        prev_value = next((value for value in reversed(force_index_series[:-1]) if not math.isnan(value)), 0.0)
        if current_value > 0 >= prev_value:
            zero_cross = "bullish_cross"
        elif current_value < 0 <= prev_value:
            zero_cross = "bearish_cross"
        else:
            zero_cross = "none"

        return {
            "status": "success",
            "data": {
                "force_index_series": force_index_series,
                "current_value": current_value,
                "signal": signal,
                "zero_line_crossover": zero_cross
            },
            "timestamp": datetime.now(timezone.utc).isoformat()
        }
    except (ValueError, TypeError, ZeroDivisionError) as e:
        logger.error(f"force_index failed: {e}")
        _log_lesson(f"force_index: {e}")
        return {
            "status": "error",
            "error": str(e),
            "timestamp": datetime.now(timezone.utc).isoformat()
        }


def _ema(values: list[float], period: int) -> list[float]:
    ema = [math.nan] * len(values)
    valid_values = [value for value in values if not math.isnan(value)]
    if len(valid_values) < period:
        return ema
    alpha = 2 / (period + 1)
    # find index of first valid value to start
    first_valid_index = values.index(valid_values[0])
    seed_values = valid_values[:period]
    seed_avg = sum(seed_values) / period
    ema[first_valid_index + period - 1] = seed_avg
    prev = seed_avg
    idx_pointer = first_valid_index + period
    valid_pointer = period
    while idx_pointer < len(values):
        value = values[idx_pointer]
        if math.isnan(value):
            idx_pointer += 1
            continue
        prev = alpha * value + (1 - alpha) * prev
        ema[idx_pointer] = prev
        idx_pointer += 1
        valid_pointer += 1
    return ema


def _log_lesson(message: str) -> None:
    try:
        with open("logs/lessons.md", "a") as f:
            f.write(f"- [{datetime.now(timezone.utc).isoformat()}] {message}\n")
    except OSError:
        pass
