"""
Execuve Summary: Computes Commodity Channel Index to identify overbought/oversold departures from mean.
Inputs: highs (list[float]), lows (list[float]), closes (list[float]), period (int), constant (float)
Outputs: cci_series (list[float]), current_cci (float), zone (str), trend_strength (str)
MCP Tool Name: cci_calculator
"""
import logging
import math
from datetime import datetime, timezone
from typing import Any

logger = logging.getLogger("snowdrop.skills")

TOOL_META = {
    "name": "cci_calculator",
    "description": "Calculates Donald Lambert's Commodity Channel Index using a mean deviation normalization.",
    "inputSchema": {
        "type": "object",
        "properties": {
            "highs": {"type": "array", "description": "High prices."},
            "lows": {"type": "array", "description": "Low prices."},
            "closes": {"type": "array", "description": "Close prices."},
            "period": {"type": "integer", "description": "CCI period (default 20)."},
            "constant": {"type": "number", "description": "Constant divisor (default 0.015)."}
        },
        "required": ["highs", "lows", "closes", "period", "constant"]
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


def cci_calculator(**kwargs: Any) -> dict:
    """Derives typical price, smooths it via SMA, and scales deviation by Lambert's constant."""
    try:
        highs = kwargs.get("highs")
        lows = kwargs.get("lows")
        closes = kwargs.get("closes")
        period = kwargs.get("period")
        constant = kwargs.get("constant")

        for series in (highs, lows, closes):
            if not isinstance(series, list) or len(series) < 2:
                raise ValueError("price series must be lists")
        if not (len(highs) == len(lows) == len(closes)):
            raise ValueError("highs, lows, closes must match length")
        if not isinstance(period, int) or period <= 1:
            raise ValueError("period must be > 1")
        if period > len(highs):
            raise ValueError("period cannot exceed data length")
        if not isinstance(constant, (int, float)) or constant <= 0:
            raise ValueError("constant must be positive")

        typical_prices = []
        for h, l, c in zip(highs, lows, closes):
            if not isinstance(h, (int, float)) or not isinstance(l, (int, float)) or not isinstance(c, (int, float)):
                raise TypeError("prices must be numeric")
            typical_prices.append((float(h) + float(l) + float(c)) / 3)

        sma_series = []
        cci_series = []
        window: list[float] = []
        for idx, tp in enumerate(typical_prices):
            window.append(tp)
            if len(window) > period:
                window.pop(0)
            if len(window) == period:
                sma = sum(window) / period
                sma_series.append(sma)
                mean_dev = sum(abs(val - sma) for val in window) / period
                denominator = constant * mean_dev if mean_dev != 0 else math.inf
                if math.isfinite(denominator):
                    cci = (tp - sma) / denominator
                else:
                    cci = 0.0
                cci_series.append(cci)
            else:
                sma_series.append(math.nan)
                cci_series.append(math.nan)

        current_cci = cci_series[-1]
        if math.isnan(current_cci):
            raise ValueError("insufficient data for CCI")

        if current_cci > 100:
            zone = "overbought"
        elif current_cci < -100:
            zone = "oversold"
        else:
            zone = "normal"

        if abs(current_cci) < 50:
            trend_strength = "weak"
        elif abs(current_cci) < 100:
            trend_strength = "moderate"
        elif abs(current_cci) < 200:
            trend_strength = "strong"
        else:
            trend_strength = "extreme"

        return {
            "status": "success",
            "data": {
                "cci_series": cci_series,
                "current_cci": current_cci,
                "zone": zone,
                "trend_strength": trend_strength
            },
            "timestamp": datetime.now(timezone.utc).isoformat()
        }
    except (ValueError, TypeError, ZeroDivisionError) as e:
        logger.error(f"cci_calculator failed: {e}")
        _log_lesson(f"cci_calculator: {e}")
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
