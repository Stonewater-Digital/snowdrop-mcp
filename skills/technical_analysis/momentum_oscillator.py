"""
Execuve Summary: Computes momentum and rate-of-change to quantify acceleration.
Inputs: prices (list[float]), period (int)
Outputs: momentum_series (list[float]), roc_series (list[float]), current_momentum (float), zero_line_crossover (str), acceleration (str)
MCP Tool Name: momentum_oscillator
"""
import logging
import math
from datetime import datetime, timezone
from typing import Any

logger = logging.getLogger("snowdrop.skills")

TOOL_META = {
    "name": "momentum_oscillator",
    "description": "Measures price momentum as the difference and percent change over a configurable lookback.",
    "inputSchema": {
        "type": "object",
        "properties": {
            "prices": {"type": "array", "description": "Price list (oldest first)."},
            "period": {"type": "integer", "description": "Lookback period for momentum calculation."}
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


def momentum_oscillator(**kwargs: Any) -> dict:
    """Calculates simple momentum and rate of change to spot zero-line crosses and acceleration."""
    try:
        prices = kwargs.get("prices")
        period = kwargs.get("period")

        if not isinstance(prices, list) or len(prices) <= period:
            raise ValueError("prices must be list longer than the period")
        if not isinstance(period, int) or period <= 0:
            raise ValueError("period must be positive integer")

        prices_f = []
        for price in prices:
            if not isinstance(price, (int, float)):
                raise TypeError("prices must be numeric")
            prices_f.append(float(price))

        momentum_series = []
        roc_series = []
        for idx in range(len(prices_f)):
            if idx < period:
                momentum_series.append(math.nan)
                roc_series.append(math.nan)
                continue
            momentum_value = prices_f[idx] - prices_f[idx - period]
            momentum_series.append(momentum_value)
            base_price = prices_f[idx - period]
            if base_price == 0:
                roc_series.append(math.inf if momentum_value > 0 else -math.inf)
            else:
                roc_series.append((momentum_value / base_price) * 100)

        current_momentum = momentum_series[-1]
        current_roc = roc_series[-1]
        if math.isnan(current_momentum):
            raise ValueError("insufficient data for momentum")

        prev_momentum = momentum_series[-2]
        zero_line_crossover = "none"
        if not math.isnan(prev_momentum):
            if current_momentum > 0 >= prev_momentum:
                zero_line_crossover = "bullish_cross"
            elif current_momentum < 0 <= prev_momentum:
                zero_line_crossover = "bearish_cross"

        acceleration = "increasing" if current_momentum > prev_momentum else ("decreasing" if current_momentum < prev_momentum else "flat")

        return {
            "status": "success",
            "data": {
                "momentum_series": momentum_series,
                "roc_series": roc_series,
                "current_momentum": current_momentum,
                "current_roc_pct": current_roc,
                "zero_line_crossover": zero_line_crossover,
                "acceleration": acceleration
            },
            "timestamp": datetime.now(timezone.utc).isoformat()
        }
    except (ValueError, TypeError, ZeroDivisionError) as e:
        logger.error(f"momentum_oscillator failed: {e}")
        _log_lesson(f"momentum_oscillator: {e}")
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
