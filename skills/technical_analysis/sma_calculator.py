"""
Execuve Summary: Computes simple moving averages to gauge price trends.
Inputs: prices (list[float]), period (int)
Outputs: sma_series (dict), current_sma (float), price_vs_sma (str), pct_from_sma (float)
MCP Tool Name: sma_calculator
"""
import logging
import math
from datetime import datetime, timezone
from typing import Any

logger = logging.getLogger("snowdrop.skills")

TOOL_META = {
    "name": "sma_calculator",
    "description": "Calculates rolling simple moving averages to identify price alignment with key trend periods.",
    "inputSchema": {
        "type": "object",
        "properties": {
            "prices": {
                "type": "array",
                "description": "Chronological list of closing prices (oldest first)."
            },
            "period": {
                "type": "integer",
                "description": "Primary SMA lookback period (e.g., 20)."
            }
        },
        "required": ["prices", "period"]
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


def sma_calculator(**kwargs: Any) -> dict:
    """Uses arithmetic means across multiple horizons to compare price versus trend baselines."""
    try:
        prices_raw = kwargs.get("prices")
        period = kwargs.get("period")

        if not isinstance(prices_raw, list) or len(prices_raw) < 2:
            raise ValueError("prices must be a non-empty list of floats")
        prices = []
        for value in prices_raw:
            if not isinstance(value, (int, float)):
                raise TypeError("prices must contain numeric values")
            prices.append(float(value))

        if not isinstance(period, int) or period <= 0:
            raise ValueError("period must be a positive integer")
        if period > len(prices):
            raise ValueError("period cannot exceed number of price points")

        comparison_periods = sorted({period, 20, 50, 200})
        sma_series: dict[str, list[float]] = {}

        def _rolling_sma(window: int) -> list[float]:
            window_values: list[float] = []
            output: list[float] = []
            running_sum = 0.0
            for idx, price in enumerate(prices):
                window_values.append(price)
                running_sum += price
                if len(window_values) > window:
                    running_sum -= window_values.pop(0)
                if idx + 1 >= window:
                    output.append(running_sum / window)
                else:
                    output.append(math.nan)
            return output

        for comp_period in comparison_periods:
            sma_series[str(comp_period)] = _rolling_sma(comp_period)

        current_price = prices[-1]
        current_sma = sma_series[str(period)][-1]
        if math.isnan(current_sma):
            raise ValueError("insufficient data for requested SMA period")

        price_vs_sma = "above" if current_price > current_sma else ("below" if current_price < current_sma else "at")
        pct_from_sma = ((current_price - current_sma) / current_sma) * 100 if current_sma != 0 else math.inf

        multi_snapshot = {}
        for comp_period in comparison_periods:
            series = sma_series[str(comp_period)]
            latest = series[-1]
            if math.isnan(latest):
                status = "insufficient"
                diff_pct = None
            else:
                status = "above" if current_price > latest else ("below" if current_price < latest else "at")
                diff_pct = ((current_price - latest) / latest) * 100 if latest else math.inf
            multi_snapshot[str(comp_period)] = {
                "latest_sma": latest,
                "price_relation": status,
                "pct_from_sma": diff_pct
            }

        return {
            "status": "success",
            "data": {
                "sma_series": sma_series,
                "current_sma": current_sma,
                "price_vs_sma": price_vs_sma,
                "pct_from_sma": pct_from_sma,
                "multi_period_snapshot": multi_snapshot,
                "latest_price": current_price
            },
            "timestamp": datetime.now(timezone.utc).isoformat()
        }
    except (ValueError, TypeError, ZeroDivisionError) as e:
        logger.error(f"sma_calculator failed: {e}")
        _log_lesson(f"sma_calculator: {e}")
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
