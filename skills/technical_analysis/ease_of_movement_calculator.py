"""Calculate the Ease of Movement (EMV) indicator.

MCP Tool Name: ease_of_movement_calculator
"""
from __future__ import annotations
from datetime import datetime, timezone
from typing import Any

TOOL_META: dict[str, Any] = {
    "name": "ease_of_movement_calculator",
    "description": "Calculate the Ease of Movement (EMV) indicator, which relates price change to volume. Positive EMV = prices advancing on low volume; negative = declining.",
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
            "volumes": {
                "type": "array",
                "items": {"type": "number"},
                "description": "List of volume values (oldest to newest).",
            },
            "period": {
                "type": "integer",
                "description": "SMA smoothing period for EMV.",
                "default": 14,
            },
        },
        "required": ["highs", "lows", "volumes"],
    },
}


def ease_of_movement_calculator(
    highs: list[float],
    lows: list[float],
    volumes: list[float],
    period: int = 14,
) -> dict[str, Any]:
    """Calculate the Ease of Movement indicator."""
    try:
        n = len(highs)
        if not (n == len(lows) == len(volumes)):
            return {
                "status": "error",
                "data": {"error": "All input arrays must be the same length."},
                "timestamp": datetime.now(timezone.utc).isoformat(),
            }
        if n < period + 1:
            return {
                "status": "error",
                "data": {"error": f"Need at least {period + 1} data points, got {n}."},
                "timestamp": datetime.now(timezone.utc).isoformat(),
            }

        # Distance Moved: ((H + L) / 2) - ((prev_H + prev_L) / 2)
        # Box Ratio: (Volume / scale_factor) / (H - L)
        # EMV = Distance Moved / Box Ratio
        scale_factor = 100000000.0  # Scale volume down for readable values
        raw_emv: list[float] = []

        for i in range(1, n):
            dm = ((highs[i] + lows[i]) / 2) - ((highs[i - 1] + lows[i - 1]) / 2)
            hl_range = highs[i] - lows[i]

            if hl_range == 0:
                raw_emv.append(0.0)
            else:
                box_ratio = (volumes[i] / scale_factor) / hl_range
                if box_ratio == 0:
                    raw_emv.append(0.0)
                else:
                    raw_emv.append(dm / box_ratio)

        # SMA of raw EMV
        emv_sma: list[float] = []
        for i in range(period - 1, len(raw_emv)):
            window = raw_emv[i - period + 1 : i + 1]
            emv_sma.append(round(sum(window) / period, 6))

        latest_emv = emv_sma[-1] if emv_sma else None

        signal = "neutral"
        if latest_emv is not None:
            if latest_emv > 0:
                signal = "Bullish — prices moving up with relative ease"
            elif latest_emv < 0:
                signal = "Bearish — prices moving down with relative ease"

        return {
            "status": "ok",
            "data": {
                "period": period,
                "latest_emv": latest_emv,
                "signal": signal,
                "emv_values": emv_sma[-period:],
                "note": "Ease of Movement relates price movement to volume. High positive EMV = price rising easily. "
                "Low negative EMV = price falling easily. Zero-line crossovers signal trend changes.",
            },
            "timestamp": datetime.now(timezone.utc).isoformat(),
        }
    except Exception as exc:
        return {
            "status": "error",
            "data": {"error": str(exc)},
            "timestamp": datetime.now(timezone.utc).isoformat(),
        }
