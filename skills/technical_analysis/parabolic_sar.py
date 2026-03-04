"""
Execuve Summary: Calculates Parabolic SAR to trail price extremes and flag reversals.
Inputs: highs (list[float]), lows (list[float]), closes (list[float]), af_start (float), af_step (float), af_max (float)
Outputs: sar_series (list[float]), current_trend (str), reversals (list[int]), current_stop_level (float)
MCP Tool Name: parabolic_sar
"""
import logging
import math
from datetime import datetime, timezone
from typing import Any

logger = logging.getLogger("snowdrop.skills")

TOOL_META = {
    "name": "parabolic_sar",
    "description": "Implements Welles Wilder's Parabolic SAR with configurable acceleration factors to trail price trends.",
    "inputSchema": {
        "type": "object",
        "properties": {
            "highs": {"type": "array", "description": "Session highs, chronological."},
            "lows": {"type": "array", "description": "Session lows aligned with highs."},
            "closes": {"type": "array", "description": "Closing prices used to infer initial trend."},
            "af_start": {"type": "number", "description": "Initial acceleration factor (default 0.02)."},
            "af_step": {"type": "number", "description": "Step increment when new extremes are set."},
            "af_max": {"type": "number", "description": "Maximum acceleration factor cap."}
        },
        "required": ["highs", "lows", "closes", "af_start", "af_step", "af_max"]
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


def parabolic_sar(**kwargs: Any) -> dict:
    """Applies Wilder's Parabolic Stop-and-Reverse using acceleration toward the extreme price."""
    try:
        highs = kwargs.get("highs")
        lows = kwargs.get("lows")
        closes = kwargs.get("closes")
        af_start = kwargs.get("af_start")
        af_step = kwargs.get("af_step")
        af_max = kwargs.get("af_max")

        for series_name, series in (("highs", highs), ("lows", lows), ("closes", closes)):
            if not isinstance(series, list) or len(series) < 2:
                raise ValueError(f"{series_name} must be a list with at least two elements")
        if not (len(highs) == len(lows) == len(closes)):
            raise ValueError("highs, lows, and closes must share the same length")

        highs_clean = []
        lows_clean = []
        closes_clean = []
        for idx in range(len(highs)):
            h = highs[idx]
            l = lows[idx]
            c = closes[idx]
            if not isinstance(h, (int, float)) or not isinstance(l, (int, float)) or not isinstance(c, (int, float)):
                raise TypeError("price series must contain numbers")
            highs_clean.append(float(h))
            lows_clean.append(float(l))
            closes_clean.append(float(c))

        for label, value in (("af_start", af_start), ("af_step", af_step), ("af_max", af_max)):
            if not isinstance(value, (int, float)) or value <= 0:
                raise ValueError(f"{label} must be a positive number")

        if af_start > af_max:
            raise ValueError("af_start cannot exceed af_max")

        trend = "up" if closes_clean[1] >= closes_clean[0] else "down"
        sar_values = [lows_clean[0] if trend == "up" else highs_clean[0]]
        extreme = max(highs_clean[:2]) if trend == "up" else min(lows_clean[:2])
        af = af_start
        reversal_points: list[int] = []

        for idx in range(1, len(highs_clean)):
            prior_sar = sar_values[-1]
            sar = prior_sar + af * (extreme - prior_sar)
            if trend == "up":
                sar = min(sar, lows_clean[idx - 1], lows_clean[idx])
                if highs_clean[idx] > extreme:
                    extreme = highs_clean[idx]
                    af = min(af + af_step, af_max)
                if sar >= lows_clean[idx]:
                    trend = "down"
                    sar = extreme
                    extreme = lows_clean[idx]
                    af = af_start
                    reversal_points.append(idx)
            else:
                sar = max(sar, highs_clean[idx - 1], highs_clean[idx])
                if lows_clean[idx] < extreme:
                    extreme = lows_clean[idx]
                    af = min(af + af_step, af_max)
                if sar <= highs_clean[idx]:
                    trend = "up"
                    sar = extreme
                    extreme = highs_clean[idx]
                    af = af_start
                    reversal_points.append(idx)
            sar_values.append(sar)

        current_stop = sar_values[-1]
        return {
            "status": "success",
            "data": {
                "sar_series": sar_values,
                "current_trend": trend,
                "reversals": reversal_points,
                "current_stop_level": current_stop,
                "acceleration_factor": af
            },
            "timestamp": datetime.now(timezone.utc).isoformat()
        }
    except (ValueError, TypeError, ZeroDivisionError) as e:
        logger.error(f"parabolic_sar failed: {e}")
        _log_lesson(f"parabolic_sar: {e}")
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
