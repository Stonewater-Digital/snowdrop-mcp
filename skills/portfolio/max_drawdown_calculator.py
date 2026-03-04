"""Calculate maximum drawdown from a price series.

MCP Tool Name: max_drawdown_calculator
"""
from __future__ import annotations

from datetime import datetime, timezone
from typing import Any

TOOL_META: dict[str, Any] = {
    "name": "max_drawdown_calculator",
    "description": (
        "Calculates the maximum drawdown from a series of prices, measuring the "
        "largest peak-to-trough decline as a percentage."
    ),
    "inputSchema": {
        "type": "object",
        "properties": {
            "prices": {
                "type": "array",
                "items": {"type": "number"},
                "description": "List of asset prices in chronological order.",
            },
        },
        "required": ["prices"],
    },
}


def max_drawdown_calculator(prices: list[float]) -> dict[str, Any]:
    """Calculate maximum drawdown from a price series."""
    try:
        prices = [float(p) for p in prices]

        if len(prices) < 2:
            raise ValueError("prices must contain at least 2 values.")

        peak = prices[0]
        max_dd = 0.0
        peak_idx = 0
        trough_idx = 0
        dd_peak_idx = 0

        for i, price in enumerate(prices):
            if price > peak:
                peak = price
                peak_idx = i
            drawdown = (peak - price) / peak if peak != 0 else 0.0
            if drawdown > max_dd:
                max_dd = drawdown
                trough_idx = i
                dd_peak_idx = peak_idx

        return {
            "status": "ok",
            "data": {
                "max_drawdown_pct": round(max_dd * 100, 4),
                "max_drawdown_decimal": round(max_dd, 6),
                "peak_index": dd_peak_idx,
                "trough_index": trough_idx,
                "peak_price": prices[dd_peak_idx],
                "trough_price": prices[trough_idx],
            },
            "timestamp": datetime.now(timezone.utc).isoformat(),
        }
    except Exception as exc:
        return {
            "status": "error",
            "data": {"error": str(exc)},
            "timestamp": datetime.now(timezone.utc).isoformat(),
        }
