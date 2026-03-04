"""Calculate Keltner Channels using EMA and Average True Range.

MCP Tool Name: keltner_channel_calculator
"""
from __future__ import annotations
from datetime import datetime, timezone
from typing import Any

TOOL_META: dict[str, Any] = {
    "name": "keltner_channel_calculator",
    "description": "Calculate Keltner Channels (middle EMA band with ATR-based upper/lower channels). Used for trend direction and volatility-based breakouts.",
    "inputSchema": {
        "type": "object",
        "properties": {
            "prices": {
                "type": "array",
                "items": {"type": "number"},
                "description": "List of closing prices (oldest to newest).",
            },
            "period": {
                "type": "integer",
                "description": "EMA and ATR lookback period.",
                "default": 20,
            },
            "atr_multiplier": {
                "type": "number",
                "description": "Multiplier for ATR to set channel width.",
                "default": 2.0,
            },
        },
        "required": ["prices"],
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


def keltner_channel_calculator(
    prices: list[float],
    period: int = 20,
    atr_multiplier: float = 2.0,
) -> dict[str, Any]:
    """Calculate Keltner Channels."""
    try:
        if len(prices) < period + 1:
            return {
                "status": "error",
                "data": {"error": f"Need at least {period + 1} prices, got {len(prices)}."},
                "timestamp": datetime.now(timezone.utc).isoformat(),
            }

        # Calculate true range (using close-to-close as proxy since we only have closes)
        true_ranges = [abs(prices[i] - prices[i - 1]) for i in range(1, len(prices))]
        # Prepend a zero for index alignment
        true_ranges.insert(0, abs(prices[1] - prices[0]) if len(prices) > 1 else 0)

        # EMA of prices (middle band)
        middle = _ema(prices, period)

        # ATR = EMA of true ranges
        atr_values = _ema(true_ranges, period)

        # Build channels
        upper = [round(m + atr_multiplier * a, 4) for m, a in zip(middle, atr_values)]
        lower = [round(m - atr_multiplier * a, 4) for m, a in zip(middle, atr_values)]
        middle_rounded = [round(m, 4) for m in middle]

        latest_price = prices[-1]
        latest_upper = upper[-1]
        latest_lower = lower[-1]
        latest_middle = middle_rounded[-1]

        if latest_price > latest_upper:
            signal = "Price above upper channel — strong uptrend or breakout"
        elif latest_price < latest_lower:
            signal = "Price below lower channel — strong downtrend or breakdown"
        elif latest_price > latest_middle:
            signal = "Price above middle band — mild bullish bias"
        else:
            signal = "Price below middle band — mild bearish bias"

        return {
            "status": "ok",
            "data": {
                "period": period,
                "atr_multiplier": atr_multiplier,
                "latest_upper": latest_upper,
                "latest_middle": latest_middle,
                "latest_lower": latest_lower,
                "latest_price": latest_price,
                "signal": signal,
                "upper_channel": upper[-period:],
                "middle_channel": middle_rounded[-period:],
                "lower_channel": lower[-period:],
            },
            "timestamp": datetime.now(timezone.utc).isoformat(),
        }
    except Exception as exc:
        return {
            "status": "error",
            "data": {"error": str(exc)},
            "timestamp": datetime.now(timezone.utc).isoformat(),
        }
