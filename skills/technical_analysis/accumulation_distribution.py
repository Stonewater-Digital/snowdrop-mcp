"""
Execuve Summary: Computes the Chaikin Accumulation/Distribution (A/D) line to track money flow.
Inputs: highs (list[float]), lows (list[float]), closes (list[float]), volumes (list[float])
Outputs: ad_line (list[float]), current_ad (float), ad_trend (str), money_flow_multiplier (float), price_ad_divergence (str)
MCP Tool Name: accumulation_distribution
"""
import logging
import math
from datetime import datetime, timezone
from typing import Any

logger = logging.getLogger("snowdrop.skills")

TOOL_META = {
    "name": "accumulation_distribution",
    "description": "Calculates accumulation/distribution via money flow multiplier and cumulative volume flow.",
    "inputSchema": {
        "type": "object",
        "properties": {
            "highs": {"type": "array", "description": "High prices."},
            "lows": {"type": "array", "description": "Low prices."},
            "closes": {"type": "array", "description": "Close prices."},
            "volumes": {"type": "array", "description": "Volume per period."}
        },
        "required": ["highs", "lows", "closes", "volumes"]
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


def accumulation_distribution(**kwargs: Any) -> dict:
    """Implements the Chaikin A/D Line to show cumulative money flow based on intraday range."""
    try:
        highs = kwargs.get("highs")
        lows = kwargs.get("lows")
        closes = kwargs.get("closes")
        volumes = kwargs.get("volumes")

        for series in (highs, lows, closes, volumes):
            if not isinstance(series, list) or len(series) < 1:
                raise ValueError("all inputs must be lists")
        if not (len(highs) == len(lows) == len(closes) == len(volumes)):
            raise ValueError("series must align")

        ad_line = []
        cumulative = 0.0
        money_flow_multiplier = 0.0
        for h, l, c, v in zip(highs, lows, closes, volumes):
            if not isinstance(h, (int, float)) or not isinstance(l, (int, float)) or not isinstance(c, (int, float)) or not isinstance(v, (int, float)):
                raise TypeError("price and volume inputs must be numeric")
            if h == l:
                multiplier = 0.0
            else:
                multiplier = (((c - l) - (h - c)) / (h - l))
            money_flow_multiplier = multiplier
            money_flow_volume = multiplier * float(v)
            cumulative += money_flow_volume
            ad_line.append(cumulative)

        current_ad = ad_line[-1]
        previous_ad = ad_line[-2] if len(ad_line) > 1 else ad_line[-1]
        if current_ad > previous_ad:
            ad_trend = "rising"
        elif current_ad < previous_ad:
            ad_trend = "falling"
        else:
            ad_trend = "flat"

        price_ad_divergence = "none"
        if len(closes) >= 2:
            price_change = closes[-1] - closes[-2]
            ad_change = current_ad - previous_ad
            if price_change > 0 and ad_change < 0:
                price_ad_divergence = "bearish"
            elif price_change < 0 and ad_change > 0:
                price_ad_divergence = "bullish"

        return {
            "status": "success",
            "data": {
                "ad_line": ad_line,
                "current_ad": current_ad,
                "ad_trend": ad_trend,
                "money_flow_multiplier": money_flow_multiplier,
                "price_ad_divergence": price_ad_divergence
            },
            "timestamp": datetime.now(timezone.utc).isoformat()
        }
    except (ValueError, TypeError, ZeroDivisionError) as e:
        logger.error(f"accumulation_distribution failed: {e}")
        _log_lesson(f"accumulation_distribution: {e}")
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
