"""
Execuve Summary: Computes the True Strength Index via double-smoothed momentum.
Inputs: prices (list[float]), long_period (int), short_period (int), signal_period (int)
Outputs: tsi_series (list[float]), signal_line (list[float]), current_tsi (float), crossover_signal (str), zero_line_cross (str)
MCP Tool Name: tsi_calculator
"""
import logging
import math
from datetime import datetime, timezone
from typing import Any

logger = logging.getLogger("snowdrop.skills")

TOOL_META = {
    "name": "tsi_calculator",
    "description": "Calculates William Blau's True Strength Index via double EMA of price momentum.",
    "inputSchema": {
        "type": "object",
        "properties": {
            "prices": {"type": "array", "description": "Price series (oldest first)."},
            "long_period": {"type": "integer", "description": "Long EMA period (e.g., 25)."},
            "short_period": {"type": "integer", "description": "Short EMA period (e.g., 13)."},
            "signal_period": {"type": "integer", "description": "Signal EMA on TSI (e.g., 7)."}
        },
        "required": ["prices", "long_period", "short_period", "signal_period"]
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


def tsi_calculator(**kwargs: Any) -> dict:
    """Follows William Blau's 1991 formulation: double EMA of momentum divided by double EMA of absolute momentum."""
    try:
        prices = kwargs.get("prices")
        long_period = kwargs.get("long_period")
        short_period = kwargs.get("short_period")
        signal_period = kwargs.get("signal_period")

        if not isinstance(prices, list) or len(prices) < 3:
            raise ValueError("prices must be a list with at least three points")
        for label, value in (("long_period", long_period), ("short_period", short_period), ("signal_period", signal_period)):
            if not isinstance(value, int) or value <= 0:
                raise ValueError(f"{label} must be positive integer")
        if short_period >= long_period:
            raise ValueError("short_period must be less than long_period for traditional TSI")

        prices_f = []
        for price in prices:
            if not isinstance(price, (int, float)):
                raise TypeError("prices must be numeric")
            prices_f.append(float(price))

        def _ema_from(series: list[float], period: int) -> list[float]:
            alpha = 2 / (period + 1)
            ema = [math.nan] * len(series)
            buffer: list[float] = []
            start_index = None
            for idx, value in enumerate(series):
                if math.isnan(value):
                    continue
                buffer.append(value)
                if len(buffer) == period:
                    seed = sum(buffer) / period
                    ema[idx] = seed
                    prev = seed
                    start_index = idx + 1
                    break
            if start_index is None:
                raise ValueError("insufficient data for EMA calculation")
            for idx in range(start_index, len(series)):
                value = series[idx]
                if math.isnan(value):
                    continue
                prev = alpha * value + (1 - alpha) * prev
                ema[idx] = prev
            return ema

        momentum = [math.nan]
        abs_momentum = [math.nan]
        for idx in range(1, len(prices_f)):
            move = prices_f[idx] - prices_f[idx - 1]
            momentum.append(move)
            abs_momentum.append(abs(move))

        ema_short_m = _ema_from(momentum, short_period)
        ema_short_abs = _ema_from(abs_momentum, short_period)
        ema_long_m = _ema_from(ema_short_m, long_period)
        ema_long_abs = _ema_from(ema_short_abs, long_period)

        tsi_series = []
        for mom_val, abs_val in zip(ema_long_m, ema_long_abs):
            if math.isnan(mom_val) or math.isnan(abs_val) or abs_val == 0:
                tsi_series.append(math.nan)
            else:
                tsi_series.append(100 * (mom_val / abs_val))

        signal_line = _ema_from(tsi_series, signal_period)
        current_tsi = tsi_series[-1]
        current_signal = signal_line[-1]
        if math.isnan(current_tsi) or math.isnan(current_signal):
            raise ValueError("insufficient data for TSI")

        crossover_signal = "neutral"
        prev_tsi = next((value for value in reversed(tsi_series[:-1]) if not math.isnan(value)), None)
        prev_signal = next((value for value in reversed(signal_line[:-1]) if not math.isnan(value)), None)
        if prev_tsi is not None and prev_signal is not None:
            if current_tsi > current_signal and prev_tsi <= prev_signal:
                crossover_signal = "bullish_cross"
            elif current_tsi < current_signal and prev_tsi >= prev_signal:
                crossover_signal = "bearish_cross"

        zero_line_cross = "none"
        prev_valid_tsi = prev_tsi if prev_tsi is not None else 0.0
        if current_tsi > 0 >= prev_valid_tsi:
            zero_line_cross = "bullish_zero_cross"
        elif current_tsi < 0 <= prev_valid_tsi:
            zero_line_cross = "bearish_zero_cross"

        return {
            "status": "success",
            "data": {
                "tsi_series": tsi_series,
                "signal_line": signal_line,
                "current_tsi": current_tsi,
                "crossover_signal": crossover_signal,
                "zero_line_cross": zero_line_cross
            },
            "timestamp": datetime.now(timezone.utc).isoformat()
        }
    except (ValueError, TypeError, ZeroDivisionError) as e:
        logger.error(f"tsi_calculator failed: {e}")
        _log_lesson(f"tsi_calculator: {e}")
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
