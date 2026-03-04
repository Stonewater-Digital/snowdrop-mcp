"""Calculate the Commodity Channel Index (CCI).

MCP Tool Name: commodity_channel_index_calculator
"""
from __future__ import annotations
from datetime import datetime, timezone
from typing import Any

TOOL_META: dict[str, Any] = {
    "name": "commodity_channel_index_calculator",
    "description": "Calculate the Commodity Channel Index (CCI), an oscillator measuring deviation from the statistical mean. Values above +100 suggest overbought; below -100 suggest oversold.",
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
                "description": "CCI lookback period.",
                "default": 20,
            },
        },
        "required": ["highs", "lows", "closes"],
    },
}


def commodity_channel_index_calculator(
    highs: list[float],
    lows: list[float],
    closes: list[float],
    period: int = 20,
) -> dict[str, Any]:
    """Calculate the Commodity Channel Index."""
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

        # Typical price
        tp = [(h + l + c) / 3 for h, l, c in zip(highs, lows, closes)]

        cci_values: list[float] = []
        for i in range(period - 1, n):
            window = tp[i - period + 1 : i + 1]
            sma = sum(window) / period
            mean_deviation = sum(abs(x - sma) for x in window) / period

            if mean_deviation == 0:
                cci_values.append(0.0)
            else:
                cci = (tp[i] - sma) / (0.015 * mean_deviation)
                cci_values.append(round(cci, 4))

        latest_cci = cci_values[-1] if cci_values else None

        signal = "neutral"
        if latest_cci is not None:
            if latest_cci > 200:
                signal = "Extremely overbought"
            elif latest_cci > 100:
                signal = "Overbought — potential reversal or strong uptrend"
            elif latest_cci > -100:
                signal = "Neutral range"
            elif latest_cci > -200:
                signal = "Oversold — potential reversal or strong downtrend"
            else:
                signal = "Extremely oversold"

        return {
            "status": "ok",
            "data": {
                "period": period,
                "latest_cci": latest_cci,
                "signal": signal,
                "cci_values": cci_values[-period:],
                "note": "CCI measures deviation from average. +100/-100 are traditional overbought/oversold thresholds. Constant 0.015 ensures ~75% of values fall between -100 and +100.",
            },
            "timestamp": datetime.now(timezone.utc).isoformat(),
        }
    except Exception as exc:
        return {
            "status": "error",
            "data": {"error": str(exc)},
            "timestamp": datetime.now(timezone.utc).isoformat(),
        }
