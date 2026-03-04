"""Calculate the Detrended Price Oscillator (DPO).

MCP Tool Name: detrended_price_oscillator_calculator
"""
from __future__ import annotations
from datetime import datetime, timezone
from typing import Any

TOOL_META: dict[str, Any] = {
    "name": "detrended_price_oscillator_calculator",
    "description": "Calculate the Detrended Price Oscillator (DPO), which removes the trend from prices to identify cycles. DPO = Close[-(period/2+1)] - SMA(period).",
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
                "description": "DPO lookback period.",
                "default": 20,
            },
        },
        "required": ["closes"],
    },
}


def detrended_price_oscillator_calculator(
    closes: list[float],
    period: int = 20,
) -> dict[str, Any]:
    """Calculate the Detrended Price Oscillator."""
    try:
        n = len(closes)
        shift = period // 2 + 1
        if n < period + shift:
            return {
                "status": "error",
                "data": {"error": f"Need at least {period + shift} data points, got {n}."},
                "timestamp": datetime.now(timezone.utc).isoformat(),
            }

        # Calculate SMA
        sma_values: list[float] = []
        for i in range(period - 1, n):
            window = closes[i - period + 1 : i + 1]
            sma_values.append(sum(window) / period)

        # DPO: Compare price from (period/2 + 1) bars ago to current SMA
        dpo_values: list[float] = []
        for i in range(len(sma_values)):
            # The SMA at index i corresponds to closes[i + period - 1]
            # DPO looks at the close that is shift bars before the end of the SMA window
            close_idx = (i + period - 1) - shift
            if close_idx >= 0:
                dpo = closes[close_idx] - sma_values[i]
                dpo_values.append(round(dpo, 4))

        latest_dpo = dpo_values[-1] if dpo_values else None

        signal = "neutral"
        if latest_dpo is not None:
            if latest_dpo > 0:
                signal = "Price above detrended average — in upper cycle phase"
            elif latest_dpo < 0:
                signal = "Price below detrended average — in lower cycle phase"

        # Detect zero-line crossover
        crossover = None
        if len(dpo_values) >= 2:
            if dpo_values[-2] < 0 and dpo_values[-1] > 0:
                crossover = "Crossed above zero — potential cycle low turning up"
            elif dpo_values[-2] > 0 and dpo_values[-1] < 0:
                crossover = "Crossed below zero — potential cycle high turning down"

        return {
            "status": "ok",
            "data": {
                "period": period,
                "shift": shift,
                "latest_dpo": latest_dpo,
                "signal": signal,
                "crossover": crossover,
                "dpo_values": dpo_values[-period:],
                "note": "DPO removes trend to reveal cycles. It is NOT a real-time indicator — "
                "it is shifted back by (period/2 + 1) bars. Best used for identifying cycle lengths and overbought/oversold cycle positions.",
            },
            "timestamp": datetime.now(timezone.utc).isoformat(),
        }
    except Exception as exc:
        return {
            "status": "error",
            "data": {"error": str(exc)},
            "timestamp": datetime.now(timezone.utc).isoformat(),
        }
