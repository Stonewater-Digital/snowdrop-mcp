"""Calculate the Mass Index indicator for detecting trend reversals.

MCP Tool Name: mass_index_calculator
"""
from __future__ import annotations
from datetime import datetime, timezone
from typing import Any

TOOL_META: dict[str, Any] = {
    "name": "mass_index_calculator",
    "description": "Calculate the Mass Index, which uses the high-low range to identify trend reversals through 'reversal bulges'. A bulge above 27 followed by drop below 26.5 signals reversal.",
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
                "description": "Summation period for the Mass Index.",
                "default": 25,
            },
        },
        "required": ["highs", "lows"],
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


def mass_index_calculator(
    highs: list[float],
    lows: list[float],
    period: int = 25,
) -> dict[str, Any]:
    """Calculate the Mass Index indicator."""
    try:
        n = len(highs)
        if n != len(lows):
            return {
                "status": "error",
                "data": {"error": "Highs and lows arrays must be the same length."},
                "timestamp": datetime.now(timezone.utc).isoformat(),
            }
        if n < period + 20:
            return {
                "status": "error",
                "data": {"error": f"Need at least {period + 20} data points, got {n}."},
                "timestamp": datetime.now(timezone.utc).isoformat(),
            }

        # High-Low range
        hl_range = [highs[i] - lows[i] for i in range(n)]

        # Single EMA(9) of range
        ema9 = _ema(hl_range, 9)

        # Double EMA(9) of range
        double_ema9 = _ema(ema9, 9)

        # EMA ratio
        ratio: list[float] = []
        for i in range(len(double_ema9)):
            if double_ema9[i] == 0:
                ratio.append(1.0)
            else:
                ratio.append(ema9[i] / double_ema9[i])

        # Mass Index = sum of ratio over period
        mass_values: list[float] = []
        for i in range(period - 1, len(ratio)):
            mass = sum(ratio[i - period + 1 : i + 1])
            mass_values.append(round(mass, 4))

        latest_mass = mass_values[-1] if mass_values else None

        # Detect reversal bulge
        bulge_detected = False
        if len(mass_values) >= 3:
            # Check if mass went above 27 recently and then dropped below 26.5
            for i in range(len(mass_values) - 1, max(0, len(mass_values) - 10), -1):
                if mass_values[i] < 26.5:
                    for j in range(i, max(0, i - 10), -1):
                        if mass_values[j] > 27:
                            bulge_detected = True
                            break
                    break

        signal = "No reversal signal"
        if bulge_detected:
            signal = "Reversal bulge detected — Mass Index rose above 27 and fell below 26.5"
        elif latest_mass is not None and latest_mass > 27:
            signal = "Mass Index above 27 — watch for drop below 26.5 to confirm reversal bulge"

        return {
            "status": "ok",
            "data": {
                "period": period,
                "latest_mass_index": latest_mass,
                "bulge_detected": bulge_detected,
                "signal": signal,
                "mass_index_values": mass_values[-period:],
                "note": "The Mass Index identifies potential reversals by analyzing the narrowing and widening of the high-low range. "
                "A 'reversal bulge' occurs when the index rises above 27 and then drops below 26.5.",
            },
            "timestamp": datetime.now(timezone.utc).isoformat(),
        }
    except Exception as exc:
        return {
            "status": "error",
            "data": {"error": str(exc)},
            "timestamp": datetime.now(timezone.utc).isoformat(),
        }
