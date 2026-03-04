"""
Execuve Summary: Builds a moving average ribbon across multiple periods.
Inputs: prices (list[float]), periods (list[int])
Outputs: ma_values_per_period (dict), ribbon_spread (float), ribbon_expanding (bool), trend_alignment (str), squeeze_detected (bool)
MCP Tool Name: moving_average_ribbon
"""
import logging
import math
from datetime import datetime, timezone
from typing import Any

logger = logging.getLogger("snowdrop.skills")

TOOL_META = {
    "name": "moving_average_ribbon",
    "description": "Calculates SMA values for multiple periods to form a ribbon and detect trend/squeeze signals.",
    "inputSchema": {
        "type": "object",
        "properties": {
            "prices": {"type": "array", "description": "Price series."},
            "periods": {"type": "array", "description": "List of SMA periods (e.g., [10,20,30...])."}
        },
        "required": ["prices", "periods"]
    },
    "outputSchema": {
        "type": "object",
        "properties": {
            "status": {"type": "string"},
            "timestamp": {"type": "string"},
            "data": {"type": "object"}
        },
        "required": ["status", "timestamp"]
    }
}


def moving_average_ribbon(**kwargs: Any) -> dict:
    """Calculates multiple SMAs and evaluates spacing/trend cohesion."""
    try:
        prices = kwargs.get("prices")
        periods = kwargs.get("periods")

        if not isinstance(prices, list) or len(prices) < 2:
            raise ValueError("prices must be list with >=2 items")
        if not isinstance(periods, list) or not periods:
            raise ValueError("periods must be a non-empty list")
        periods = sorted({int(period) for period in periods})
        if periods[0] <= 1:
            raise ValueError("periods must be > 1")

        ma_values = {}
        for period in periods:
            if period > len(prices):
                raise ValueError("each period must be <= len(prices)")
            ma = sum(prices[-period:]) / period
            ma_values[str(period)] = ma

        ordered_mas = [ma_values[str(period)] for period in periods]
        ribbon_spread = max(ordered_mas) - min(ordered_mas)
        latest_price = prices[-1]
        squeeze_detected = (ribbon_spread / latest_price) < 0.01 if latest_price != 0 else False

        trend_alignment = "mixed"
        if ordered_mas == sorted(ordered_mas, reverse=True):
            trend_alignment = "bearish"
        elif ordered_mas == sorted(ordered_mas):
            trend_alignment = "bullish"

        previous_mas = {}
        for period in periods:
            if period + 1 > len(prices):
                previous_mas[str(period)] = ma_values[str(period)]
            else:
                previous_mas[str(period)] = sum(prices[-(period + 1):-1]) / period
        prev_spread = max(previous_mas.values()) - min(previous_mas.values())
        ribbon_expanding = ribbon_spread > prev_spread

        return {
            "status": "success",
            "data": {
                "ma_values_per_period": ma_values,
                "ribbon_spread": ribbon_spread,
                "ribbon_expanding": ribbon_expanding,
                "trend_alignment": trend_alignment,
                "squeeze_detected": squeeze_detected
            },
            "timestamp": datetime.now(timezone.utc).isoformat()
        }
    except (ValueError, TypeError, ZeroDivisionError) as e:
        logger.error(f"moving_average_ribbon failed: {e}")
        _log_lesson(f"moving_average_ribbon: {e}")
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
