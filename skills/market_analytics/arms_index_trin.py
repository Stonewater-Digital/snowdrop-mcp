"""
Execuve Summary: Calculates the Arms Index (TRIN) for short-term breadth.
Inputs: advances (list[int]), declines (list[int]), advancing_volume (list[float]), declining_volume (list[float])
Outputs: trin (list[float]), signal (str), 10day_trin (float)
MCP Tool Name: arms_index_trin
"""
import logging
import math
from datetime import datetime, timezone
from typing import Any

logger = logging.getLogger("snowdrop.skills")

TOOL_META = {
    "name": "arms_index_trin",
    "description": "Computes TRIN as (Adv/Dec)/(AdvVol/DecVol) and averages it to identify overbought/oversold.",
    "inputSchema": {
        "type": "object",
        "properties": {
            "advances": {"type": "array", "description": "Advancing issues."},
            "declines": {"type": "array", "description": "Declining issues."},
            "advancing_volume": {"type": "array", "description": "Volume in advancers."},
            "declining_volume": {"type": "array", "description": "Volume in decliners."}
        },
        "required": ["advances", "declines", "advancing_volume", "declining_volume"]
    },
    "outputSchema": {
        "type": "object", "properties": {"status": {"type": "string"}, "timestamp": {"type": "string"}, "data": {"type": "object"}}, "required": ["status", "timestamp"]
    }
}


def arms_index_trin(**kwargs: Any) -> dict:
    """Calculates TRIN series and a 10-day average."""
    try:
        advances = kwargs.get("advances")
        declines = kwargs.get("declines")
        adv_vol = kwargs.get("advancing_volume")
        dec_vol = kwargs.get("declining_volume")
        if not all(isinstance(series, list) for series in (advances, declines, adv_vol, dec_vol)):
            raise ValueError("all inputs must be lists")
        if not (len(advances) == len(declines) == len(adv_vol) == len(dec_vol)):
            raise ValueError("series must align in length")

        trin_series = []
        for a, d, av, dv in zip(advances, declines, adv_vol, dec_vol):
            numerator = (a / d) if d else math.inf
            denominator = (av / dv) if dv else math.inf
            trin_value = numerator / denominator if denominator else math.inf
            trin_series.append(trin_value)
        window = trin_series[-10:] if len(trin_series) >= 10 else trin_series
        trin_10day = sum(window) / len(window)
        latest_trin = trin_series[-1]
        if latest_trin < 0.8:
            signal = "oversold_bounce"
        elif latest_trin > 1.2:
            signal = "overbought_risk"
        else:
            signal = "neutral"

        return {
            "status": "success",
            "data": {
                "trin": trin_series,
                "signal": signal,
                "10day_trin": trin_10day
            },
            "timestamp": datetime.now(timezone.utc).isoformat()
        }
    except (ValueError, TypeError, ZeroDivisionError) as e:
        logger.error(f"arms_index_trin failed: {e}")
        _log_lesson(f"arms_index_trin: {e}")
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
