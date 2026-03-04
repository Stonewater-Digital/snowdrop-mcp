"""
Execuve Summary: Builds Bollinger Bands using population standard deviation for volatility analysis.
Inputs: prices (list[float]), period (int), num_std (float)
Outputs: upper_band (float), middle_band (float), lower_band (float), percent_b (float), bandwidth (float), squeeze_detected (bool)
MCP Tool Name: bollinger_bands
"""
import logging
import math
from datetime import datetime, timezone
from typing import Any

logger = logging.getLogger("snowdrop.skills")

TOOL_META = {
    "name": "bollinger_bands",
    "description": "Calculates SMA-based Bollinger Bands with configurable standard deviation multipliers.",
    "inputSchema": {
        "type": "object",
        "properties": {
            "prices": {"type": "array", "description": "Price list (oldest first)."},
            "period": {"type": "integer", "description": "SMA lookback (default 20)."},
            "num_std": {"type": "number", "description": "Standard deviation multiplier (default 2)."}
        },
        "required": ["prices", "period", "num_std"]
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


def bollinger_bands(**kwargs: Any) -> dict:
    """Computes Bollinger Bands per John Bollinger with population standard deviation."""
    try:
        prices = kwargs.get("prices")
        period = kwargs.get("period")
        num_std = kwargs.get("num_std")

        if not isinstance(prices, list) or len(prices) < period:
            raise ValueError("prices must contain at least 'period' points")
        if not isinstance(period, int) or period <= 1:
            raise ValueError("period must be integer > 1")
        if not isinstance(num_std, (int, float)) or num_std <= 0:
            raise ValueError("num_std must be positive number")

        prices_f = []
        for price in prices:
            if not isinstance(price, (int, float)):
                raise TypeError("prices must be numeric")
            prices_f.append(float(price))

        window = prices_f[-period:]
        middle_band = sum(window) / period
        variance = sum((value - middle_band) ** 2 for value in window) / period
        std_dev = math.sqrt(variance)
        upper_band = middle_band + num_std * std_dev
        lower_band = middle_band - num_std * std_dev
        latest_price = prices_f[-1]
        denominator = upper_band - lower_band
        percent_b = (latest_price - lower_band) / denominator if denominator != 0 else 0.5
        bandwidth = denominator / middle_band if middle_band != 0 else math.inf
        squeeze_detected = bandwidth < 0.05

        return {
            "status": "success",
            "data": {
                "upper_band": upper_band,
                "middle_band": middle_band,
                "lower_band": lower_band,
                "percent_b": percent_b,
                "bandwidth": bandwidth,
                "squeeze_detected": squeeze_detected
            },
            "timestamp": datetime.now(timezone.utc).isoformat()
        }
    except (ValueError, TypeError, ZeroDivisionError) as e:
        logger.error(f"bollinger_bands failed: {e}")
        _log_lesson(f"bollinger_bands: {e}")
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
