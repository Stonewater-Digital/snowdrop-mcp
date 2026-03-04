"""Calculate the Aroon indicator (Aroon Up and Aroon Down).

MCP Tool Name: aroon_indicator_calculator
"""
from __future__ import annotations
from datetime import datetime, timezone
from typing import Any

TOOL_META: dict[str, Any] = {
    "name": "aroon_indicator_calculator",
    "description": "Calculate the Aroon indicator (Aroon Up and Aroon Down), which identifies trend strength and direction based on the time since the highest high and lowest low.",
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
                "description": "Aroon lookback period.",
                "default": 25,
            },
        },
        "required": ["highs", "lows"],
    },
}


def aroon_indicator_calculator(
    highs: list[float],
    lows: list[float],
    period: int = 25,
) -> dict[str, Any]:
    """Calculate the Aroon indicator."""
    try:
        n = len(highs)
        if n != len(lows):
            return {
                "status": "error",
                "data": {"error": "Highs and lows arrays must be the same length."},
                "timestamp": datetime.now(timezone.utc).isoformat(),
            }
        if n < period + 1:
            return {
                "status": "error",
                "data": {"error": f"Need at least {period + 1} data points, got {n}."},
                "timestamp": datetime.now(timezone.utc).isoformat(),
            }

        aroon_up_values: list[float] = []
        aroon_down_values: list[float] = []
        aroon_osc_values: list[float] = []

        for i in range(period, n):
            window_highs = highs[i - period : i + 1]
            window_lows = lows[i - period : i + 1]

            # Days since highest high (0 = today, period = oldest)
            max_val = max(window_highs)
            days_since_high = period - window_highs.index(max_val)

            # Days since lowest low
            min_val = min(window_lows)
            days_since_low = period - window_lows.index(min_val)

            aroon_up = ((period - days_since_high) / period) * 100
            aroon_down = ((period - days_since_low) / period) * 100
            aroon_osc = aroon_up - aroon_down

            aroon_up_values.append(round(aroon_up, 2))
            aroon_down_values.append(round(aroon_down, 2))
            aroon_osc_values.append(round(aroon_osc, 2))

        latest_up = aroon_up_values[-1] if aroon_up_values else None
        latest_down = aroon_down_values[-1] if aroon_down_values else None
        latest_osc = aroon_osc_values[-1] if aroon_osc_values else None

        signal = "neutral"
        if latest_up is not None and latest_down is not None:
            if latest_up > 70 and latest_down < 30:
                signal = "Strong uptrend — Aroon Up high, Aroon Down low"
            elif latest_down > 70 and latest_up < 30:
                signal = "Strong downtrend — Aroon Down high, Aroon Up low"
            elif latest_up > 70 and latest_down > 70:
                signal = "Consolidation — both Aroon lines high (new highs and lows in range)"
            elif latest_up < 30 and latest_down < 30:
                signal = "Consolidation — both Aroon lines low (no new highs or lows)"
            elif latest_up > latest_down:
                signal = "Mild bullish bias"
            else:
                signal = "Mild bearish bias"

        return {
            "status": "ok",
            "data": {
                "period": period,
                "latest_aroon_up": latest_up,
                "latest_aroon_down": latest_down,
                "latest_aroon_oscillator": latest_osc,
                "signal": signal,
                "aroon_up": aroon_up_values[-period:],
                "aroon_down": aroon_down_values[-period:],
                "aroon_oscillator": aroon_osc_values[-period:],
                "note": "Aroon ranges 0-100. Up measures bars since highest high; Down measures bars since lowest low. "
                "Aroon Oscillator = Up - Down. Values near +100 = strong uptrend, near -100 = strong downtrend.",
            },
            "timestamp": datetime.now(timezone.utc).isoformat(),
        }
    except Exception as exc:
        return {
            "status": "error",
            "data": {"error": str(exc)},
            "timestamp": datetime.now(timezone.utc).isoformat(),
        }
