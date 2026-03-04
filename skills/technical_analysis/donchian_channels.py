"""
Execuve Summary: Computes Donchian Channels to track breakouts beyond highest highs or lowest lows.
Inputs: highs (list[float]), lows (list[float]), period (int)
Outputs: upper_channel (float), lower_channel (float), middle_line (float), breakout_signal (str), channel_width (float)
MCP Tool Name: donchian_channels
"""
import logging
import math
from datetime import datetime, timezone
from typing import Any

logger = logging.getLogger("snowdrop.skills")

TOOL_META = {
    "name": "donchian_channels",
    "description": "Applies Richard Donchian's channel breakout system using highest highs and lowest lows.",
    "inputSchema": {
        "type": "object",
        "properties": {
            "highs": {"type": "array", "description": "High price series."},
            "lows": {"type": "array", "description": "Low price series."},
            "period": {"type": "integer", "description": "Lookback period (default 20)."}
        },
        "required": ["highs", "lows", "period"]
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


def donchian_channels(**kwargs: Any) -> dict:
    """Generates Donchian upper/lower bands and flags breakout direction."""
    try:
        highs = kwargs.get("highs")
        lows = kwargs.get("lows")
        period = kwargs.get("period")

        for series in (highs, lows):
            if not isinstance(series, list) or len(series) < period:
                raise ValueError("highs and lows must be lists at least 'period' long")
        if len(highs) != len(lows):
            raise ValueError("highs and lows must align")
        if not isinstance(period, int) or period <= 1:
            raise ValueError("period must be > 1")

        highs_f = []
        lows_f = []
        for h, l in zip(highs, lows):
            if not isinstance(h, (int, float)) or not isinstance(l, (int, float)):
                raise TypeError("highs and lows must be numeric")
            highs_f.append(float(h))
            lows_f.append(float(l))

        upper_channel = max(highs_f[-period:])
        lower_channel = min(lows_f[-period:])
        middle_line = (upper_channel + lower_channel) / 2
        channel_width = upper_channel - lower_channel
        last_price = (highs_f[-1] + lows_f[-1]) / 2
        if last_price > upper_channel:
            breakout_signal = "upper"
        elif last_price < lower_channel:
            breakout_signal = "lower"
        else:
            breakout_signal = "none"

        return {
            "status": "success",
            "data": {
                "upper_channel": upper_channel,
                "lower_channel": lower_channel,
                "middle_line": middle_line,
                "breakout_signal": breakout_signal,
                "channel_width": channel_width
            },
            "timestamp": datetime.now(timezone.utc).isoformat()
        }
    except (ValueError, TypeError, ZeroDivisionError) as e:
        logger.error(f"donchian_channels failed: {e}")
        _log_lesson(f"donchian_channels: {e}")
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
