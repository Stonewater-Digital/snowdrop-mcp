"""
Execuve Summary: Analyzes drawdown profile including max depth and recovery timeline.
Inputs: prices (list[float])
Outputs: max_drawdown_pct (float), peak_date_index (int), trough_date_index (int), recovery_date_index (int|None), current_drawdown (float), drawdown_series (list[float]), top_5_drawdowns (list)
MCP Tool Name: max_drawdown_analyzer
"""
import logging
import math
from datetime import datetime, timezone
from typing import Any

logger = logging.getLogger("snowdrop.skills")

TOOL_META = {
    "name": "max_drawdown_analyzer",
    "description": "Computes drawdown statistics, including top drawdowns and recovery metrics.",
    "inputSchema": {
        "type": "object",
        "properties": {
            "prices": {"type": "array", "description": "Equity curve or price series."}
        },
        "required": ["prices"]
    },
    "outputSchema": {
        "type": "object", "properties": {"status": {"type": "string"}, "timestamp": {"type": "string"}, "data": {"type": "object"}},
        "required": ["status", "timestamp"]
    }
}


def max_drawdown_analyzer(**kwargs: Any) -> dict:
    """Calculates drawdown series and identifies peak/trough/recovery stats."""
    try:
        prices = kwargs.get("prices")
        if not isinstance(prices, list) or len(prices) < 2:
            raise ValueError("prices must be a list with at least two observations")
        prices_f = []
        for price in prices:
            if not isinstance(price, (int, float)):
                raise TypeError("prices must be numeric")
            if price <= 0:
                raise ValueError("prices must be positive for drawdown analysis")
            prices_f.append(float(price))

        peak = prices_f[0]
        peak_index = 0
        drawdown_series = [0.0]
        trough_index = 0
        max_drawdown = 0.0
        peak_indices = [0]
        troughs = []
        for idx, price in enumerate(prices_f[1:], start=1):
            if price > peak:
                peak = price
                peak_index = idx
            peak_indices.append(peak_index)
            drawdown = price / peak - 1
            drawdown_series.append(drawdown)
            if drawdown < max_drawdown:
                max_drawdown = drawdown
                trough_index = idx
            if drawdown < 0:
                troughs.append((peak_index, idx, drawdown))

        recovery_date = None
        peak_value = prices_f[peak_indices[trough_index]]
        for idx in range(trough_index, len(prices_f)):
            if prices_f[idx] >= peak_value:
                recovery_date = idx
                break

        top_drawdowns = sorted(troughs, key=lambda item: item[2])[:5]
        top_5 = [
            {
                "peak_index": item[0],
                "trough_index": item[1],
                "drawdown_pct": item[2]
            }
            for item in top_drawdowns
        ]

        current_drawdown = drawdown_series[-1]
        return {
            "status": "success",
            "data": {
                "max_drawdown_pct": max_drawdown,
                "peak_date_index": peak_indices[trough_index],
                "trough_date_index": trough_index,
                "recovery_date_index": recovery_date,
                "current_drawdown": current_drawdown,
                "drawdown_series": drawdown_series,
                "top_5_drawdowns": top_5
            },
            "timestamp": datetime.now(timezone.utc).isoformat()
        }
    except (ValueError, TypeError, ZeroDivisionError) as e:
        logger.error(f"max_drawdown_analyzer failed: {e}")
        _log_lesson(f"max_drawdown_analyzer: {e}")
        return {
            "status": "error",
            "error": str(e),
            "timestamp": datetime.now(timezone.utc).isoformat()
        }


def _log_lesson(message: str) -> None:
    try:
        with open("logs/lessons.md", "a") as f:
            f.write(f"- [{datetime.now(timezone.utc).isoformat()}] {message}\n")
    except OSError:
        pass
