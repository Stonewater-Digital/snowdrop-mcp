"""
Execuve Summary: Converts OHLC candles into Heikin-Ashi representation.
Inputs: opens (list[float]), highs (list[float]), lows (list[float]), closes (list[float])
Outputs: ha_opens (list[float]), ha_highs (list[float]), ha_lows (list[float]), ha_closes (list[float]), trend_signal (list[str]), trend_strength (str)
MCP Tool Name: heikin_ashi_calculator
"""
import logging
import math
from datetime import datetime, timezone
from typing import Any

logger = logging.getLogger("snowdrop.skills")

TOOL_META = {
    "name": "heikin_ashi_calculator",
    "description": "Converts standard candles to Heikin-Ashi and reports trend direction and strength.",
    "inputSchema": {
        "type": "object",
        "properties": {
            "opens": {"type": "array", "description": "Open prices."},
            "highs": {"type": "array", "description": "High prices."},
            "lows": {"type": "array", "description": "Low prices."},
            "closes": {"type": "array", "description": "Close prices."}
        },
        "required": ["opens", "highs", "lows", "closes"]
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


def heikin_ashi_calculator(**kwargs: Any) -> dict:
    """Computes Heikin-Ashi OHLC series and interprets streaks for trend strength."""
    try:
        opens = kwargs.get("opens")
        highs = kwargs.get("highs")
        lows = kwargs.get("lows")
        closes = kwargs.get("closes")
        for series in (opens, highs, lows, closes):
            if not isinstance(series, list) or len(series) == 0:
                raise ValueError("OHLC inputs must be non-empty lists")
        if not (len(opens) == len(highs) == len(lows) == len(closes)):
            raise ValueError("OHLC series must align")

        ha_opens = []
        ha_highs = []
        ha_lows = []
        ha_closes = []
        trend_signal: list[str] = []
        prev_ha_open = (opens[0] + closes[0]) / 2
        prev_ha_close = (opens[0] + highs[0] + lows[0] + closes[0]) / 4
        ha_opens.append(prev_ha_open)
        ha_closes.append(prev_ha_close)
        ha_highs.append(max(highs[0], prev_ha_open, prev_ha_close))
        ha_lows.append(min(lows[0], prev_ha_open, prev_ha_close))
        trend_signal.append("bullish" if prev_ha_close >= prev_ha_open else "bearish")

        for idx in range(1, len(opens)):
            ha_close = (opens[idx] + highs[idx] + lows[idx] + closes[idx]) / 4
            ha_open = (prev_ha_open + prev_ha_close) / 2
            ha_high = max(highs[idx], ha_open, ha_close)
            ha_low = min(lows[idx], ha_open, ha_close)
            ha_opens.append(ha_open)
            ha_closes.append(ha_close)
            ha_highs.append(ha_high)
            ha_lows.append(ha_low)
            signal = "bullish" if ha_close >= ha_open else "bearish"
            trend_signal.append(signal)
            prev_ha_open = ha_open
            prev_ha_close = ha_close

        streak = 1
        max_streak = 1
        for idx in range(1, len(trend_signal)):
            if trend_signal[idx] == trend_signal[idx - 1]:
                streak += 1
            else:
                streak = 1
            max_streak = max(max_streak, streak)
        if max_streak >= 5:
            trend_strength = "strong"
        elif max_streak >= 3:
            trend_strength = "moderate"
        else:
            trend_strength = "weak"

        return {
            "status": "success",
            "data": {
                "ha_opens": ha_opens,
                "ha_highs": ha_highs,
                "ha_lows": ha_lows,
                "ha_closes": ha_closes,
                "trend_signal": trend_signal,
                "trend_strength": trend_strength
            },
            "timestamp": datetime.now(timezone.utc).isoformat()
        }
    except (ValueError, TypeError, ZeroDivisionError) as e:
        logger.error(f"heikin_ashi_calculator failed: {e}")
        _log_lesson(f"heikin_ashi_calculator: {e}")
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
