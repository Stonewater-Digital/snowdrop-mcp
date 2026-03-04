"""Calculate Chaikin Money Flow (CMF) indicator.

MCP Tool Name: chaikin_money_flow_calculator
"""
from __future__ import annotations
from datetime import datetime, timezone
from typing import Any

TOOL_META: dict[str, Any] = {
    "name": "chaikin_money_flow_calculator",
    "description": "Calculate Chaikin Money Flow (CMF), which measures the accumulation/distribution of money flow over a period. Positive CMF = buying pressure, negative = selling pressure.",
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
            "volumes": {
                "type": "array",
                "items": {"type": "number"},
                "description": "List of volume values (oldest to newest).",
            },
            "period": {
                "type": "integer",
                "description": "CMF lookback period.",
                "default": 20,
            },
        },
        "required": ["highs", "lows", "closes", "volumes"],
    },
}


def chaikin_money_flow_calculator(
    highs: list[float],
    lows: list[float],
    closes: list[float],
    volumes: list[float],
    period: int = 20,
) -> dict[str, Any]:
    """Calculate Chaikin Money Flow indicator."""
    try:
        n = len(highs)
        if not (n == len(lows) == len(closes) == len(volumes)):
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

        # Money Flow Multiplier: ((C - L) - (H - C)) / (H - L)
        # Money Flow Volume: MFM * Volume
        mfv: list[float] = []
        for i in range(n):
            hl_range = highs[i] - lows[i]
            if hl_range == 0:
                mfv.append(0.0)
            else:
                mfm = ((closes[i] - lows[i]) - (highs[i] - closes[i])) / hl_range
                mfv.append(mfm * volumes[i])

        # CMF = sum(MFV, period) / sum(Volume, period)
        cmf_values: list[float] = []
        for i in range(period - 1, n):
            sum_mfv = sum(mfv[i - period + 1 : i + 1])
            sum_vol = sum(volumes[i - period + 1 : i + 1])
            if sum_vol == 0:
                cmf_values.append(0.0)
            else:
                cmf_values.append(round(sum_mfv / sum_vol, 6))

        latest_cmf = cmf_values[-1] if cmf_values else None

        signal = "neutral"
        if latest_cmf is not None:
            if latest_cmf > 0.25:
                signal = "Strong buying pressure"
            elif latest_cmf > 0.05:
                signal = "Moderate buying pressure"
            elif latest_cmf > -0.05:
                signal = "Neutral — no clear money flow bias"
            elif latest_cmf > -0.25:
                signal = "Moderate selling pressure"
            else:
                signal = "Strong selling pressure"

        return {
            "status": "ok",
            "data": {
                "period": period,
                "latest_cmf": latest_cmf,
                "signal": signal,
                "cmf_values": cmf_values[-period:],
                "note": "CMF ranges from -1 to +1. Positive = accumulation (buying). Negative = distribution (selling). Zero line crossovers are significant.",
            },
            "timestamp": datetime.now(timezone.utc).isoformat(),
        }
    except Exception as exc:
        return {
            "status": "error",
            "data": {"error": str(exc)},
            "timestamp": datetime.now(timezone.utc).isoformat(),
        }
