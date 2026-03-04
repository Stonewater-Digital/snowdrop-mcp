"""
Execuve Summary: Computes implied volatility rank and percentile.
Inputs: current_iv (float), historical_iv_series (list[float])
Outputs: iv_rank (float), iv_percentile (float), iv_high_52w (float), iv_low_52w (float), regime (str)
MCP Tool Name: volatility_rank_percentile
"""
import logging
import math
from datetime import datetime, timezone
from typing import Any

logger = logging.getLogger("snowdrop.skills")

TOOL_META = {
    "name": "volatility_rank_percentile",
    "description": "Calculates IV rank and percentile to understand volatility regimes.",
    "inputSchema": {
        "type": "object",
        "properties": {
            "current_iv": {"type": "number", "description": "Current implied volatility (decimal)."},
            "historical_iv_series": {"type": "array", "description": "History of implied vol values (>=252 observations)."}
        },
        "required": ["current_iv", "historical_iv_series"]
    },
    "outputSchema": {
        "type": "object", "properties": {"status": {"type": "string"}, "timestamp": {"type": "string"}, "data": {"type": "object"}}, "required": ["status", "timestamp"]
    }
}


def volatility_rank_percentile(**kwargs: Any) -> dict:
    """Computes IV rank and percentile to categorize volatility regime."""
    try:
        current_iv = kwargs.get("current_iv")
        history = kwargs.get("historical_iv_series")
        if not isinstance(current_iv, (int, float)):
            raise ValueError("current_iv must be numeric")
        if not isinstance(history, list) or len(history) == 0:
            raise ValueError("historical_iv_series must be non-empty list")
        iv_low = min(history)
        iv_high = max(history)
        iv_rank = (current_iv - iv_low) / (iv_high - iv_low) if iv_high != iv_low else 0.0
        sorted_history = sorted(history)
        iv_percentile = sum(1 for val in sorted_history if val <= current_iv) / len(sorted_history)
        if iv_rank > 0.75:
            regime = "extreme"
        elif iv_rank > 0.5:
            regime = "elevated"
        elif iv_rank > 0.25:
            regime = "normal"
        else:
            regime = "low"

        return {
            "status": "success",
            "data": {
                "iv_rank": iv_rank,
                "iv_percentile": iv_percentile,
                "iv_high_52w": iv_high,
                "iv_low_52w": iv_low,
                "regime": regime
            },
            "timestamp": datetime.now(timezone.utc).isoformat()
        }
    except (ValueError, TypeError, ZeroDivisionError) as e:
        logger.error(f"volatility_rank_percentile failed: {e}")
        _log_lesson(f"volatility_rank_percentile: {e}")
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
