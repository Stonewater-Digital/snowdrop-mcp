"""
Execuve Summary: Detects common candlestick reversal and continuation patterns.
Inputs: opens (list[float]), highs (list[float]), lows (list[float]), closes (list[float])
Outputs: patterns_detected (list of dicts)
MCP Tool Name: candlestick_pattern_detector
"""
import logging
import math
from datetime import datetime, timezone
from typing import Any

logger = logging.getLogger("snowdrop.skills")

TOOL_META = {
    "name": "candlestick_pattern_detector",
    "description": "Scans OHLC data for common patterns: doji, hammer, engulfing, stars, soldiers/crows, harami, spinning top, shooting star.",
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


def candlestick_pattern_detector(**kwargs: Any) -> dict:
    """Evaluates common candlestick formations and returns pattern metadata."""
    try:
        opens = kwargs.get("opens")
        highs = kwargs.get("highs")
        lows = kwargs.get("lows")
        closes = kwargs.get("closes")

        for series in (opens, highs, lows, closes):
            if not isinstance(series, list) or len(series) < 3:
                raise ValueError("all series must be lists with at least three entries")
        if not (len(opens) == len(highs) == len(lows) == len(closes)):
            raise ValueError("OHLC series must align")

        patterns: list[dict[str, Any]] = []

        def _body(o: float, c: float) -> float:
            return abs(c - o)

        def _range(h: float, l: float) -> float:
            return h - l

        for idx in range(len(opens)):
            o, h, l, c = float(opens[idx]), float(highs[idx]), float(lows[idx]), float(closes[idx])
            body = _body(o, c)
            total_range = _range(h, l) or 1e-9
            upper_shadow = h - max(o, c)
            lower_shadow = min(o, c) - l

            # Doji
            if body <= 0.1 * total_range:
                patterns.append({"index": idx, "pattern_name": "doji", "type": "neutral", "reliability": "medium"})
            # Spinning top
            if body <= 0.3 * total_range and upper_shadow >= 0.3 * total_range and lower_shadow >= 0.3 * total_range:
                patterns.append({"index": idx, "pattern_name": "spinning_top", "type": "neutral", "reliability": "medium"})
            # Hammer
            if body <= 0.3 * total_range and lower_shadow >= 2 * body and upper_shadow <= 0.2 * total_range and c > o:
                patterns.append({"index": idx, "pattern_name": "hammer", "type": "bullish", "reliability": "high"})
            # Shooting star
            if body <= 0.3 * total_range and upper_shadow >= 2 * body and lower_shadow <= 0.2 * total_range and c < o:
                patterns.append({"index": idx, "pattern_name": "shooting_star", "type": "bearish", "reliability": "high"})

            # Engulfing (requires prior candle)
            if idx >= 1:
                prev_o, prev_c = float(opens[idx - 1]), float(closes[idx - 1])
                prev_body = _body(prev_o, prev_c)
                if prev_body > 0:
                    # Bullish engulfing
                    if prev_c < prev_o and c > o and c >= prev_o and o <= prev_c:
                        patterns.append({"index": idx, "pattern_name": "bullish_engulfing", "type": "bullish", "reliability": "high"})
                    # Bearish engulfing
                    if prev_c > prev_o and c < o and o >= prev_c and c <= prev_o:
                        patterns.append({"index": idx, "pattern_name": "bearish_engulfing", "type": "bearish", "reliability": "high"})
                # Harami
                if prev_body > 0 and body < prev_body and max(o, c) <= max(prev_o, prev_c) and min(o, c) >= min(prev_o, prev_c):
                    pattern_type = "bullish" if c > o else "bearish"
                    patterns.append({"index": idx, "pattern_name": "harami", "type": pattern_type, "reliability": "medium"})

            # Morning/Evening star requires 3 candles
            if idx >= 2:
                o1, c1 = float(opens[idx - 2]), float(closes[idx - 2])
                o2, c2 = float(opens[idx - 1]), float(closes[idx - 1])
                o3, c3 = o, c
                body1 = _body(o1, c1)
                body2 = _body(o2, c2)
                body3 = _body(o3, c3)
                # Morning star
                if c1 < o1 and body1 > body2 and c3 > o3 and c3 > ((o1 + c1) / 2):
                    if min(o2, c2) < min(o1, c1) and max(o2, c2) < min(o1, c1):
                        patterns.append({"index": idx, "pattern_name": "morning_star", "type": "bullish", "reliability": "high"})
                # Evening star
                if c1 > o1 and body1 > body2 and c3 < o3 and c3 < ((o1 + c1) / 2):
                    if max(o2, c2) > max(o1, c1) and min(o2, c2) > max(o1, c1):
                        patterns.append({"index": idx, "pattern_name": "evening_star", "type": "bearish", "reliability": "high"})

            # Three white soldiers / black crows
            if idx >= 2:
                recent = list(zip(opens[idx - 2: idx + 1], closes[idx - 2: idx + 1]))
                if all(cand[1] > cand[0] for cand in recent):
                    if (recent[1][0] > recent[0][0]) and (recent[2][0] > recent[1][0]):
                        patterns.append({"index": idx, "pattern_name": "three_white_soldiers", "type": "bullish", "reliability": "high"})
                if all(cand[1] < cand[0] for cand in recent):
                    if (recent[1][0] < recent[0][0]) and (recent[2][0] < recent[1][0]):
                        patterns.append({"index": idx, "pattern_name": "three_black_crows", "type": "bearish", "reliability": "high"})

        return {
            "status": "success",
            "data": {
                "patterns_detected": patterns
            },
            "timestamp": datetime.now(timezone.utc).isoformat()
        }
    except (ValueError, TypeError, ZeroDivisionError) as e:
        logger.error(f"candlestick_pattern_detector failed: {e}")
        _log_lesson(f"candlestick_pattern_detector: {e}")
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
