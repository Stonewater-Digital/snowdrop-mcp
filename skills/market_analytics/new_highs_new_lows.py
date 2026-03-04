"""
Execuve Summary: Measures breadth using new highs minus new lows.
Inputs: new_highs (list[int]), new_lows (list[int])
Outputs: nh_nl_diff (list[float]), nh_nl_ratio (float), 10day_ma (float), signal (str), market_regime (str)
MCP Tool Name: new_highs_new_lows
"""
import logging
import math
from datetime import datetime, timezone
from typing import Any

logger = logging.getLogger("snowdrop.skills")

TOOL_META = {
    "name": "new_highs_new_lows",
    "description": "Computes new-high minus new-low series, ratios, and signals.",
    "inputSchema": {
        "type": "object",
        "properties": {
            "new_highs": {"type": "array", "description": "Counts of new highs."},
            "new_lows": {"type": "array", "description": "Counts of new lows."}
        },
        "required": ["new_highs", "new_lows"]
    },
    "outputSchema": {
        "type": "object", "properties": {"status": {"type": "string"}, "timestamp": {"type": "string"}, "data": {"type": "object"}}, "required": ["status", "timestamp"]
    }
}


def new_highs_new_lows(**kwargs: Any) -> dict:
    """Computes NH-NL diff, ratios, and regime signals."""
    try:
        highs = kwargs.get("new_highs")
        lows = kwargs.get("new_lows")
        if not isinstance(highs, list) or not isinstance(lows, list) or len(highs) != len(lows):
            raise ValueError("new_highs/new_lows must be equal-length lists")
        diff_series = []
        ratio = 0.0
        for h, l in zip(highs, lows):
            if not isinstance(h, (int, float)) or not isinstance(l, (int, float)):
                raise TypeError("inputs must be numeric")
            diff_series.append(float(h) - float(l))
            ratio = (float(h) + 1) / (float(l) + 1)
        window = diff_series[-10:] if len(diff_series) >= 10 else diff_series
        ma10 = sum(window) / len(window)
        signal = "bullish" if diff_series[-1] > 0 else ("bearish" if diff_series[-1] < 0 else "neutral")
        if ratio > 2:
            regime = "breakout"
        elif ratio < 0.5:
            regime = "breakdown"
        else:
            regime = "balanced"

        return {
            "status": "success",
            "data": {
                "nh_nl_diff": diff_series,
                "nh_nl_ratio": ratio,
                "10day_ma": ma10,
                "signal": signal,
                "market_regime": regime
            },
            "timestamp": datetime.now(timezone.utc).isoformat()
        }
    except (ValueError, TypeError, ZeroDivisionError) as e:
        logger.error(f"new_highs_new_lows failed: {e}")
        _log_lesson(f"new_highs_new_lows: {e}")
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
