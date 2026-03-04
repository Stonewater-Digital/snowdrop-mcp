"""
Execuve Summary: Detects divergences between price and an indicator series.
Inputs: prices (list[float]), indicator_values (list[float]), lookback (int)
Outputs: divergences (list of dicts)
MCP Tool Name: divergence_detector
"""
import logging
import math
from datetime import datetime, timezone
from typing import Any

logger = logging.getLogger("snowdrop.skills")

TOOL_META = {
    "name": "divergence_detector",
    "description": "Identifies regular and hidden divergences between price action and an oscillator/indicator.",
    "inputSchema": {
        "type": "object",
        "properties": {
            "prices": {"type": "array", "description": "Price series."},
            "indicator_values": {"type": "array", "description": "Indicator series aligned with prices."},
            "lookback": {"type": "integer", "description": "Window used to search for pivots."}
        },
        "required": ["prices", "indicator_values", "lookback"]
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


def divergence_detector(**kwargs: Any) -> dict:
    """Compares pivot highs/lows in price versus indicator to flag divergences."""
    try:
        prices = kwargs.get("prices")
        indicator_values = kwargs.get("indicator_values")
        lookback = kwargs.get("lookback")

        if not isinstance(prices, list) or not isinstance(indicator_values, list):
            raise ValueError("prices and indicator_values must be lists")
        if len(prices) != len(indicator_values):
            raise ValueError("series must align")
        if len(prices) < lookback or lookback < 3:
            raise ValueError("lookback must be at least 3 and less than series length")

        prices_f = [float(value) for value in prices]
        indicator_f = [float(value) for value in indicator_values]
        start_index = len(prices_f) - lookback
        price_section = prices_f[start_index:]
        indicator_section = indicator_f[start_index:]

        price_highs = _find_pivots(price_section, mode="high")
        price_lows = _find_pivots(price_section, mode="low")
        indicator_highs = _find_pivots(indicator_section, mode="high")
        indicator_lows = _find_pivots(indicator_section, mode="low")

        divergences = []
        if len(price_highs) >= 2 and len(indicator_highs) >= 2:
            p1, p2 = price_highs[-2], price_highs[-1]
            i1, i2 = indicator_highs[-2], indicator_highs[-1]
            if p2[1] > p1[1] and i2[1] < i1[1]:
                divergences.append({
                    "type": "regular_bearish",
                    "start_index": start_index + p1[0],
                    "end_index": start_index + p2[0],
                    "strength": abs((i2[1] - i1[1]) / (p2[1] - p1[1] or 1e-9))
                })
            if p2[1] < p1[1] and i2[1] > i1[1]:
                divergences.append({
                    "type": "hidden_bullish",
                    "start_index": start_index + p1[0],
                    "end_index": start_index + p2[0],
                    "strength": abs((i2[1] - i1[1]) / (p2[1] - p1[1] or 1e-9))
                })
        if len(price_lows) >= 2 and len(indicator_lows) >= 2:
            p1, p2 = price_lows[-2], price_lows[-1]
            i1, i2 = indicator_lows[-2], indicator_lows[-1]
            if p2[1] < p1[1] and i2[1] > i1[1]:
                divergences.append({
                    "type": "regular_bullish",
                    "start_index": start_index + p1[0],
                    "end_index": start_index + p2[0],
                    "strength": abs((i2[1] - i1[1]) / (p2[1] - p1[1] or 1e-9))
                })
            if p2[1] > p1[1] and i2[1] < i1[1]:
                divergences.append({
                    "type": "hidden_bearish",
                    "start_index": start_index + p1[0],
                    "end_index": start_index + p2[0],
                    "strength": abs((i2[1] - i1[1]) / (p2[1] - p1[1] or 1e-9))
                })

        return {
            "status": "success",
            "data": {
                "divergences": divergences
            },
            "timestamp": datetime.now(timezone.utc).isoformat()
        }
    except (ValueError, TypeError, ZeroDivisionError) as e:
        logger.error(f"divergence_detector failed: {e}")
        _log_lesson(f"divergence_detector: {e}")
        return {
            "status": "error",
            "error": str(e),
            "timestamp": datetime.now(timezone.utc).isoformat()
        }


def _find_pivots(values: list[float], mode: str) -> list[tuple[int, float]]:
    pivots = []
    for idx in range(1, len(values) - 1):
        if mode == "high" and values[idx] >= values[idx - 1] and values[idx] >= values[idx + 1]:
            pivots.append((idx, values[idx]))
        if mode == "low" and values[idx] <= values[idx - 1] and values[idx] <= values[idx + 1]:
            pivots.append((idx, values[idx]))
    return pivots


def _log_lesson(message: str) -> None:
    try:
        with open("logs/lessons.md", "a") as f:
            f.write(f"- [{datetime.now(timezone.utc).isoformat()}] {message}\n")
    except OSError:
        pass
