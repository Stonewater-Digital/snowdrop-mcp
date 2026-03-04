"""Calculate the Force Index indicator.

MCP Tool Name: force_index_calculator
"""
from __future__ import annotations
from datetime import datetime, timezone
from typing import Any

TOOL_META: dict[str, Any] = {
    "name": "force_index_calculator",
    "description": "Calculate the Force Index, which combines price change and volume to measure the strength of bulls and bears. Uses EMA smoothing.",
    "inputSchema": {
        "type": "object",
        "properties": {
            "closes": {
                "type": "array",
                "items": {"type": "number"},
                "description": "List of closing prices (oldest to newest).",
            },
            "volumes": {
                "type": "array",
                "items": {"type": "number"},
                "description": "List of volume values (oldest to newest).",
            },
            "period": {
                "type": "integer",
                "description": "EMA smoothing period for the Force Index.",
                "default": 13,
            },
        },
        "required": ["closes", "volumes"],
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


def force_index_calculator(
    closes: list[float],
    volumes: list[float],
    period: int = 13,
) -> dict[str, Any]:
    """Calculate the Force Index indicator."""
    try:
        n = len(closes)
        if n != len(volumes):
            return {
                "status": "error",
                "data": {"error": "Closes and volumes arrays must be the same length."},
                "timestamp": datetime.now(timezone.utc).isoformat(),
            }
        if n < period + 1:
            return {
                "status": "error",
                "data": {"error": f"Need at least {period + 1} data points, got {n}."},
                "timestamp": datetime.now(timezone.utc).isoformat(),
            }

        # Raw Force Index: (Close - Previous Close) * Volume
        raw_fi: list[float] = []
        for i in range(1, n):
            raw_fi.append((closes[i] - closes[i - 1]) * volumes[i])

        # EMA-smoothed Force Index
        smoothed = _ema(raw_fi, period)

        latest_fi = round(smoothed[-1], 2) if smoothed else None

        signal = "neutral"
        if latest_fi is not None:
            if latest_fi > 0:
                signal = "Bullish — buying force dominates"
            elif latest_fi < 0:
                signal = "Bearish — selling force dominates"
            else:
                signal = "Neutral — balanced forces"

        # Check for zero-line crossover
        crossover = None
        if len(smoothed) >= 2:
            if smoothed[-2] < 0 and smoothed[-1] > 0:
                crossover = "Bullish crossover — Force Index crossed above zero"
            elif smoothed[-2] > 0 and smoothed[-1] < 0:
                crossover = "Bearish crossover — Force Index crossed below zero"

        return {
            "status": "ok",
            "data": {
                "period": period,
                "latest_force_index": latest_fi,
                "signal": signal,
                "crossover": crossover,
                "force_index_values": [round(v, 2) for v in smoothed[-period:]],
                "note": "Force Index = (Close - Prev Close) * Volume, smoothed with EMA. "
                "Positive = buying pressure. Negative = selling pressure. Zero-line crossovers signal trend changes.",
            },
            "timestamp": datetime.now(timezone.utc).isoformat(),
        }
    except Exception as exc:
        return {
            "status": "error",
            "data": {"error": str(exc)},
            "timestamp": datetime.now(timezone.utc).isoformat(),
        }
