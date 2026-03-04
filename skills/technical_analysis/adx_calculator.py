"""
Execuve Summary: Measures trend strength via Average Directional Index (ADX).
Inputs: highs (list[float]), lows (list[float]), closes (list[float]), period (int)
Outputs: adx (float), plus_di (float), minus_di (float), trend_strength (str), directional_signal (str)
MCP Tool Name: adx_calculator
"""
import logging
import math
from datetime import datetime, timezone
from typing import Any

logger = logging.getLogger("snowdrop.skills")

TOOL_META = {
    "name": "adx_calculator",
    "description": "Applies Wilder's Average Directional Index to gauge whether trends are weak or strong.",
    "inputSchema": {
        "type": "object",
        "properties": {
            "highs": {"type": "array", "description": "High prices (oldest first)."},
            "lows": {"type": "array", "description": "Low prices aligned with highs."},
            "closes": {"type": "array", "description": "Close prices for true range computation."},
            "period": {"type": "integer", "description": "ADX period, typically 14."}
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


def adx_calculator(**kwargs: Any) -> dict:
    """Follows Wilder's 1978 smoothing of directional movement and true range to derive ADX."""
    try:
        highs = kwargs.get("highs")
        lows = kwargs.get("lows")
        closes = kwargs.get("closes")
        period = kwargs.get("period")

        for series_name, series in (("highs", highs), ("lows", lows), ("closes", closes)):
            if not isinstance(series, list) or len(series) < 2:
                raise ValueError(f"{series_name} must be a list")
        if not (len(highs) == len(lows) == len(closes)):
            raise ValueError("highs, lows, and closes must be equal length")
        if not isinstance(period, int) or period <= 1:
            raise ValueError("period must be an integer greater than 1")
        if period >= len(highs):
            raise ValueError("period must be less than data length")

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

        tr_list = [0.0]
        plus_dm = [0.0]
        minus_dm = [0.0]
        for idx in range(1, len(highs_f)):
            high = highs_f[idx]
            low = lows_f[idx]
            prev_high = highs_f[idx - 1]
            prev_low = lows_f[idx - 1]
            prev_close = closes_f[idx - 1]

            tr = max(high - low, abs(high - prev_close), abs(low - prev_close))
            tr_list.append(tr)

            up_move = high - prev_high
            down_move = prev_low - low
            plus_dm.append(up_move if up_move > down_move and up_move > 0 else 0.0)
            minus_dm.append(down_move if down_move > up_move and down_move > 0 else 0.0)

        def _wilder_smooth(data: list[float]) -> list[float]:
            smoothed = [math.nan] * len(data)
            initial = sum(data[1:period + 1])
            smoothed[period] = initial
            prev = initial
            for idx in range(period + 1, len(data)):
                prev = prev - (prev / period) + data[idx]
                smoothed[idx] = prev
            return smoothed

        tr_smooth = _wilder_smooth(tr_list)
        plus_dm_smooth = _wilder_smooth(plus_dm)
        minus_dm_smooth = _wilder_smooth(minus_dm)

        plus_di = [math.nan] * len(highs_f)
        minus_di = [math.nan] * len(highs_f)
        dx = [math.nan] * len(highs_f)
        for idx in range(period, len(highs_f)):
            tr_value = tr_smooth[idx]
            if tr_value == 0 or math.isnan(tr_value):
                continue
            plus_di[idx] = 100 * (plus_dm_smooth[idx] / tr_value)
            minus_di[idx] = 100 * (minus_dm_smooth[idx] / tr_value)
            sum_di = plus_di[idx] + minus_di[idx]
            if sum_di == 0:
                dx[idx] = 0.0
            else:
                dx[idx] = 100 * abs(plus_di[idx] - minus_di[idx]) / sum_di

        adx_series = [math.nan] * len(highs_f)
        valid_dx = [value for value in dx if not math.isnan(value)]
        if len(valid_dx) < period:
            raise ValueError("insufficient DX values for ADX")
        first_adx_index = dx.index(valid_dx[period - 1])
        initial_adx = sum(valid_dx[:period]) / period
        adx_series[first_adx_index] = initial_adx
        prev_adx = initial_adx
        for idx in range(first_adx_index + 1, len(dx)):
            if math.isnan(dx[idx]):
                continue
            prev_adx = ((prev_adx * (period - 1)) + dx[idx]) / period
            adx_series[idx] = prev_adx

        current_adx = adx_series[-1]
        current_plus_di = plus_di[-1]
        current_minus_di = minus_di[-1]
        if math.isnan(current_adx) or math.isnan(current_plus_di) or math.isnan(current_minus_di):
            raise ValueError("current ADX unavailable")

        if current_adx < 20:
            strength = "weak"
        elif current_adx < 25:
            strength = "moderate"
        elif current_adx < 40:
            strength = "strong"
        else:
            strength = "very_strong"

        directional_signal = "bullish" if current_plus_di > current_minus_di else ("bearish" if current_plus_di < current_minus_di else "neutral")

        return {
            "status": "success",
            "data": {
                "adx": current_adx,
                "plus_di": current_plus_di,
                "minus_di": current_minus_di,
                "trend_strength": strength,
                "directional_signal": directional_signal,
                "adx_series": adx_series
            },
            "timestamp": datetime.now(timezone.utc).isoformat()
        }
    except (ValueError, TypeError, ZeroDivisionError) as e:
        logger.error(f"adx_calculator failed: {e}")
        _log_lesson(f"adx_calculator: {e}")
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
