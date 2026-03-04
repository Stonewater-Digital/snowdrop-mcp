"""
Execuve Summary: Applies double exponential smoothing to reduce EMA lag relative to price.
Inputs: prices (list[float]), period (int)
Outputs: dema_series (list[float]), current_dema (float), vs_ema_lag_reduction (float)
MCP Tool Name: dema_calculator
"""
import logging
import math
from datetime import datetime, timezone
from typing import Any

logger = logging.getLogger("snowdrop.skills")

TOOL_META = {
    "name": "dema_calculator",
    "description": "Computes the Double Exponential Moving Average (2*EMA - EMA(EMA)) to highlight early momentum turns.",
    "inputSchema": {
        "type": "object",
        "properties": {
            "prices": {
                "type": "array",
                "description": "Chronological price series used for the base EMA calculation."
            },
            "period": {
                "type": "integer",
                "description": "Lookback period for both EMA layers."
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


def dema_calculator(**kwargs: Any) -> dict:
    """Uses Patrick Mulloy's 1994 DEMA formula to compare lag against traditional EMA."""
    try:
        prices_raw = kwargs.get("prices")
        period = kwargs.get("period")

        if not isinstance(prices_raw, list) or len(prices_raw) < 2:
            raise ValueError("prices must be a list")
        prices = []
        for price in prices_raw:
            if not isinstance(price, (int, float)):
                raise TypeError("prices must contain numbers")
            prices.append(float(price))

        if not isinstance(period, int) or period <= 0:
            raise ValueError("period must be a positive integer")
        if period > len(prices):
            raise ValueError("period cannot exceed prices length")

        alpha = 2 / (period + 1)
        ema_first = [math.nan] * len(prices)
        seed = sum(prices[:period]) / period
        ema_first[period - 1] = seed
        ema_val = seed
        for idx in range(period, len(prices)):
            ema_val = alpha * prices[idx] + (1 - alpha) * ema_val
            ema_first[idx] = ema_val

        ema_second = [math.nan] * len(prices)
        ema_pool: list[float] = []
        ema_second_val = math.nan
        for idx, ema_point in enumerate(ema_first):
            if math.isnan(ema_point):
                continue
            ema_pool.append(ema_point)
            if len(ema_pool) == period:
                ema_second_val = sum(ema_pool) / period
                ema_second[idx] = ema_second_val
            elif len(ema_pool) > period:
                ema_second_val = alpha * ema_point + (1 - alpha) * ema_second_val
                ema_second[idx] = ema_second_val

        dema_series = []
        for ema_val_first, ema_val_second in zip(ema_first, ema_second):
            if math.isnan(ema_val_first) or math.isnan(ema_val_second):
                dema_series.append(math.nan)
            else:
                dema_series.append(2 * ema_val_first - ema_val_second)

        current_dema = dema_series[-1]
        if math.isnan(current_dema):
            raise ValueError("insufficient data for DEMA")
        current_ema = ema_first[-1]
        lag_reduction = current_ema - current_dema
        price_relation = "above" if prices[-1] > current_dema else ("below" if prices[-1] < current_dema else "at")

        return {
            "status": "success",
            "data": {
                "dema_series": dema_series,
                "current_dema": current_dema,
                "current_ema": current_ema,
                "vs_ema_lag_reduction": lag_reduction,
                "price_relation": price_relation
            },
            "timestamp": datetime.now(timezone.utc).isoformat()
        }
    except (ValueError, TypeError, ZeroDivisionError) as e:
        logger.error(f"dema_calculator failed: {e}")
        _log_lesson(f"dema_calculator: {e}")
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
