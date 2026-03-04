"""Calculate the TRIX (Triple Exponential Average) indicator.

MCP Tool Name: trix_indicator_calculator
"""
from __future__ import annotations
from datetime import datetime, timezone
from typing import Any

TOOL_META: dict[str, Any] = {
    "name": "trix_indicator_calculator",
    "description": "Calculate the TRIX indicator, a momentum oscillator based on the rate of change of a triple-smoothed EMA. Filters out insignificant price movements.",
    "inputSchema": {
        "type": "object",
        "properties": {
            "closes": {
                "type": "array",
                "items": {"type": "number"},
                "description": "List of closing prices (oldest to newest).",
            },
            "period": {
                "type": "integer",
                "description": "EMA period for each of the three smoothings.",
                "default": 15,
            },
        },
        "required": ["closes"],
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


def trix_indicator_calculator(
    closes: list[float],
    period: int = 15,
) -> dict[str, Any]:
    """Calculate the TRIX indicator."""
    try:
        if len(closes) < period * 3 + 1:
            return {
                "status": "error",
                "data": {"error": f"Need at least {period * 3 + 1} data points, got {len(closes)}."},
                "timestamp": datetime.now(timezone.utc).isoformat(),
            }

        # Triple EMA
        ema1 = _ema(closes, period)
        ema2 = _ema(ema1, period)
        ema3 = _ema(ema2, period)

        # TRIX = percent change of triple EMA
        trix_values: list[float] = []
        for i in range(1, len(ema3)):
            if ema3[i - 1] == 0:
                trix_values.append(0.0)
            else:
                trix = (ema3[i] - ema3[i - 1]) / ema3[i - 1] * 100
                trix_values.append(round(trix, 6))

        latest_trix = trix_values[-1] if trix_values else None

        signal = "neutral"
        if latest_trix is not None:
            if latest_trix > 0:
                signal = "Bullish — TRIX above zero line"
            elif latest_trix < 0:
                signal = "Bearish — TRIX below zero line"

        # Zero-line crossover
        crossover = None
        if len(trix_values) >= 2:
            if trix_values[-2] < 0 and trix_values[-1] > 0:
                crossover = "Bullish crossover — TRIX crossed above zero"
            elif trix_values[-2] > 0 and trix_values[-1] < 0:
                crossover = "Bearish crossover — TRIX crossed below zero"

        return {
            "status": "ok",
            "data": {
                "period": period,
                "latest_trix": latest_trix,
                "signal": signal,
                "crossover": crossover,
                "trix_values": trix_values[-period:],
                "note": "TRIX is the 1-period percent change of a triple-smoothed EMA. "
                "The triple smoothing filters noise. Positive = uptrend, negative = downtrend. "
                "Zero-line crossovers and signal line crossovers generate trade signals.",
            },
            "timestamp": datetime.now(timezone.utc).isoformat(),
        }
    except Exception as exc:
        return {
            "status": "error",
            "data": {"error": str(exc)},
            "timestamp": datetime.now(timezone.utc).isoformat(),
        }
