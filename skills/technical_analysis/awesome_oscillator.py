"""
Execuve Summary: Computes the Awesome Oscillator (AO) to compare short and long-term momentum.
Inputs: highs (list[float]), lows (list[float])
Outputs: ao_series (list[float]), current_ao (float), saucer_signal (str), twin_peaks_signal (str), zero_line_cross (str), histogram_color (str)
MCP Tool Name: awesome_oscillator
"""
import logging
import math
from datetime import datetime, timezone
from typing import Any

logger = logging.getLogger("snowdrop.skills")

TOOL_META = {
    "name": "awesome_oscillator",
    "description": "Calculates Bill Williams' Awesome Oscillator using 5/34 SMA of median price to highlight momentum shifts.",
    "inputSchema": {
        "type": "object",
        "properties": {
            "highs": {"type": "array", "description": "High prices (oldest first)."},
            "lows": {"type": "array", "description": "Low prices aligned with highs."}
        },
        "required": ["highs", "lows"]
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


def awesome_oscillator(**kwargs: Any) -> dict:
    """Derives AO = SMA(median price,5) - SMA(median price,34) plus saucer and twin peaks patterns."""
    try:
        highs = kwargs.get("highs")
        lows = kwargs.get("lows")
        if not isinstance(highs, list) or not isinstance(lows, list):
            raise ValueError("highs and lows must be lists")
        if len(highs) != len(lows) or len(highs) < 34:
            raise ValueError("highs and lows must match and contain at least 34 points")

        median_prices = []
        for h, l in zip(highs, lows):
            if not isinstance(h, (int, float)) or not isinstance(l, (int, float)):
                raise TypeError("highs and lows must be numeric")
            median_prices.append((float(h) + float(l)) / 2)

        def _sma(values: list[float], period: int) -> list[float]:
            result = []
            window: list[float] = []
            total = 0.0
            for value in values:
                window.append(value)
                total += value
                if len(window) > period:
                    total -= window.pop(0)
                if len(window) == period:
                    result.append(total / period)
                else:
                    result.append(math.nan)
            return result

        sma5 = _sma(median_prices, 5)
        sma34 = _sma(median_prices, 34)
        ao_series = []
        for short, long_val in zip(sma5, sma34):
            if math.isnan(short) or math.isnan(long_val):
                ao_series.append(math.nan)
            else:
                ao_series.append(short - long_val)

        current_ao = ao_series[-1]
        previous_ao = ao_series[-2]
        if math.isnan(current_ao) or math.isnan(previous_ao):
            raise ValueError("insufficient data for AO")

        zero_line_cross = "none"
        if current_ao > 0 >= previous_ao:
            zero_line_cross = "bullish_zero_cross"
        elif current_ao < 0 <= previous_ao:
            zero_line_cross = "bearish_zero_cross"

        histogram_color = "green" if current_ao > previous_ao else ("red" if current_ao < previous_ao else "flat")

        saucer_signal = "none"
        if len(ao_series) >= 3:
            a, b, c = ao_series[-3], ao_series[-2], ao_series[-1]
            if not math.isnan(a) and not math.isnan(b) and not math.isnan(c):
                if c > b > a and a < b and c > 0:
                    saucer_signal = "bullish"
                elif c < b < a and a > b and c < 0:
                    saucer_signal = "bearish"

        twin_peaks_signal = "none"
        if len(ao_series) >= 6:
            peaks = []
            for idx in range(1, len(ao_series) - 1):
                value = ao_series[idx]
                if math.isnan(value):
                    continue
                if ao_series[idx - 1] < value and ao_series[idx + 1] < value:
                    peaks.append((idx, value))
            if len(peaks) >= 2:
                last_peak, prev_peak = peaks[-1], peaks[-2]
                if last_peak[1] > prev_peak[1] and last_peak[1] < 0 and prev_peak[1] < 0:
                    twin_peaks_signal = "bullish"
                elif last_peak[1] < prev_peak[1] and last_peak[1] > 0 and prev_peak[1] > 0:
                    twin_peaks_signal = "bearish"

        return {
            "status": "success",
            "data": {
                "ao_series": ao_series,
                "current_ao": current_ao,
                "saucer_signal": saucer_signal,
                "twin_peaks_signal": twin_peaks_signal,
                "zero_line_cross": zero_line_cross,
                "histogram_color": histogram_color
            },
            "timestamp": datetime.now(timezone.utc).isoformat()
        }
    except (ValueError, TypeError, ZeroDivisionError) as e:
        logger.error(f"awesome_oscillator failed: {e}")
        _log_lesson(f"awesome_oscillator: {e}")
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
