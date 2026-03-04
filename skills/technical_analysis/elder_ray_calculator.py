"""Calculate the Elder Ray Index (Bull Power and Bear Power).

MCP Tool Name: elder_ray_calculator
"""
from __future__ import annotations
from datetime import datetime, timezone
from typing import Any

TOOL_META: dict[str, Any] = {
    "name": "elder_ray_calculator",
    "description": "Calculate Elder Ray Index with Bull Power (High - EMA) and Bear Power (Low - EMA). Used to measure buying and selling pressure relative to the trend.",
    "inputSchema": {
        "type": "object",
        "properties": {
            "highs": {
                "type": "array",
                "items": {"type": "number"},
                "description": "List of high prices (oldest to newest).",
            },
            "lows": {
                "type": "array",
                "items": {"type": "number"},
                "description": "List of low prices (oldest to newest).",
            },
            "closes": {
                "type": "array",
                "items": {"type": "number"},
                "description": "List of closing prices (oldest to newest).",
            },
            "period": {
                "type": "integer",
                "description": "EMA period for the Elder Ray calculation.",
                "default": 13,
            },
        },
        "required": ["highs", "lows", "closes"],
    },
}


def _ema(values: list[float], period: int) -> list[float]:
    """Calculate exponential moving average."""
    if not values or period < 1:
        return []
    k = 2.0 / (period + 1)
    result = [values[0]]
    for i in range(1, len(values)):
        result.append(values[i] * k + result[-1] * (1 - k))
    return result


def elder_ray_calculator(
    highs: list[float],
    lows: list[float],
    closes: list[float],
    period: int = 13,
) -> dict[str, Any]:
    """Calculate the Elder Ray Index."""
    try:
        n = len(highs)
        if not (n == len(lows) == len(closes)):
            return {
                "status": "error",
                "data": {"error": "All input arrays must be the same length."},
                "timestamp": datetime.now(timezone.utc).isoformat(),
            }
        if n < period:
            return {
                "status": "error",
                "data": {"error": f"Need at least {period} data points, got {n}."},
                "timestamp": datetime.now(timezone.utc).isoformat(),
            }

        ema_values = _ema(closes, period)

        bull_power: list[float] = []
        bear_power: list[float] = []
        for i in range(n):
            bull_power.append(round(highs[i] - ema_values[i], 4))
            bear_power.append(round(lows[i] - ema_values[i], 4))

        latest_bull = bull_power[-1]
        latest_bear = bear_power[-1]
        latest_ema = round(ema_values[-1], 4)

        # Determine EMA trend
        ema_rising = ema_values[-1] > ema_values[-2] if len(ema_values) >= 2 else None

        signal = "neutral"
        if ema_rising is True and latest_bear < 0 and latest_bull > 0:
            if latest_bear > bear_power[-2] if len(bear_power) >= 2 else False:
                signal = "Buy signal — EMA rising, Bear Power negative but improving"
            else:
                signal = "Bullish — EMA rising, Bull Power positive"
        elif ema_rising is False and latest_bull > 0 and latest_bear < 0:
            if latest_bull < bull_power[-2] if len(bull_power) >= 2 else False:
                signal = "Sell signal — EMA falling, Bull Power positive but declining"
            else:
                signal = "Bearish — EMA falling, Bear Power negative"
        elif latest_bull > 0 and latest_bear > 0:
            signal = "Strong bullish — both powers positive"
        elif latest_bull < 0 and latest_bear < 0:
            signal = "Strong bearish — both powers negative"

        return {
            "status": "ok",
            "data": {
                "period": period,
                "latest_ema": latest_ema,
                "latest_bull_power": latest_bull,
                "latest_bear_power": latest_bear,
                "ema_rising": ema_rising,
                "signal": signal,
                "bull_power": bull_power[-period:],
                "bear_power": bear_power[-period:],
                "note": "Bull Power = High - EMA (measures buying strength above average). "
                "Bear Power = Low - EMA (measures selling pressure below average). "
                "Best used when EMA is rising and Bear Power is negative but improving (buy), "
                "or EMA is falling and Bull Power is positive but declining (sell).",
            },
            "timestamp": datetime.now(timezone.utc).isoformat(),
        }
    except Exception as exc:
        return {
            "status": "error",
            "data": {"error": str(exc)},
            "timestamp": datetime.now(timezone.utc).isoformat(),
        }
