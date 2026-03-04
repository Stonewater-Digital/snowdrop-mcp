"""
Execuve Summary: Computes the McClellan Oscillator and Summation Index from advance/decline data.
Inputs: advances (list[int]), declines (list[int])
Outputs: mcclellan_oscillator (float), summation_index (list[float]), signal (str), overbought_oversold (str)
MCP Tool Name: mcclellan_oscillator
"""
import logging
import math
from datetime import datetime, timezone
from typing import Any

logger = logging.getLogger("snowdrop.skills")

TOOL_META = {
    "name": "mcclellan_oscillator",
    "description": "Calculates McClellan Oscillator (EMA19-EMA39) and the Summation Index to gauge breadth thrusts.",
    "inputSchema": {
        "type": "object",
        "properties": {
            "advances": {"type": "array", "description": "Advancing issues."},
            "declines": {"type": "array", "description": "Declining issues."}
        },
        "required": ["advances", "declines"]
    },
    "outputSchema": {
        "type": "object", "properties": {"status": {"type": "string"}, "timestamp": {"type": "string"}, "data": {"type": "object"}}, "required": ["status", "timestamp"]
    }
}


def mcclellan_oscillator(**kwargs: Any) -> dict:
    """Generates McClellan Oscillator and Summation Index."""
    try:
        advances = kwargs.get("advances")
        declines = kwargs.get("declines")
        if not isinstance(advances, list) or not isinstance(declines, list) or len(advances) != len(declines):
            raise ValueError("advances/declines must be equal-length lists")
        net = [float(a) - float(d) for a, d in zip(advances, declines)]
        ema19 = _ema(net, 19)
        ema39 = _ema(net, 39)
        oscillator_series = []
        for fast, slow in zip(ema19, ema39):
            if math.isnan(fast) or math.isnan(slow):
                oscillator_series.append(math.nan)
            else:
                oscillator_series.append(fast - slow)
        current_osc = oscillator_series[-1]
        summation_index = []
        cumulative = 0.0
        for value in oscillator_series:
            if math.isnan(value):
                summation_index.append(math.nan)
            else:
                cumulative += value
                summation_index.append(cumulative)
        signal = "bullish" if current_osc > 0 else ("bearish" if current_osc < 0 else "neutral")
        overbought = "neutral"
        if current_osc > 100:
            overbought = "overbought"
        elif current_osc < -100:
            overbought = "oversold"

        return {
            "status": "success",
            "data": {
                "mcclellan_oscillator": current_osc,
                "summation_index": summation_index,
                "signal": signal,
                "overbought_oversold": overbought
            },
            "timestamp": datetime.now(timezone.utc).isoformat()
        }
    except (ValueError, TypeError, ZeroDivisionError) as e:
        logger.error(f"mcclellan_oscillator failed: {e}")
        _log_lesson(f"mcclellan_oscillator: {e}")
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
    seed = sum(values[:period]) / period
    ema[period - 1] = seed
    prev = seed
    for idx in range(period, len(values)):
        prev = alpha * values[idx] + (1 - alpha) * prev
        ema[idx] = prev
    return ema


def _log_lesson(message: str) -> None:
    try:
        with open("logs/lessons.md", "a") as f:
            f.write(f"- [{datetime.now(timezone.utc).isoformat()}] {message}\n")
    except OSError:
        pass
