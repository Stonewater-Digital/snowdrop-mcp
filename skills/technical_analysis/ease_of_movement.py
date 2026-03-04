"""
Execuve Summary: Calculates Ease of Movement (EMV) to show how easily price moves relative to volume.
Inputs: highs (list[float]), lows (list[float]), volumes (list[float]), period (int)
Outputs: emv_series (list[float]), signal_line (list[float]), current_emv (float), price_movement_efficiency (str)
MCP Tool Name: ease_of_movement
"""
import logging
import math
from datetime import datetime, timezone
from typing import Any

logger = logging.getLogger("snowdrop.skills")

TOOL_META = {
    "name": "ease_of_movement",
    "description": "Computes Richard Arms' Ease of Movement oscillator with SMA signal to judge efficient rallies/drops.",
    "inputSchema": {
        "type": "object",
        "properties": {
            "highs": {"type": "array", "description": "High prices."},
            "lows": {"type": "array", "description": "Low prices."},
            "volumes": {"type": "array", "description": "Volume per bar."},
            "period": {"type": "integer", "description": "SMA period for EMV signal (default 14)."}
        },
        "required": ["highs", "lows", "volumes", "period"]
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


def ease_of_movement(**kwargs: Any) -> dict:
    """Computes EMV = (Midpoint Move / Box Ratio) and smooths it by SMA."""
    try:
        highs = kwargs.get("highs")
        lows = kwargs.get("lows")
        volumes = kwargs.get("volumes")
        period = kwargs.get("period")

        for series in (highs, lows, volumes):
            if not isinstance(series, list) or len(series) < 2:
                raise ValueError("highs, lows, and volumes must be lists with at least two entries")
        if not isinstance(period, int) or period <= 1:
            raise ValueError("period must be integer > 1")
        if not (len(highs) == len(lows) == len(volumes)):
            raise ValueError("series must align")

        emv_series = [math.nan]
        for idx in range(1, len(highs)):
            h = float(highs[idx])
            l = float(lows[idx])
            prev_h = float(highs[idx - 1])
            prev_l = float(lows[idx - 1])
            volume = float(volumes[idx])
            midpoint_move = ((h + l) / 2) - ((prev_h + prev_l) / 2)
            box_ratio = (volume / 1_000_000) / (h - l) if (h - l) != 0 else 0.0
            emv = midpoint_move / box_ratio if box_ratio != 0 else 0.0
            emv_series.append(emv)

        signal_line = []
        for idx in range(len(emv_series)):
            if idx + 1 < period:
                signal_line.append(math.nan)
                continue
            window = [value for value in emv_series[idx - period + 1: idx + 1] if not math.isnan(value)]
            signal_line.append(sum(window) / len(window) if window else math.nan)

        current_emv = emv_series[-1]
        if math.isnan(current_emv):
            raise ValueError("insufficient data for EMV")
        if current_emv > 0 and signal_line[-1] > 0:
            efficiency = "uptrend_effortless"
        elif current_emv < 0 and signal_line[-1] < 0:
            efficiency = "downtrend_pressure"
        else:
            efficiency = "neutral"

        return {
            "status": "success",
            "data": {
                "emv_series": emv_series,
                "signal_line": signal_line,
                "current_emv": current_emv,
                "price_movement_efficiency": efficiency
            },
            "timestamp": datetime.now(timezone.utc).isoformat()
        }
    except (ValueError, TypeError, ZeroDivisionError) as e:
        logger.error(f"ease_of_movement failed: {e}")
        _log_lesson(f"ease_of_movement: {e}")
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
