"""
Execuve Summary: Calculates Volume-Weighted Average Price (VWAP) with standard deviation bands.
Inputs: highs (list[float]), lows (list[float]), closes (list[float]), volumes (list[float])
Outputs: vwap (float), upper_band_1std (float), lower_band_1std (float), upper_band_2std (float), lower_band_2std (float), price_vs_vwap (str)
MCP Tool Name: vwap_calculator
"""
import logging
import math
from datetime import datetime, timezone
from typing import Any

logger = logging.getLogger("snowdrop.skills")

TOOL_META = {
    "name": "vwap_calculator",
    "description": "Computes VWAP from typical price (H+L+C)/3 and derives 1/2 standard deviation bands.",
    "inputSchema": {
        "type": "object",
        "properties": {
            "highs": {"type": "array", "description": "High prices."},
            "lows": {"type": "array", "description": "Low prices."},
            "closes": {"type": "array", "description": "Close prices."},
            "volumes": {"type": "array", "description": "Volume per bar."}
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


def vwap_calculator(**kwargs: Any) -> dict:
    """Derives VWAP by weighting typical price with traded volume and builds statistical bands."""
    try:
        highs = kwargs.get("highs")
        lows = kwargs.get("lows")
        closes = kwargs.get("closes")
        volumes = kwargs.get("volumes")

        for series in (highs, lows, closes, volumes):
            if not isinstance(series, list) or len(series) == 0:
                raise ValueError("all series must be non-empty lists")
        if not (len(highs) == len(lows) == len(closes) == len(volumes)):
            raise ValueError("all series must align in length")

        typical_prices = []
        volume_list = []
        for h, l, c, v in zip(highs, lows, closes, volumes):
            if not isinstance(h, (int, float)) or not isinstance(l, (int, float)) or not isinstance(c, (int, float)) or not isinstance(v, (int, float)):
                raise TypeError("price and volume inputs must be numeric")
            if v < 0:
                raise ValueError("volumes cannot be negative")
            typical_prices.append((float(h) + float(l) + float(c)) / 3)
            volume_list.append(float(v))

        total_volume = sum(volume_list)
        if total_volume == 0:
            raise ZeroDivisionError("total volume cannot be zero")
        weighted_sum = sum(price * volume for price, volume in zip(typical_prices, volume_list))
        vwap_value = weighted_sum / total_volume
        variance = sum(volume * (price - vwap_value) ** 2 for price, volume in zip(typical_prices, volume_list)) / total_volume
        std_dev = math.sqrt(variance)
        upper_band_1 = vwap_value + std_dev
        lower_band_1 = vwap_value - std_dev
        upper_band_2 = vwap_value + 2 * std_dev
        lower_band_2 = vwap_value - 2 * std_dev

        last_price = float(closes[-1])
        if last_price > vwap_value:
            relation = "above"
        elif last_price < vwap_value:
            relation = "below"
        else:
            relation = "at"

        return {
            "status": "success",
            "data": {
                "vwap": vwap_value,
                "upper_band_1std": upper_band_1,
                "lower_band_1std": lower_band_1,
                "upper_band_2std": upper_band_2,
                "lower_band_2std": lower_band_2,
                "price_vs_vwap": relation
            },
            "timestamp": datetime.now(timezone.utc).isoformat()
        }
    except (ValueError, TypeError, ZeroDivisionError) as e:
        logger.error(f"vwap_calculator failed: {e}")
        _log_lesson(f"vwap_calculator: {e}")
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
