"""
Execuve Summary: Tracks Chaikin Volatility as the rate of change of the high-low EMA.
Inputs: highs (list[float]), lows (list[float]), ema_period (int), roc_period (int)
Outputs: chaikin_vol_series (list[float]), current_value (float), expanding_contracting (str), signal (str)
MCP Tool Name: chaikin_volatility
"""
import logging
import math
from datetime import datetime, timezone
from typing import Any

logger = logging.getLogger("snowdrop.skills")

TOOL_META = {
    "name": "chaikin_volatility",
    "description": "Calculates Chaikin Volatility (EMA of range with rate-of-change comparison).",
    "inputSchema": {
        "type": "object",
        "properties": {
            "highs": {"type": "array", "description": "High prices."},
            "lows": {"type": "array", "description": "Low prices."},
            "ema_period": {"type": "integer", "description": "EMA period (default 10)."},
            "roc_period": {"type": "integer", "description": "Lookback for EMA rate-of-change (default 10)."}
        },
        "required": ["highs", "lows", "ema_period", "roc_period"]
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


def chaikin_volatility(**kwargs: Any) -> dict:
    """Derives Chaikin Volatility = 100 * (EMA(high-low) - EMA lag) / EMA lag."""
    try:
        highs = kwargs.get("highs")
        lows = kwargs.get("lows")
        ema_period = kwargs.get("ema_period")
        roc_period = kwargs.get("roc_period")

        for series in (highs, lows):
            if not isinstance(series, list) or len(series) < 2:
                raise ValueError("series must be lists")
        if len(highs) != len(lows):
            raise ValueError("highs and lows must align")
        for label, value in (("ema_period", ema_period), ("roc_period", roc_period)):
            if not isinstance(value, int) or value <= 0:
                raise ValueError(f"{label} must be positive integer")

        ranges = []
        for h, l in zip(highs, lows):
            if not isinstance(h, (int, float)) or not isinstance(l, (int, float)):
                raise TypeError("highs and lows must be numeric")
            ranges.append(float(h) - float(l))

        def _ema(values: list[float], period: int) -> list[float]:
            alpha = 2 / (period + 1)
            ema = [math.nan] * len(values)
            if len(values) < period:
                return ema
            seed = sum(values[:period]) / period
            ema[period - 1] = seed
            prev = seed
            for idx in range(period, len(values)):
                prev = alpha * values[idx] + (1 - alpha) * prev
                ema[idx] = prev
            return ema

        ema_range = _ema(ranges, ema_period)
        chaikin_series = [math.nan] * len(ema_range)
        for idx in range(roc_period, len(ema_range)):
            current = ema_range[idx]
            past = ema_range[idx - roc_period]
            if math.isnan(current) or math.isnan(past) or past == 0:
                continue
            chaikin_series[idx] = ((current - past) / past) * 100

        current_value = chaikin_series[-1]
        if math.isnan(current_value):
            raise ValueError("insufficient data for Chaikin Volatility")
        expanding_contracting = "expanding" if current_value > 0 else ("contracting" if current_value < 0 else "flat")
        if expanding_contracting == "expanding":
            signal = "expansion"
        elif expanding_contracting == "contracting":
            signal = "contraction"
        else:
            signal = "neutral"

        return {
            "status": "success",
            "data": {
                "chaikin_vol_series": chaikin_series,
                "current_value": current_value,
                "expanding_contracting": expanding_contracting,
                "signal": signal
            },
            "timestamp": datetime.now(timezone.utc).isoformat()
        }
    except (ValueError, TypeError, ZeroDivisionError) as e:
        logger.error(f"chaikin_volatility failed: {e}")
        _log_lesson(f"chaikin_volatility: {e}")
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
