"""
Execuve Summary: Derives MACD, signal, and histogram lines to diagnose momentum shifts.
Inputs: prices (list[float]), fast_period (int), slow_period (int), signal_period (int)
Outputs: macd_line (list[float]), signal_line (list[float]), histogram (list[float]), current_signal (str)
MCP Tool Name: macd_calculator
"""
import logging
import math
from datetime import datetime, timezone
from typing import Any

logger = logging.getLogger("snowdrop.skills")

TOOL_META = {
    "name": "macd_calculator",
    "description": "Computes Moving Average Convergence Divergence (12/26/9 defaults) with bullish/bearish interpretation.",
    "inputSchema": {
        "type": "object",
        "properties": {
            "prices": {
                "type": "array",
                "description": "Chronological list of closing prices."
            },
            "fast_period": {
                "type": "integer",
                "description": "Fast EMA lookback (default 12)."
            },
            "slow_period": {
                "type": "integer",
                "description": "Slow EMA lookback (default 26)."
            },
            "signal_period": {
                "type": "integer",
                "description": "Signal EMA lookback for MACD line (default 9)."
            }
        },
        "required": ["prices", "fast_period", "slow_period", "signal_period"]
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


def macd_calculator(**kwargs: Any) -> dict:
    """Implements Gerald Appel's MACD using EMA differentials and a nine-period signal line."""
    try:
        prices_raw = kwargs.get("prices")
        fast_period = kwargs.get("fast_period")
        slow_period = kwargs.get("slow_period")
        signal_period = kwargs.get("signal_period")

        if not isinstance(prices_raw, list) or len(prices_raw) < 2:
            raise ValueError("prices must be a list")
        prices = []
        for price in prices_raw:
            if not isinstance(price, (int, float)):
                raise TypeError("prices must be numeric")
            prices.append(float(price))

        for label, value in (("fast_period", fast_period), ("slow_period", slow_period), ("signal_period", signal_period)):
            if not isinstance(value, int) or value <= 0:
                raise ValueError(f"{label} must be a positive integer")

        if fast_period >= slow_period:
            raise ValueError("fast_period must be less than slow_period")
        if slow_period > len(prices):
            raise ValueError("slow_period cannot exceed price length")

        def _ema(series: list[float], period: int) -> list[float]:
            alpha = 2 / (period + 1)
            ema_values = [math.nan] * len(series)
            seed = sum(series[:period]) / period
            ema_values[period - 1] = seed
            ema_last = seed
            for idx in range(period, len(series)):
                ema_last = alpha * series[idx] + (1 - alpha) * ema_last
                ema_values[idx] = ema_last
            return ema_values

        fast_ema = _ema(prices, fast_period)
        slow_ema = _ema(prices, slow_period)
        macd_line = []
        for fast_val, slow_val in zip(fast_ema, slow_ema):
            if math.isnan(fast_val) or math.isnan(slow_val):
                macd_line.append(math.nan)
            else:
                macd_line.append(fast_val - slow_val)

        non_nan_indices = [idx for idx, value in enumerate(macd_line) if not math.isnan(value)]
        if len(non_nan_indices) < signal_period:
            raise ValueError("insufficient MACD points for signal line")

        signal_series = [math.nan] * len(macd_line)
        alpha_signal = 2 / (signal_period + 1)
        seed_indices = non_nan_indices[:signal_period]
        seed_values = [macd_line[idx] for idx in seed_indices]
        seed = sum(seed_values) / signal_period
        signal_series[seed_indices[-1]] = seed
        last_signal = seed
        for idx in non_nan_indices[signal_period:]:
            value = macd_line[idx]
            last_signal = alpha_signal * value + (1 - alpha_signal) * last_signal
            signal_series[idx] = last_signal

        histogram = []
        for macd_val, sig_val in zip(macd_line, signal_series):
            if math.isnan(macd_val) or math.isnan(sig_val):
                histogram.append(math.nan)
            else:
                histogram.append(macd_val - sig_val)

        current_macd = macd_line[-1]
        current_signal_value = signal_series[-1]
        current_hist = histogram[-1]
        if math.isnan(current_macd) or math.isnan(current_signal_value):
            raise ValueError("current MACD unavailable due to insufficient data")

        if current_macd > current_signal_value and current_hist > 0:
            current_signal_text = "bullish"
        elif current_macd < current_signal_value and current_hist < 0:
            current_signal_text = "bearish"
        else:
            current_signal_text = "neutral"

        prev_diff = macd_line[-2] - signal_series[-2] if not math.isnan(macd_line[-2]) and not math.isnan(signal_series[-2]) else 0.0
        curr_diff = current_macd - current_signal_value
        if curr_diff > 0 and prev_diff <= 0:
            crossover = "bullish_cross"
        elif curr_diff < 0 and prev_diff >= 0:
            crossover = "bearish_cross"
        else:
            crossover = "none"

        hist_trend = "increasing" if current_hist > histogram[-2] else ("decreasing" if current_hist < histogram[-2] else "flat")

        return {
            "status": "success",
            "data": {
                "macd_line": macd_line,
                "signal_line": signal_series,
                "histogram": histogram,
                "current_signal": current_signal_text,
                "crossover_detected": crossover,
                "histogram_divergence": hist_trend
            },
            "timestamp": datetime.now(timezone.utc).isoformat()
        }
    except (ValueError, TypeError, ZeroDivisionError) as e:
        logger.error(f"macd_calculator failed: {e}")
        _log_lesson(f"macd_calculator: {e}")
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
