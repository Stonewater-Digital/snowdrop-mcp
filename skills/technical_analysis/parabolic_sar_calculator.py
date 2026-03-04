"""Calculate the Parabolic SAR (Stop and Reverse) indicator.

MCP Tool Name: parabolic_sar_calculator
"""
from __future__ import annotations
from datetime import datetime, timezone
from typing import Any

TOOL_META: dict[str, Any] = {
    "name": "parabolic_sar_calculator",
    "description": "Calculate the Parabolic SAR (Stop and Reverse) indicator. Used for trailing stop placement and trend direction identification.",
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
            "af_start": {
                "type": "number",
                "description": "Initial acceleration factor.",
                "default": 0.02,
            },
            "af_max": {
                "type": "number",
                "description": "Maximum acceleration factor.",
                "default": 0.20,
            },
        },
        "required": ["highs", "lows"],
    },
}


def parabolic_sar_calculator(
    highs: list[float],
    lows: list[float],
    af_start: float = 0.02,
    af_max: float = 0.20,
) -> dict[str, Any]:
    """Calculate the Parabolic SAR indicator."""
    try:
        n = len(highs)
        if n != len(lows):
            return {
                "status": "error",
                "data": {"error": "Highs and lows arrays must be the same length."},
                "timestamp": datetime.now(timezone.utc).isoformat(),
            }
        if n < 3:
            return {
                "status": "error",
                "data": {"error": f"Need at least 3 data points, got {n}."},
                "timestamp": datetime.now(timezone.utc).isoformat(),
            }

        sar_values: list[float] = [0.0] * n
        trend: list[int] = [0] * n  # 1 = uptrend, -1 = downtrend

        # Initialize: assume uptrend if second high > first high
        is_uptrend = highs[1] > highs[0]
        af = af_start
        ep = highs[0] if is_uptrend else lows[0]
        sar = lows[0] if is_uptrend else highs[0]

        sar_values[0] = round(sar, 4)
        trend[0] = 1 if is_uptrend else -1

        for i in range(1, n):
            prev_sar = sar

            if is_uptrend:
                sar = prev_sar + af * (ep - prev_sar)
                # SAR must not be above the two previous lows
                sar = min(sar, lows[i - 1])
                if i >= 2:
                    sar = min(sar, lows[i - 2])

                if lows[i] < sar:
                    # Reversal to downtrend
                    is_uptrend = False
                    sar = ep
                    ep = lows[i]
                    af = af_start
                else:
                    if highs[i] > ep:
                        ep = highs[i]
                        af = min(af + af_start, af_max)
            else:
                sar = prev_sar + af * (ep - prev_sar)
                # SAR must not be below the two previous highs
                sar = max(sar, highs[i - 1])
                if i >= 2:
                    sar = max(sar, highs[i - 2])

                if highs[i] > sar:
                    # Reversal to uptrend
                    is_uptrend = True
                    sar = ep
                    ep = highs[i]
                    af = af_start
                else:
                    if lows[i] < ep:
                        ep = lows[i]
                        af = min(af + af_start, af_max)

            sar_values[i] = round(sar, 4)
            trend[i] = 1 if is_uptrend else -1

        latest_sar = sar_values[-1]
        latest_trend = "uptrend" if trend[-1] == 1 else "downtrend"

        # Detect recent reversal
        reversal = None
        if len(trend) >= 2 and trend[-1] != trend[-2]:
            reversal = f"SAR reversal detected: switched to {latest_trend} on latest bar"

        return {
            "status": "ok",
            "data": {
                "af_start": af_start,
                "af_max": af_max,
                "latest_sar": latest_sar,
                "latest_trend": latest_trend,
                "reversal": reversal,
                "sar_values": sar_values[-20:],
                "trend_values": trend[-20:],
                "note": "Parabolic SAR dots below price = uptrend (support). Dots above price = downtrend (resistance). Reversal when price crosses SAR.",
            },
            "timestamp": datetime.now(timezone.utc).isoformat(),
        }
    except Exception as exc:
        return {
            "status": "error",
            "data": {"error": str(exc)},
            "timestamp": datetime.now(timezone.utc).isoformat(),
        }
