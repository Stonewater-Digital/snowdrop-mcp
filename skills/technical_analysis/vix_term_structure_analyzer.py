"""
Execuve Summary: Evaluates the VIX futures term structure for contango/backwardation dynamics.
Inputs: vix_prices (list[dict])
Outputs: term_structure_shape (str), steepness (float), roll_yield_estimate (float), mean_reversion_signal (str)
MCP Tool Name: vix_term_structure_analyzer
"""
import logging
import math
from datetime import datetime, timezone
from typing import Any

logger = logging.getLogger("snowdrop.skills")

TOOL_META = {
    "name": "vix_term_structure_analyzer",
    "description": "Analyzes VIX futures prices by expiry to identify contango/backwardation and roll yield.",
    "inputSchema": {
        "type": "object",
        "properties": {
            "vix_prices": {
                "type": "array",
                "description": "List of objects with expiry_days and price for VIX futures."
            }
        },
        "required": ["vix_prices"]
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


def vix_term_structure_analyzer(**kwargs: Any) -> dict:
    """Sorts VIX futures by days to expiry and compares the slope vs front contract to gauge regime."""
    try:
        vix_prices = kwargs.get("vix_prices")
        if not isinstance(vix_prices, list) or len(vix_prices) < 2:
            raise ValueError("vix_prices must be a list with at least two entries")

        structured = []
        for entry in vix_prices:
            if not isinstance(entry, dict):
                raise TypeError("each vix_prices entry must be a dict")
            expiry = entry.get("expiry_days")
            price = entry.get("price")
            if not isinstance(expiry, (int, float)) or not isinstance(price, (int, float)):
                raise ValueError("expiry_days and price must be numeric")
            structured.append((float(expiry), float(price)))
        structured.sort(key=lambda item: item[0])

        expiries = [item[0] for item in structured]
        prices = [item[1] for item in structured]
        front_price = prices[0]
        back_price = prices[-1]
        if back_price > front_price:
            shape = "contango"
        elif back_price < front_price:
            shape = "backwardation"
        else:
            shape = "flat"

        # Linear regression slope (price per day to expiry)
        mean_x = sum(expiries) / len(expiries)
        mean_y = sum(prices) / len(prices)
        cov = sum((x - mean_x) * (y - mean_y) for x, y in zip(expiries, prices))
        var_x = sum((x - mean_x) ** 2 for x in expiries)
        slope = cov / var_x if var_x != 0 else 0.0

        roll_yield = 0.0
        if len(prices) >= 2 and prices[0] != 0:
            roll_yield = (prices[0] - prices[1]) / prices[0]

        mean_reversion_signal = "neutral"
        if shape == "contango" and slope > 0:
            mean_reversion_signal = "vol_crush"
        elif shape == "backwardation" and slope < 0:
            mean_reversion_signal = "panic_regime"
        elif abs(slope) < 0.01:
            mean_reversion_signal = "balanced"

        return {
            "status": "success",
            "data": {
                "term_structure_shape": shape,
                "steepness": slope,
                "roll_yield_estimate": roll_yield,
                "mean_reversion_signal": mean_reversion_signal,
                "ordered_curve": structured
            },
            "timestamp": datetime.now(timezone.utc).isoformat()
        }
    except (ValueError, TypeError, ZeroDivisionError) as e:
        logger.error(f"vix_term_structure_analyzer failed: {e}")
        _log_lesson(f"vix_term_structure_analyzer: {e}")
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
