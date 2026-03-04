"""
Execuve Summary: Evaluates put/call volume and open-interest ratios for sentiment.
Inputs: put_volume (float), call_volume (float), put_oi (float), call_oi (float)
Outputs: volume_pcr (float), oi_pcr (float), signal (str), historical_context_note (str)
MCP Tool Name: put_call_ratio
"""
import logging
import math
from datetime import datetime, timezone
from typing import Any

logger = logging.getLogger("snowdrop.skills")

TOOL_META = {
    "name": "put_call_ratio",
    "description": "Tracks put/call ratios to identify fear vs greed sentiment zones.",
    "inputSchema": {
        "type": "object",
        "properties": {
            "put_volume": {"type": "number", "description": "Daily put volume."},
            "call_volume": {"type": "number", "description": "Daily call volume."},
            "put_oi": {"type": "number", "description": "Put open interest."},
            "call_oi": {"type": "number", "description": "Call open interest."}
        },
        "required": ["put_volume", "call_volume", "put_oi", "call_oi"]
    },
    "outputSchema": {
        "type": "object", "properties": {"status": {"type": "string"}, "timestamp": {"type": "string"}, "data": {"type": "object"}}, "required": ["status", "timestamp"]
    }
}


def put_call_ratio(**kwargs: Any) -> dict:
    """Calculates put/call ratios and assigns sentiment signal."""
    try:
        put_volume = kwargs.get("put_volume")
        call_volume = kwargs.get("call_volume")
        put_oi = kwargs.get("put_oi")
        call_oi = kwargs.get("call_oi")
        for label, value in (("put_volume", put_volume), ("call_volume", call_volume), ("put_oi", put_oi), ("call_oi", call_oi)):
            if not isinstance(value, (int, float)) or value < 0:
                raise ValueError(f"{label} must be non-negative number")

        volume_pcr = put_volume / call_volume if call_volume else math.inf
        oi_pcr = put_oi / call_oi if call_oi else math.inf
        signal = "neutral"
        hist_note = "within_normal_range"
        if volume_pcr > 1.3 or oi_pcr > 1.3:
            signal = "extreme_fear"
            hist_note = "far_above_average"
        elif volume_pcr < 0.7 or oi_pcr < 0.7:
            signal = "extreme_greed"
            hist_note = "far_below_average"
        elif volume_pcr > 1 or oi_pcr > 1:
            signal = "fear"
        elif volume_pcr < 0.9 or oi_pcr < 0.9:
            signal = "greed"

        return {
            "status": "success",
            "data": {
                "volume_pcr": volume_pcr,
                "oi_pcr": oi_pcr,
                "signal": signal,
                "historical_context_note": hist_note
            },
            "timestamp": datetime.now(timezone.utc).isoformat()
        }
    except (ValueError, TypeError, ZeroDivisionError) as e:
        logger.error(f"put_call_ratio failed: {e}")
        _log_lesson(f"put_call_ratio: {e}")
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
