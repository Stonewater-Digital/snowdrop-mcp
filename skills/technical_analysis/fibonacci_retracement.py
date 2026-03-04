"""
Execuve Summary: Calculates Fibonacci retracement levels for a swing move.
Inputs: swing_high (float), swing_low (float), trend (str), current_price (float|None)
Outputs: levels (dict), price_at_each_level (dict), current_price_near (str)
MCP Tool Name: fibonacci_retracement
"""
import logging
import math
from datetime import datetime, timezone
from typing import Any

logger = logging.getLogger("snowdrop.skills")

TOOL_META = {
    "name": "fibonacci_retracement",
    "description": "Computes common Fibonacci retracement prices (23.6%, 38.2%, 50%, 61.8%, 78.6%) for trend analysis.",
    "inputSchema": {
        "type": "object",
        "properties": {
            "swing_high": {"type": "number", "description": "Recent swing high price."},
            "swing_low": {"type": "number", "description": "Recent swing low price."},
            "trend": {"type": "string", "description": "Direction of move being measured: up or down."},
            "current_price": {"type": "number", "description": "Optional current price to identify nearest retracement."}
        },
        "required": ["swing_high", "swing_low", "trend"]
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

LEVELS = [0.0, 23.6, 38.2, 50.0, 61.8, 78.6, 100.0]


def fibonacci_retracement(**kwargs: Any) -> dict:
    """Applies Fibonacci ratios to the swing range to highlight potential support/resistance."""
    try:
        swing_high = kwargs.get("swing_high")
        swing_low = kwargs.get("swing_low")
        trend = kwargs.get("trend")
        current_price = kwargs.get("current_price")

        if not isinstance(swing_high, (int, float)) or not isinstance(swing_low, (int, float)):
            raise ValueError("swing_high and swing_low must be numbers")
        if swing_high <= swing_low:
            raise ValueError("swing_high must be greater than swing_low")
        if not isinstance(trend, str) or trend.lower() not in {"up", "down"}:
            raise ValueError("trend must be 'up' or 'down'")
        if current_price is not None and not isinstance(current_price, (int, float)):
            raise ValueError("current_price must be numeric if provided")

        trend = trend.lower()
        range_size = swing_high - swing_low
        price_levels: dict[str, float] = {}
        for level in LEVELS:
            if trend == "up":
                price_at_level = swing_high - (level / 100) * range_size
            else:
                price_at_level = swing_low + (level / 100) * range_size
            price_levels[f"{level}"] = price_at_level

        nearest_level = None
        if current_price is not None:
            distances = {level: abs(current_price - price) for level, price in price_levels.items()}
            nearest_level = min(distances, key=distances.get)

        return {
            "status": "success",
            "data": {
                "levels": LEVELS,
                "price_at_each_level": price_levels,
                "current_price_near": nearest_level,
                "trend_reference": trend
            },
            "timestamp": datetime.now(timezone.utc).isoformat()
        }
    except (ValueError, TypeError, ZeroDivisionError) as e:
        logger.error(f"fibonacci_retracement failed: {e}")
        _log_lesson(f"fibonacci_retracement: {e}")
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
