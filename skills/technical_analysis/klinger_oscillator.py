"""
Execuve Summary: Computes the Klinger Volume Oscillator (KVO) to detect long-term money flow shifts.
Inputs: highs (list[float]), lows (list[float]), closes (list[float]), volumes (list[float]), fast (int), slow (int), signal (int)
Outputs: kvo_series (list[float]), signal_line (list[float]), histogram (list[float]), crossover_signal (str), trend_confirmation (str)
MCP Tool Name: klinger_oscillator
"""
import logging
import math
from datetime import datetime, timezone
from typing import Any

logger = logging.getLogger("snowdrop.skills")

TOOL_META = {
    "name": "klinger_oscillator",
    "description": "Implements the Klinger Volume Oscillator (fast/slow EMAs of volume force) with signal histogram.",
    "inputSchema": {
        "type": "object",
        "properties": {
            "highs": {"type": "array", "description": "High prices."},
            "lows": {"type": "array", "description": "Low prices."},
            "closes": {"type": "array", "description": "Close prices."},
            "volumes": {"type": "array", "description": "Volume data."},
            "fast": {"type": "integer", "description": "Fast EMA length (34)."},
            "slow": {"type": "integer", "description": "Slow EMA length (55)."},
            "signal": {"type": "integer", "description": "Signal EMA length (13)."}
        },
        "required": ["highs", "lows", "closes", "volumes", "fast", "slow", "signal"]
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


def klinger_oscillator(**kwargs: Any) -> dict:
    """Calculates volume force based on trend direction and applies fast/slow EMAs for the KVO."""
    try:
        highs = kwargs.get("highs")
        lows = kwargs.get("lows")
        closes = kwargs.get("closes")
        volumes = kwargs.get("volumes")
        fast = kwargs.get("fast")
        slow = kwargs.get("slow")
        signal = kwargs.get("signal")

        for series in (highs, lows, closes, volumes):
            if not isinstance(series, list) or len(series) < 2:
                raise ValueError("price and volume series must be lists")
        if not (len(highs) == len(lows) == len(closes) == len(volumes)):
            raise ValueError("series must align")
        for label, value in (("fast", fast), ("slow", slow), ("signal", signal)):
            if not isinstance(value, int) or value <= 1:
                raise ValueError(f"{label} must be integer > 1")
        if fast >= slow:
            raise ValueError("fast period must be less than slow period")

        volume_force = [math.nan]
        prev_trend = 0
        prev_typical = (float(highs[0]) + float(lows[0]) + float(closes[0])) / 3
        for idx in range(1, len(highs)):
            typical = (float(highs[idx]) + float(lows[idx]) + float(closes[idx])) / 3
            volume = float(volumes[idx])
            if typical > prev_typical:
                trend = 1
            elif typical < prev_typical:
                trend = -1
            else:
                trend = prev_trend
            prev_trend = trend if trend != 0 else prev_trend
            if typical + prev_typical == 0:
                vf_component = 0.0
            else:
                vf_component = 2 * (typical - prev_typical) / (typical + prev_typical)
            volume_force.append(volume * vf_component * (prev_trend or 1))
            prev_typical = typical

        fast_ema = _ema(volume_force, fast)
        slow_ema = _ema(volume_force, slow)
        kvo_series = []
        for fast_val, slow_val in zip(fast_ema, slow_ema):
            if math.isnan(fast_val) or math.isnan(slow_val):
                kvo_series.append(math.nan)
            else:
                kvo_series.append(fast_val - slow_val)

        signal_line = _ema(kvo_series, signal)
        histogram = []
        for kvo, sig in zip(kvo_series, signal_line):
            if math.isnan(kvo) or math.isnan(sig):
                histogram.append(math.nan)
            else:
                histogram.append(kvo - sig)

        current_kvo = kvo_series[-1]
        current_signal = signal_line[-1]
        if math.isnan(current_kvo) or math.isnan(current_signal):
            raise ValueError("insufficient data for KVO")

        crossover_signal = "neutral"
        prev_kvo = next((value for value in reversed(kvo_series[:-1]) if not math.isnan(value)), None)
        prev_sig = next((value for value in reversed(signal_line[:-1]) if not math.isnan(value)), None)
        if prev_kvo is not None and prev_sig is not None:
            if current_kvo > current_signal and prev_kvo <= prev_sig:
                crossover_signal = "bullish"
            elif current_kvo < current_signal and prev_kvo >= prev_sig:
                crossover_signal = "bearish"

        trend_confirmation = "confirming" if current_kvo > 0 else "weakening"
        if current_kvo > 0 and histogram[-1] > 0:
            trend_confirmation = "bullish_confirmation"
        elif current_kvo < 0 and histogram[-1] < 0:
            trend_confirmation = "bearish_confirmation"

        return {
            "status": "success",
            "data": {
                "kvo_series": kvo_series,
                "signal_line": signal_line,
                "histogram": histogram,
                "crossover_signal": crossover_signal,
                "trend_confirmation": trend_confirmation
            },
            "timestamp": datetime.now(timezone.utc).isoformat()
        }
    except (ValueError, TypeError, ZeroDivisionError) as e:
        logger.error(f"klinger_oscillator failed: {e}")
        _log_lesson(f"klinger_oscillator: {e}")
        return {
            "status": "error",
            "error": str(e),
            "timestamp": datetime.now(timezone.utc).isoformat()
        }


def _ema(values: list[float], period: int) -> list[float]:
    ema = [math.nan] * len(values)
    valid = [value for value in values if not math.isnan(value)]
    if len(valid) < period:
        return ema
    alpha = 2 / (period + 1)
    seed = sum(valid[:period]) / period
    first_index = values.index(valid[period - 1])
    ema[first_index] = seed
    prev = seed
    for idx in range(first_index + 1, len(values)):
        value = values[idx]
        if math.isnan(value):
            continue
        prev = alpha * value + (1 - alpha) * prev
        ema[idx] = prev
    return ema


def _log_lesson(message: str) -> None:
    try:
        with open("logs/lessons.md", "a") as f:
            f.write(f"- [{datetime.now(timezone.utc).isoformat()}] {message}\n")
    except OSError:
        pass
