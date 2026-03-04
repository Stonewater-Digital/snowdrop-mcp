"""Calculate Williams %R oscillator.

MCP Tool Name: williams_percent_r_calculator
"""
from __future__ import annotations
from datetime import datetime, timezone
from typing import Any

TOOL_META: dict[str, Any] = {
    "name": "williams_percent_r_calculator",
    "description": "Calculate Williams %R, a momentum oscillator ranging from -100 to 0. Readings above -20 are overbought; below -80 are oversold.",
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
                "description": "Lookback period.",
                "default": 14,
            },
        },
        "required": ["highs", "lows", "closes"],
    },
}


def williams_percent_r_calculator(
    highs: list[float],
    lows: list[float],
    closes: list[float],
    period: int = 14,
) -> dict[str, Any]:
    """Calculate Williams %R oscillator."""
    try:
        n = len(highs)
        if n != len(lows) or n != len(closes):
            return {
                "status": "error",
                "data": {"error": "Highs, lows, and closes arrays must be the same length."},
                "timestamp": datetime.now(timezone.utc).isoformat(),
            }
        if n < period:
            return {
                "status": "error",
                "data": {"error": f"Need at least {period} data points, got {n}."},
                "timestamp": datetime.now(timezone.utc).isoformat(),
            }

        wr_values: list[float] = []
        for i in range(period - 1, n):
            highest_high = max(highs[i - period + 1 : i + 1])
            lowest_low = min(lows[i - period + 1 : i + 1])

            if highest_high == lowest_low:
                wr_values.append(0.0)
            else:
                wr = -100 * (highest_high - closes[i]) / (highest_high - lowest_low)
                wr_values.append(round(wr, 4))

        latest_wr = wr_values[-1] if wr_values else None

        signal = "neutral"
        if latest_wr is not None:
            if latest_wr > -20:
                signal = "Overbought (above -20)"
            elif latest_wr < -80:
                signal = "Oversold (below -80)"
            else:
                signal = "Neutral range"

        return {
            "status": "ok",
            "data": {
                "period": period,
                "latest_williams_r": latest_wr,
                "signal": signal,
                "williams_r_values": wr_values[-period:],
                "note": "Williams %R ranges from -100 to 0. Above -20 = overbought, below -80 = oversold. Similar to stochastic oscillator but inverted.",
            },
            "timestamp": datetime.now(timezone.utc).isoformat(),
        }
    except Exception as exc:
        return {
            "status": "error",
            "data": {"error": str(exc)},
            "timestamp": datetime.now(timezone.utc).isoformat(),
        }
