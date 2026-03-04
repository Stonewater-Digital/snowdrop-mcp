"""
Execuve Summary: Measures price rate of change with optional smoothing.
Inputs: prices (list[float]), period (int), smoothing_period (int|None)
Outputs: roc_series (list[float]), smoothed_roc (list[float]), current_roc_pct (float), momentum_trend (str), acceleration_deceleration (str)
MCP Tool Name: roc_calculator
"""
import logging
import math
from datetime import datetime, timezone
from typing import Any

logger = logging.getLogger("snowdrop.skills")

TOOL_META = {
    "name": "roc_calculator",
    "description": "Computes percentage rate of change and optional SMA smoothing to track acceleration.",
    "inputSchema": {
        "type": "object",
        "properties": {
            "prices": {"type": "array", "description": "Price list (oldest first)."},
            "period": {"type": "integer", "description": "Lookback used for ROC (e.g., 12)."},
            "smoothing_period": {"type": "integer", "description": "Optional SMA smoothing length for ROC."}
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


def roc_calculator(**kwargs: Any) -> dict:
    """Computes price ROC and smooths it via simple moving average if requested."""
    try:
        prices = kwargs.get("prices")
        period = kwargs.get("period")
        smoothing_period = kwargs.get("smoothing_period")

        if not isinstance(prices, list) or len(prices) <= period:
            raise ValueError("prices must exceed period length")
        if not isinstance(period, int) or period <= 0:
            raise ValueError("period must be a positive integer")
        if smoothing_period is not None and (not isinstance(smoothing_period, int) or smoothing_period <= 0):
            raise ValueError("smoothing_period must be positive integer when provided")

        prices_f = []
        for price in prices:
            if not isinstance(price, (int, float)):
                raise TypeError("prices must be numeric")
            prices_f.append(float(price))

        roc_series = []
        for idx in range(len(prices_f)):
            if idx < period:
                roc_series.append(math.nan)
                continue
            base_price = prices_f[idx - period]
            if base_price == 0:
                roc_series.append(math.inf if prices_f[idx] > 0 else -math.inf)
            else:
                roc_series.append(((prices_f[idx] - base_price) / base_price) * 100)

        smoothed = []
        if smoothing_period:
            window: list[float] = []
            for value in roc_series:
                if math.isnan(value):
                    smoothed.append(math.nan)
                    continue
                window.append(value)
                if len(window) > smoothing_period:
                    window.pop(0)
                smoothed.append(sum(window) / len(window))
        else:
            smoothed = roc_series[:]

        current_roc = smoothed[-1]
        if math.isnan(current_roc):
            raise ValueError("insufficient data for ROC")

        prev_roc = next((value for value in reversed(smoothed[:-1]) if not math.isnan(value)), current_roc)
        momentum_trend = "rising" if current_roc > prev_roc else ("falling" if current_roc < prev_roc else "flat")

        acceleration = "accelerating" if momentum_trend == "rising" else ("decelerating" if momentum_trend == "falling" else "stable")

        return {
            "status": "success",
            "data": {
                "roc_series": roc_series,
                "smoothed_roc": smoothed,
                "current_roc_pct": current_roc,
                "momentum_trend": momentum_trend,
                "acceleration_deceleration": acceleration
            },
            "timestamp": datetime.now(timezone.utc).isoformat()
        }
    except (ValueError, TypeError, ZeroDivisionError) as e:
        logger.error(f"roc_calculator failed: {e}")
        _log_lesson(f"roc_calculator: {e}")
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
