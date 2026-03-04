"""Calculate Donchian Channels from high/low price data.

MCP Tool Name: donchian_channel_calculator
"""
from __future__ import annotations
from datetime import datetime, timezone
from typing import Any

TOOL_META: dict[str, Any] = {
    "name": "donchian_channel_calculator",
    "description": "Calculate Donchian Channels (highest high and lowest low over a lookback period). Used for breakout trading systems.",
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
            "period": {
                "type": "integer",
                "description": "Lookback period for the channel.",
                "default": 20,
            },
        },
        "required": ["highs", "lows"],
    },
}


def donchian_channel_calculator(
    highs: list[float],
    lows: list[float],
    period: int = 20,
) -> dict[str, Any]:
    """Calculate Donchian Channels."""
    try:
        if len(highs) != len(lows):
            return {
                "status": "error",
                "data": {"error": "Highs and lows arrays must be the same length."},
                "timestamp": datetime.now(timezone.utc).isoformat(),
            }
        if len(highs) < period:
            return {
                "status": "error",
                "data": {"error": f"Need at least {period} data points, got {len(highs)}."},
                "timestamp": datetime.now(timezone.utc).isoformat(),
            }

        upper_channel: list[float] = []
        lower_channel: list[float] = []
        middle_channel: list[float] = []

        for i in range(period - 1, len(highs)):
            window_highs = highs[i - period + 1 : i + 1]
            window_lows = lows[i - period + 1 : i + 1]
            upper = max(window_highs)
            lower = min(window_lows)
            middle = (upper + lower) / 2
            upper_channel.append(round(upper, 4))
            lower_channel.append(round(lower, 4))
            middle_channel.append(round(middle, 4))

        latest_upper = upper_channel[-1]
        latest_lower = lower_channel[-1]
        latest_middle = middle_channel[-1]
        channel_width = round(latest_upper - latest_lower, 4)

        return {
            "status": "ok",
            "data": {
                "period": period,
                "latest_upper": latest_upper,
                "latest_middle": latest_middle,
                "latest_lower": latest_lower,
                "channel_width": channel_width,
                "upper_channel": upper_channel[-period:],
                "middle_channel": middle_channel[-period:],
                "lower_channel": lower_channel[-period:],
                "note": "Donchian Channels mark the highest high and lowest low over the lookback period. "
                "Breakout above upper = bullish signal. Breakdown below lower = bearish signal.",
            },
            "timestamp": datetime.now(timezone.utc).isoformat(),
        }
    except Exception as exc:
        return {
            "status": "error",
            "data": {"error": str(exc)},
            "timestamp": datetime.now(timezone.utc).isoformat(),
        }
