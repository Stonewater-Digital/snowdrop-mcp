"""
Execuve Summary: Computes a mean-reversion z-score and half-life estimate.
Inputs: prices (list[float]), lookback (int), z_threshold (float)
Outputs: current_z_score (float), mean (float), std (float), percentile (float), signal (str), half_life_estimate (float)
MCP Tool Name: mean_reversion_score
"""
import logging
import math
from datetime import datetime, timezone
from typing import Any

logger = logging.getLogger("snowdrop.skills")

TOOL_META = {
    "name": "mean_reversion_score",
    "description": "Computes z-score of price versus rolling mean and estimates Ornstein-Uhlenbeck half-life.",
    "inputSchema": {
        "type": "object",
        "properties": {
            "prices": {"type": "array", "description": "Price series."},
            "lookback": {"type": "integer", "description": "Lookback window for mean/std."},
            "z_threshold": {"type": "number", "description": "Z-score trigger for signals."}
        },
        "required": ["prices", "lookback", "z_threshold"]
    },
    "outputSchema": {
        "type": "object", "properties": {"status": {"type": "string"}, "timestamp": {"type": "string"}, "data": {"type": "object"}}, "required": ["status", "timestamp"]
    }
}


def mean_reversion_score(**kwargs: Any) -> dict:
    """Computes z-score and mean reversion half-life."""
    try:
        prices = kwargs.get("prices")
        lookback = kwargs.get("lookback")
        z_threshold = kwargs.get("z_threshold")
        if not isinstance(prices, list) or len(prices) < lookback:
            raise ValueError("prices must be at least as long as lookback")
        if not isinstance(lookback, int) or lookback <= 1:
            raise ValueError("lookback must be integer > 1")
        if not isinstance(z_threshold, (int, float)):
            raise ValueError("z_threshold must be numeric")

        window = prices[-lookback:]
        mean_val = sum(window) / lookback
        variance = sum((price - mean_val) ** 2 for price in window) / (lookback - 1)
        std_dev = math.sqrt(variance)
        current_z = (window[-1] - mean_val) / std_dev if std_dev else math.inf
        percentile = sum(1 for price in window if price <= window[-1]) / lookback
        if current_z >= z_threshold:
            signal = "overbought"
        elif current_z <= -z_threshold:
            signal = "oversold"
        else:
            signal = "neutral"

        half_life = _estimate_half_life(window)

        return {
            "status": "success",
            "data": {
                "current_z_score": current_z,
                "mean": mean_val,
                "std": std_dev,
                "percentile": percentile,
                "signal": signal,
                "half_life_estimate": half_life
            },
            "timestamp": datetime.now(timezone.utc).isoformat()
        }
    except (ValueError, TypeError, ZeroDivisionError) as e:
        logger.error(f"mean_reversion_score failed: {e}")
        _log_lesson(f"mean_reversion_score: {e}")
        return {
            "status": "error",
            "error": str(e),
            "timestamp": datetime.now(timezone.utc).isoformat()
        }


def _estimate_half_life(prices: list[float]) -> float:
    x = prices[:-1]
    y = prices[1:]
    mean_x = sum(x) / len(x)
    mean_y = sum(y) / len(y)
    numerator = sum((xi - mean_x) * (yi - mean_y) for xi, yi in zip(x, y))
    denominator = sum((xi - mean_x) ** 2 for xi in x)
    beta = numerator / denominator if denominator else 0
    if beta >= 1:
        return math.inf
    try:
        half_life = -math.log(2) / math.log(beta) if beta > 0 else math.inf
    except ValueError:
        half_life = math.inf
    return half_life


def _log_lesson(message: str) -> None:
    try:
        with open("logs/lessons.md", "a") as f:
            f.write(f"- [{datetime.now(timezone.utc).isoformat()}] {message}\n")
    except OSError:
        pass
