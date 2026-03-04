"""
Execuve Summary: Calculates Martin Pring's Know Sure Thing oscillator from multiple smoothed ROCs.
Inputs: prices (list[float]), roc_periods (list[int]), sma_periods (list[int]), signal_period (int)
Outputs: kst_line (list[float]), signal_line (list[float]), histogram (list[float]), crossover_signal (str)
MCP Tool Name: know_sure_thing
"""
import logging
import math
from datetime import datetime, timezone
from typing import Any

logger = logging.getLogger("snowdrop.skills")

TOOL_META = {
    "name": "know_sure_thing",
    "description": "Implements Martin Pring's KST oscillator via four smoothed rate-of-change components.",
    "inputSchema": {
        "type": "object",
        "properties": {
            "prices": {"type": "array", "description": "Price series."},
            "roc_periods": {"type": "array", "description": "List of ROC lookbacks (e.g., [10,15,20,30])."},
            "sma_periods": {"type": "array", "description": "List of SMA smoothings for each ROC."},
            "signal_period": {"type": "integer", "description": "Signal SMA for KST (default 9)."}
        },
        "required": ["prices", "roc_periods", "sma_periods", "signal_period"]
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


def know_sure_thing(**kwargs: Any) -> dict:
    """Calculates KST = Σ w_i * SMA(ROC(period_i), sma_i) and a signal line for crossovers."""
    try:
        prices = kwargs.get("prices")
        roc_periods = kwargs.get("roc_periods")
        sma_periods = kwargs.get("sma_periods")
        signal_period = kwargs.get("signal_period")

        if not isinstance(prices, list) or len(prices) < 50:
            raise ValueError("prices list must be sufficiently long for KST")
        if not isinstance(roc_periods, list) or not isinstance(sma_periods, list):
            raise ValueError("roc_periods and sma_periods must be lists")
        if len(roc_periods) != 4 or len(sma_periods) != 4:
            raise ValueError("KST requires four ROC and SMA periods")
        if not isinstance(signal_period, int) or signal_period <= 0:
            raise ValueError("signal_period must be positive integer")

        prices_f = []
        for price in prices:
            if not isinstance(price, (int, float)):
                raise TypeError("prices must be numeric")
            prices_f.append(float(price))

        def _roc(period: int) -> list[float]:
            if not isinstance(period, int) or period <= 0:
                raise ValueError("roc periods must be positive integers")
            series = []
            for idx in range(len(prices_f)):
                if idx < period:
                    series.append(math.nan)
                    continue
                base = prices_f[idx - period]
                if base == 0:
                    series.append(math.nan)
                else:
                    series.append(((prices_f[idx] - base) / base) * 100)
            return series

        def _sma(series: list[float], period: int) -> list[float]:
            result = []
            window: list[float] = []
            for value in series:
                if math.isnan(value):
                    result.append(math.nan)
                    continue
                window.append(value)
                if len(window) > period:
                    window.pop(0)
                if len(window) == period:
                    result.append(sum(window) / period)
                else:
                    result.append(math.nan)
            return result

        weights = [1, 2, 3, 4]
        weighted_components = []
        for weight, roc_p, sma_p in zip(weights, roc_periods, sma_periods):
            roc_series = _roc(int(roc_p))
            smoothed = _sma(roc_series, int(sma_p))
            weighted_components.append([weight * value if not math.isnan(value) else math.nan for value in smoothed])

        kst_line = []
        for idx in range(len(prices_f)):
            values = [component[idx] for component in weighted_components if idx < len(component) and not math.isnan(component[idx])]
            if len(values) != 4:
                kst_line.append(math.nan)
            else:
                kst_line.append(sum(values))

        signal_line = _sma(kst_line, signal_period)
        current_kst = kst_line[-1]
        current_signal = signal_line[-1]
        if math.isnan(current_kst) or math.isnan(current_signal):
            raise ValueError("insufficient data for KST or signal line")

        histogram = []
        for kst_val, signal_val in zip(kst_line, signal_line):
            if math.isnan(kst_val) or math.isnan(signal_val):
                histogram.append(math.nan)
            else:
                histogram.append(kst_val - signal_val)

        crossover_signal = "neutral"
        prev_kst = next((v for v in reversed(kst_line[:-1]) if not math.isnan(v)), None)
        prev_signal = next((v for v in reversed(signal_line[:-1]) if not math.isnan(v)), None)
        if prev_kst is not None and prev_signal is not None:
            if current_kst > current_signal and prev_kst <= prev_signal:
                crossover_signal = "bullish"
            elif current_kst < current_signal and prev_kst >= prev_signal:
                crossover_signal = "bearish"

        return {
            "status": "success",
            "data": {
                "kst_line": kst_line,
                "signal_line": signal_line,
                "histogram": histogram,
                "crossover_signal": crossover_signal
            },
            "timestamp": datetime.now(timezone.utc).isoformat()
        }
    except (ValueError, TypeError, ZeroDivisionError) as e:
        logger.error(f"know_sure_thing failed: {e}")
        _log_lesson(f"know_sure_thing: {e}")
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
