"""
Execuve Summary: Computes the Advance-Decline line to gauge market breadth.
Inputs: advances (list[int]), declines (list[int])
Outputs: ad_line (list[float]), ad_ratio (float), mcclellan_oscillator (float|None), market_breadth_signal (str)
MCP Tool Name: advance_decline_line
"""
import logging
import math
from datetime import datetime, timezone
from typing import Any

logger = logging.getLogger("snowdrop.skills")

TOOL_META = {
    "name": "advance_decline_line",
    "description": "Builds the cumulative Advance-Decline line and optional McClellan oscillator signal.",
    "inputSchema": {
        "type": "object",
        "properties": {
            "advances": {"type": "array", "description": "Number of advancing issues per day."},
            "declines": {"type": "array", "description": "Number of declining issues per day."}
        },
        "required": ["advances", "declines"]
    },
    "outputSchema": {
        "type": "object", "properties": {"status": {"type": "string"}, "timestamp": {"type": "string"}, "data": {"type": "object"}}, "required": ["status", "timestamp"]
    }
}


def advance_decline_line(**kwargs: Any) -> dict:
    """Computes AD line, ratio, and simplified McClellan oscillator."""
    try:
        advances = kwargs.get("advances")
        declines = kwargs.get("declines")
        if not isinstance(advances, list) or not isinstance(declines, list):
            raise ValueError("advances and declines must be lists")
        if len(advances) != len(declines) or len(advances) == 0:
            raise ValueError("series must align and be non-empty")

        ad_line = []
        cumulative = 0
        net_issues = []
        for adv, dec in zip(advances, declines):
            if not isinstance(adv, (int, float)) or not isinstance(dec, (int, float)):
                raise TypeError("advances/declines must be numeric")
            net = adv - dec
            net_issues.append(net)
            cumulative += net
            ad_line.append(cumulative)
        ad_ratio = sum(advances) / max(1, sum(declines))

        mcclellan = None
        if len(net_issues) >= 39:
            ema19 = _ema(net_issues, 19)
            ema39 = _ema(net_issues, 39)
            mcclellan = ema19[-1] - ema39[-1]
        signal = "bullish" if ad_ratio > 1 else ("bearish" if ad_ratio < 1 else "neutral")

        return {
            "status": "success",
            "data": {
                "ad_line": ad_line,
                "ad_ratio": ad_ratio,
                "mcclellan_oscillator": mcclellan,
                "market_breadth_signal": signal
            },
            "timestamp": datetime.now(timezone.utc).isoformat()
        }
    except (ValueError, TypeError, ZeroDivisionError) as e:
        logger.error(f"advance_decline_line failed: {e}")
        _log_lesson(f"advance_decline_line: {e}")
        return {
            "status": "error",
            "error": str(e),
            "timestamp": datetime.now(timezone.utc).isoformat()
        }


def _ema(values: list[float], period: int) -> list[float]:
    ema = [math.nan] * len(values)
    if len(values) < period:
        return ema
    alpha = 2 / (period + 1)
    seed = sum(values[:period]) / period
    ema[period - 1] = seed
    prev = seed
    for idx in range(period, len(values)):
        prev = alpha * values[idx] + (1 - alpha) * prev
        ema[idx] = prev
    return ema


def _log_lesson(message: str) -> None:
    try:
        with open("logs/lessons.md", "a") as f:
            f.write(f"- [{datetime.now(timezone.utc).isoformat()}] {message}\n")
    except OSError:
        pass
