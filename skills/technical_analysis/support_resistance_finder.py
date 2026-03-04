"""
Execuve Summary: Detects support and resistance levels based on repeated pivot touches.
Inputs: highs (list[float]), lows (list[float]), closes (list[float]), lookback (int), num_touches_required (int)
Outputs: support_levels (list), resistance_levels (list), current_nearest_support (float|None), current_nearest_resistance (float|None)
MCP Tool Name: support_resistance_finder
"""
import logging
import math
from datetime import datetime, timezone
from typing import Any

logger = logging.getLogger("snowdrop.skills")

TOOL_META = {
    "name": "support_resistance_finder",
    "description": "Finds price levels with multiple touches using swing highs/lows within a lookback window.",
    "inputSchema": {
        "type": "object",
        "properties": {
            "highs": {"type": "array", "description": "High prices (oldest first)."},
            "lows": {"type": "array", "description": "Low prices."},
            "closes": {"type": "array", "description": "Close prices."},
            "lookback": {"type": "integer", "description": "Bars to inspect on each side for pivots."},
            "num_touches_required": {"type": "integer", "description": "Minimum touches to validate a level."}
        },
        "required": ["highs", "lows", "closes", "lookback", "num_touches_required"]
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


def support_resistance_finder(**kwargs: Any) -> dict:
    """Identifies pivot highs/lows and clusters them into support/resistance zones."""
    try:
        highs = kwargs.get("highs")
        lows = kwargs.get("lows")
        closes = kwargs.get("closes")
        lookback = kwargs.get("lookback")
        num_touches_required = kwargs.get("num_touches_required")

        for series in (highs, lows, closes):
            if not isinstance(series, list) or len(series) < 2:
                raise ValueError("price series must be lists with at least two entries")
        if not (len(highs) == len(lows) == len(closes)):
            raise ValueError("series must align")
        for label, value in (("lookback", lookback), ("num_touches_required", num_touches_required)):
            if not isinstance(value, int) or value <= 0:
                raise ValueError(f"{label} must be positive integer")

        avg_range = sum(float(h) - float(l) for h, l in zip(highs, lows)) / len(highs)
        tolerance = avg_range * 0.5 if avg_range > 0 else 0.5

        support_candidates = []
        resistance_candidates = []
        for idx in range(lookback, len(closes) - lookback):
            window_highs = highs[idx - lookback: idx + lookback + 1]
            window_lows = lows[idx - lookback: idx + lookback + 1]
            current_low = lows[idx]
            current_high = highs[idx]
            if current_low == min(window_lows):
                support_candidates.append(float(current_low))
            if current_high == max(window_highs):
                resistance_candidates.append(float(current_high))

        def _cluster(levels: list[float]) -> list[dict[str, float]]:
            clusters: list[list[float]] = []
            for level in sorted(levels):
                placed = False
                for cluster in clusters:
                    if abs(level - sum(cluster) / len(cluster)) <= tolerance:
                        cluster.append(level)
                        placed = True
                        break
                if not placed:
                    clusters.append([level])
            cluster_info = []
            for cluster in clusters:
                strength = len(cluster)
                price_level = sum(cluster) / len(cluster)
                if strength >= num_touches_required:
                    cluster_info.append({"level": price_level, "strength": strength})
            return sorted(cluster_info, key=lambda item: item["level"])

        support_levels = _cluster(support_candidates)
        resistance_levels = _cluster(resistance_candidates)
        latest_close = closes[-1]

        def _nearest(levels: list[dict[str, float]], target: float, direction: str) -> float | None:
            if not levels:
                return None
            if direction == "support":
                below = [level["level"] for level in levels if level["level"] <= target]
                return max(below) if below else None
            above = [level["level"] for level in levels if level["level"] >= target]
            return min(above) if above else None

        nearest_support = _nearest(support_levels, latest_close, "support")
        nearest_resistance = _nearest(resistance_levels, latest_close, "resistance")

        return {
            "status": "success",
            "data": {
                "support_levels": support_levels,
                "resistance_levels": resistance_levels,
                "current_nearest_support": nearest_support,
                "current_nearest_resistance": nearest_resistance,
                "tolerance": tolerance
            },
            "timestamp": datetime.now(timezone.utc).isoformat()
        }
    except (ValueError, TypeError, ZeroDivisionError) as e:
        logger.error(f"support_resistance_finder failed: {e}")
        _log_lesson(f"support_resistance_finder: {e}")
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
