"""
Execuve Summary: Calculates Average True Range (ATR) for volatility sizing.
Inputs: highs (list[float]), lows (list[float]), closes (list[float]), period (int)
Outputs: atr_series (list[float]), current_atr (float), atr_pct (float), volatility_regime (str), natr (float)
MCP Tool Name: atr_calculator
"""
import logging
import math
from datetime import datetime, timezone
from typing import Any

logger = logging.getLogger("snowdrop.skills")

TOOL_META = {
    "name": "atr_calculator",
    "description": "Implements Wilder's Average True Range for volatility assessment.",
    "inputSchema": {
        "type": "object",
        "properties": {
            "highs": {"type": "array", "description": "High prices."},
            "lows": {"type": "array", "description": "Low prices."},
            "closes": {"type": "array", "description": "Close prices."},
            "period": {"type": "integer", "description": "ATR period (default 14)."}
        },
        "required": ["highs", "lows", "closes", "period"]
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


def atr_calculator(**kwargs: Any) -> dict:
    """Uses Wilder's smoothing of true range to compute ATR and normalized metrics."""
    try:
        highs = kwargs.get("highs")
        lows = kwargs.get("lows")
        closes = kwargs.get("closes")
        period = kwargs.get("period")

        for series in (highs, lows, closes):
            if not isinstance(series, list) or len(series) < 2:
                raise ValueError("price series must be lists")
        if not (len(highs) == len(lows) == len(closes)):
            raise ValueError("series must align")
        if not isinstance(period, int) or period <= 1:
            raise ValueError("period must be integer > 1")
        if period >= len(highs):
            raise ValueError("period must be less than data length")

        highs_f = []
        lows_f = []
        closes_f = []
        for h, l, c in zip(highs, lows, closes):
            if not isinstance(h, (int, float)) or not isinstance(l, (int, float)) or not isinstance(c, (int, float)):
                raise TypeError("series must be numeric")
            highs_f.append(float(h))
            lows_f.append(float(l))
            closes_f.append(float(c))

        tr_list = [0.0]
        for idx in range(1, len(highs_f)):
            tr = max(highs_f[idx] - lows_f[idx], abs(highs_f[idx] - closes_f[idx - 1]), abs(lows_f[idx] - closes_f[idx - 1]))
            tr_list.append(tr)

        atr_series = [math.nan] * len(tr_list)
        initial_atr = sum(tr_list[1:period + 1]) / period
        atr_series[period] = initial_atr
        prev_atr = initial_atr
        for idx in range(period + 1, len(tr_list)):
            prev_atr = (prev_atr * (period - 1) + tr_list[idx]) / period
            atr_series[idx] = prev_atr

        current_atr = atr_series[-1]
        if math.isnan(current_atr):
            raise ValueError("insufficient data for ATR")
        latest_close = closes_f[-1]
        atr_pct = (current_atr / latest_close) * 100 if latest_close != 0 else math.inf
        if atr_pct < 1:
            regime = "low"
        elif atr_pct < 3:
            regime = "normal"
        else:
            regime = "high"
        natr = current_atr / latest_close * 100 if latest_close != 0 else math.inf

        return {
            "status": "success",
            "data": {
                "atr_series": atr_series,
                "current_atr": current_atr,
                "atr_pct": atr_pct,
                "volatility_regime": regime,
                "natr": natr
            },
            "timestamp": datetime.now(timezone.utc).isoformat()
        }
    except (ValueError, TypeError, ZeroDivisionError) as e:
        logger.error(f"atr_calculator failed: {e}")
        _log_lesson(f"atr_calculator: {e}")
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
