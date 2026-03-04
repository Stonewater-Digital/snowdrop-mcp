"""
Execuve Summary: Computes exponential moving averages to emphasize recent prices.
Inputs: prices (list[float]), period (int)
Outputs: ema_series (list[float]), current_ema (float), smoothing_factor (float), crossover_with_price (str)
MCP Tool Name: ema_calculator
"""
import logging
import math
from datetime import datetime, timezone
from typing import Any

logger = logging.getLogger("snowdrop.skills")

TOOL_META = {
    "name": "ema_calculator",
    "description": "Calculates exponential moving averages using Wilder's smoothing to detect price momentum shifts.",
    "inputSchema": {
        "type": "object",
        "properties": {
            "prices": {
                "type": "array",
                "description": "Chronological price list (oldest first)."
            },
            "period": {
                "type": "integer",
                "description": "EMA lookback period (e.g., 12, 26)."
            }
        },
        "required": ["prices", "period"]
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


def ema_calculator(**kwargs: Any) -> dict:
    """Applies the exponential smoothing factor 2/(n+1) to highlight recent price action per Wilder."""
    try:
        prices_raw = kwargs.get("prices")
        period = kwargs.get("period")

        if not isinstance(prices_raw, list) or len(prices_raw) < 2:
            raise ValueError("prices must be a non-empty list")
        prices = []
        for val in prices_raw:
            if not isinstance(val, (int, float)):
                raise TypeError("prices must contain numbers")
            prices.append(float(val))

        if not isinstance(period, int) or period <= 0:
            raise ValueError("period must be a positive integer")
        if period > len(prices):
            raise ValueError("period cannot exceed data length")

        alpha = 2 / (period + 1)
        ema_series = [math.nan] * len(prices)
        initial_sum = sum(prices[:period])
        ema_value = initial_sum / period
        ema_series[period - 1] = ema_value

        for idx in range(period, len(prices)):
            ema_value = alpha * prices[idx] + (1 - alpha) * ema_value
            ema_series[idx] = ema_value

        current_price = prices[-1]
        current_ema = ema_series[-1]
        if math.isnan(current_ema):
            raise ValueError("insufficient data for EMA")

        previous_price = prices[-2]
        previous_ema = ema_series[-2]
        last_relation = current_price - current_ema
        prior_relation = previous_price - previous_ema if not math.isnan(previous_ema) else 0.0
        if last_relation > 0 and prior_relation <= 0:
            crossover = "bullish_cross"
        elif last_relation < 0 and prior_relation >= 0:
            crossover = "bearish_cross"
        else:
            crossover = "no_change"

        slope = current_ema - ema_series[-2] if not math.isnan(ema_series[-2]) else 0.0

        return {
            "status": "success",
            "data": {
                "ema_series": ema_series,
                "current_ema": current_ema,
                "smoothing_factor": alpha,
                "crossover_with_price": crossover,
                "ema_slope": slope,
                "latest_price": current_price
            },
            "timestamp": datetime.now(timezone.utc).isoformat()
        }
    except (ValueError, TypeError, ZeroDivisionError) as e:
        logger.error(f"ema_calculator failed: {e}")
        _log_lesson(f"ema_calculator: {e}")
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
