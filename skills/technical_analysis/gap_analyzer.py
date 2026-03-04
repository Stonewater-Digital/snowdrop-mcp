"""
Execuve Summary: Detects price gaps, classifies their type, and checks if they were filled.
Inputs: opens (list[float]), highs (list[float]), lows (list[float]), closes (list[float])
Outputs: gaps (list of dicts), unfilled_gaps (list)
MCP Tool Name: gap_analyzer
"""
import logging
import math
from datetime import datetime, timezone
from typing import Any

logger = logging.getLogger("snowdrop.skills")

TOOL_META = {
    "name": "gap_analyzer",
    "description": "Scans OHLC data for breakaway, runaway, exhaustion, and common gaps, tracking fill status.",
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


def gap_analyzer(**kwargs: Any) -> dict:
    """Analyzes daily gaps and labels them as common, breakaway, runaway, or exhaustion."""
    try:
        opens = kwargs.get("opens")
        highs = kwargs.get("highs")
        lows = kwargs.get("lows")
        closes = kwargs.get("closes")

        for series in (opens, highs, lows, closes):
            if not isinstance(series, list) or len(series) < 2:
                raise ValueError("all OHLC series must be lists with at least two entries")
        length = len(opens)
        if not (length == len(highs) == len(lows) == len(closes)):
            raise ValueError("OHLC series must have equal length")

        avg_range = sum(float(h) - float(l) for h, l in zip(highs, lows)) / length
        threshold = max(avg_range * 0.1, 0.01)
        gaps = []
        unfilled = []
        for idx in range(1, length):
            prev_close = float(closes[idx - 1])
            current_open = float(opens[idx])
            gap_size = current_open - prev_close
            if abs(gap_size) < threshold:
                continue
            gap_direction = "up" if gap_size > 0 else "down"
            size_pct = (gap_size / prev_close) * 100 if prev_close != 0 else math.inf
            gap_type = "common"
            if gap_direction == "up" and float(closes[idx]) > float(highs[idx - 1]):
                gap_type = "breakaway"
            elif gap_direction == "down" and float(closes[idx]) < float(lows[idx - 1]):
                gap_type = "breakaway"
            else:
                if idx + 1 < length:
                    next_close = float(closes[idx + 1])
                    if gap_direction == "up" and next_close > float(closes[idx]):
                        gap_type = "runaway"
                    elif gap_direction == "down" and next_close < float(closes[idx]):
                        gap_type = "runaway"
                    elif gap_direction == "up" and next_close < float(closes[idx]):
                        gap_type = "exhaustion"
                    elif gap_direction == "down" and next_close > float(closes[idx]):
                        gap_type = "exhaustion"

            filled = _gap_filled(idx, prev_close, float(highs[idx]), float(lows[idx]), highs, lows)
            gap_info = {
                "index": idx,
                "type": gap_type,
                "direction": gap_direction,
                "size": gap_size,
                "size_pct": size_pct,
                "filled": filled
            }
            gaps.append(gap_info)
            if not filled:
                unfilled.append(gap_info)

        return {
            "status": "success",
            "data": {
                "gaps": gaps,
                "unfilled_gaps": unfilled
            },
            "timestamp": datetime.now(timezone.utc).isoformat()
        }
    except (ValueError, TypeError, ZeroDivisionError) as e:
        logger.error(f"gap_analyzer failed: {e}")
        _log_lesson(f"gap_analyzer: {e}")
        return {
            "status": "error",
            "error": str(e),
            "timestamp": datetime.now(timezone.utc).isoformat()
        }


def _gap_filled(index: int, reference_price: float, high: float, low: float, highs: list[Any], lows: list[Any]) -> bool:
    if low <= reference_price <= high:
        return True
    for future in range(index + 1, len(highs)):
        if float(lows[future]) <= reference_price <= float(highs[future]):
            return True
    return False


def _log_lesson(message: str) -> None:
    try:
        with open("logs/lessons.md", "a") as f:
            f.write(f"- [{datetime.now(timezone.utc).isoformat()}] {message}\n")
    except OSError:
        pass
