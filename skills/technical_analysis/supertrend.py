"""
Execuve Summary: Generates the Supertrend trailing stop based on ATR to flag trend reversals.
Inputs: highs (list[float]), lows (list[float]), closes (list[float]), period (int), multiplier (float)
Outputs: supertrend_series (list[float]), current_trend (str), current_stop (float), reversal_points (list[int])
MCP Tool Name: supertrend
"""
import logging
import math
from datetime import datetime, timezone
from typing import Any

logger = logging.getLogger("snowdrop.skills")

TOOL_META = {
    "name": "supertrend",
    "description": "Applies the Supertrend algorithm (ATR bands with dynamic flips) to mark trailing stops and trend phase.",
    "inputSchema": {
        "type": "object",
        "properties": {
            "highs": {"type": "array", "description": "High price series."},
            "lows": {"type": "array", "description": "Low price series."},
            "closes": {"type": "array", "description": "Close price series."},
            "period": {"type": "integer", "description": "ATR lookback (default 10)."},
            "multiplier": {"type": "number", "description": "ATR multiplier (default 3)."}
        },
        "required": ["highs", "lows", "closes", "period", "multiplier"]
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


def supertrend(**kwargs: Any) -> dict:
    """Derives Supertrend via ATR bands and identifies flips between bullish and bearish regimes."""
    try:
        highs = kwargs.get("highs")
        lows = kwargs.get("lows")
        closes = kwargs.get("closes")
        period = kwargs.get("period")
        multiplier = kwargs.get("multiplier")

        for series_name, series in (("highs", highs), ("lows", lows), ("closes", closes)):
            if not isinstance(series, list) or len(series) < 2:
                raise ValueError(f"{series_name} must be a list of floats")
        if not (len(highs) == len(lows) == len(closes)):
            raise ValueError("highs, lows, and closes must match in length")

        if not isinstance(period, int) or period <= 1:
            raise ValueError("period must be an integer > 1")
        if not isinstance(multiplier, (int, float)) or multiplier <= 0:
            raise ValueError("multiplier must be a positive number")

        highs_f = []
        lows_f = []
        closes_f = []
        for idx in range(len(highs)):
            h = highs[idx]
            l = lows[idx]
            c = closes[idx]
            if not isinstance(h, (int, float)) or not isinstance(l, (int, float)) or not isinstance(c, (int, float)):
                raise TypeError("price series must be numeric")
            highs_f.append(float(h))
            lows_f.append(float(l))
            closes_f.append(float(c))

        trs = [0.0]
        for idx in range(1, len(highs_f)):
            tr = max(highs_f[idx] - lows_f[idx], abs(highs_f[idx] - closes_f[idx - 1]), abs(lows_f[idx] - closes_f[idx - 1]))
            trs.append(tr)

        atr = [math.nan] * len(trs)
        initial_atr = sum(trs[1:period + 1]) / period
        atr[period] = initial_atr
        prev_atr = initial_atr
        for idx in range(period + 1, len(trs)):
            prev_atr = (prev_atr * (period - 1) + trs[idx]) / period
            atr[idx] = prev_atr

        basic_upper = [math.nan] * len(highs_f)
        basic_lower = [math.nan] * len(highs_f)
        for idx in range(len(highs_f)):
            if math.isnan(atr[idx]):
                continue
            mean_price = (highs_f[idx] + lows_f[idx]) / 2
            basic_upper[idx] = mean_price + multiplier * atr[idx]
            basic_lower[idx] = mean_price - multiplier * atr[idx]

        final_upper = [math.nan] * len(basic_upper)
        final_lower = [math.nan] * len(basic_lower)
        for idx in range(len(basic_upper)):
            if math.isnan(basic_upper[idx]) or math.isnan(basic_lower[idx]):
                continue
            if idx == 0:
                final_upper[idx] = basic_upper[idx]
                final_lower[idx] = basic_lower[idx]
                continue
            if math.isnan(final_upper[idx - 1]) or math.isnan(final_lower[idx - 1]):
                final_upper[idx] = basic_upper[idx]
                final_lower[idx] = basic_lower[idx]
                continue
            final_upper[idx] = basic_upper[idx] if basic_upper[idx] < final_upper[idx - 1] or closes_f[idx - 1] > final_upper[idx - 1] else final_upper[idx - 1]
            final_lower[idx] = basic_lower[idx] if basic_lower[idx] > final_lower[idx - 1] or closes_f[idx - 1] < final_lower[idx - 1] else final_lower[idx - 1]

        supertrend_series = [math.nan] * len(closes_f)
        trend = "down"
        reversal_points: list[int] = []
        for idx in range(len(closes_f)):
            if math.isnan(final_upper[idx]) or math.isnan(final_lower[idx]):
                continue
            if idx == 0 or math.isnan(supertrend_series[idx - 1]):
                supertrend_series[idx] = final_upper[idx]
                trend = "down"
                continue
            prev_super = supertrend_series[idx - 1]
            if prev_super == final_upper[idx - 1]:
                if closes_f[idx] <= final_upper[idx]:
                    supertrend_series[idx] = final_upper[idx]
                    trend = "down"
                else:
                    supertrend_series[idx] = final_lower[idx]
                    trend = "up"
                    reversal_points.append(idx)
            else:
                if closes_f[idx] >= final_lower[idx]:
                    supertrend_series[idx] = final_lower[idx]
                    trend = "up"
                else:
                    supertrend_series[idx] = final_upper[idx]
                    trend = "down"
                    reversal_points.append(idx)

        current_stop = supertrend_series[-1]
        current_trend = "up" if closes_f[-1] > current_stop else "down"

        return {
            "status": "success",
            "data": {
                "supertrend_series": supertrend_series,
                "current_trend": current_trend,
                "current_stop": current_stop,
                "reversal_points": reversal_points
            },
            "timestamp": datetime.now(timezone.utc).isoformat()
        }
    except (ValueError, TypeError, ZeroDivisionError) as e:
        logger.error(f"supertrend failed: {e}")
        _log_lesson(f"supertrend: {e}")
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
