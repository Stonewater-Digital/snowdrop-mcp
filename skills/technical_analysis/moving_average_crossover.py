"""
Execuve Summary: Detects golden/death cross events between fast and slow moving averages.
Inputs: prices (list[float]), fast_period (int), slow_period (int)
Outputs: current_state (str), crossover_date_index (int|None), days_since_crossover (int|None), fast_ma (float), slow_ma (float)
MCP Tool Name: moving_average_crossover
"""
import logging
import math
from datetime import datetime, timezone
from typing import Any

logger = logging.getLogger("snowdrop.skills")

TOOL_META = {
    "name": "moving_average_crossover",
    "description": "Compares fast and slow simple moving averages to flag golden or death cross confirmations.",
    "inputSchema": {
        "type": "object",
        "properties": {
            "prices": {
                "type": "array",
                "description": "Chronological list of prices used to compute both averages."
            },
            "fast_period": {
                "type": "integer",
                "description": "Lookback for the fast moving average (e.g., 50)."
            },
            "slow_period": {
                "type": "integer",
                "description": "Lookback for the slow moving average (e.g., 200)."
            }
        },
        "required": ["prices", "fast_period", "slow_period"]
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


def moving_average_crossover(**kwargs: Any) -> dict:
    """Computes fast and slow SMAs, identifies last crossover, and evaluates present alignment."""
    try:
        prices_raw = kwargs.get("prices")
        fast_period = kwargs.get("fast_period")
        slow_period = kwargs.get("slow_period")

        if not isinstance(prices_raw, list) or len(prices_raw) < 2:
            raise ValueError("prices must be a list")
        prices = []
        for value in prices_raw:
            if not isinstance(value, (int, float)):
                raise TypeError("prices must be numeric")
            prices.append(float(value))

        for label, value in (("fast_period", fast_period), ("slow_period", slow_period)):
            if not isinstance(value, int) or value <= 0:
                raise ValueError(f"{label} must be a positive integer")

        if fast_period >= slow_period:
            raise ValueError("fast_period should be less than slow_period for classic crossovers")
        if slow_period > len(prices):
            raise ValueError("slow_period cannot exceed price length")

        def _sma(period: int) -> list[float]:
            values = []
            window: list[float] = []
            total = 0.0
            for price in prices:
                window.append(price)
                total += price
                if len(window) > period:
                    total -= window.pop(0)
                if len(window) == period:
                    values.append(total / period)
                else:
                    values.append(math.nan)
            return values

        fast_ma_series = _sma(fast_period)
        slow_ma_series = _sma(slow_period)
        fast_ma = fast_ma_series[-1]
        slow_ma = slow_ma_series[-1]
        if math.isnan(fast_ma) or math.isnan(slow_ma):
            raise ValueError("insufficient data to compute moving averages")

        current_state = "golden_cross" if fast_ma > slow_ma else ("death_cross" if fast_ma < slow_ma else "neutral")

        crossover_index = None
        crossover_type = None
        for idx in range(1, len(prices)):
            prev_fast = fast_ma_series[idx - 1]
            prev_slow = slow_ma_series[idx - 1]
            curr_fast = fast_ma_series[idx]
            curr_slow = slow_ma_series[idx]
            if math.isnan(prev_fast) or math.isnan(prev_slow) or math.isnan(curr_fast) or math.isnan(curr_slow):
                continue
            previous_diff = prev_fast - prev_slow
            current_diff = curr_fast - curr_slow
            if previous_diff <= 0 < current_diff:
                crossover_index = idx
                crossover_type = "golden_cross"
            elif previous_diff >= 0 > current_diff:
                crossover_index = idx
                crossover_type = "death_cross"
        days_since = len(prices) - 1 - crossover_index if crossover_index is not None else None

        recent_alignment = {
            "fast_ma": fast_ma,
            "slow_ma": slow_ma,
            "current_state": current_state,
            "last_crossover_type": crossover_type,
            "last_crossover_index": crossover_index,
            "days_since_crossover": days_since
        }

        return {
            "status": "success",
            "data": recent_alignment,
            "timestamp": datetime.now(timezone.utc).isoformat()
        }
    except (ValueError, TypeError, ZeroDivisionError) as e:
        logger.error(f"moving_average_crossover failed: {e}")
        _log_lesson(f"moving_average_crossover: {e}")
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
