"""
Execuve Summary: Calculates Fibonacci extension targets beyond the prior swing.
Inputs: swing_low (float), swing_high (float), retracement_low (float)
Outputs: extension_levels (dict), price_targets (dict)
MCP Tool Name: fibonacci_extension
"""
import logging
import math
from datetime import datetime, timezone
from typing import Any

logger = logging.getLogger("snowdrop.skills")

TOOL_META = {
    "name": "fibonacci_extension",
    "description": "Computes Fibonacci extension projections (100%–261.8%) for trend continuation targets.",
    "inputSchema": {
        "type": "object",
        "properties": {
            "swing_low": {"type": "number", "description": "Low preceding the impulse move."},
            "swing_high": {"type": "number", "description": "High of the impulse move."},
            "retracement_low": {"type": "number", "description": "Low after retracement used as starting point for projections."}
        },
        "required": ["swing_low", "swing_high", "retracement_low"]
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

EXT_LEVELS = [100.0, 127.2, 161.8, 200.0, 261.8]


def fibonacci_extension(**kwargs: Any) -> dict:
    """Projects Fibonacci extension targets from the retracement low based on prior swing magnitude."""
    try:
        swing_low = kwargs.get("swing_low")
        swing_high = kwargs.get("swing_high")
        retracement_low = kwargs.get("retracement_low")

        for name, value in (("swing_low", swing_low), ("swing_high", swing_high), ("retracement_low", retracement_low)):
            if not isinstance(value, (int, float)):
                raise ValueError(f"{name} must be numeric")
        if swing_high <= swing_low:
            raise ValueError("swing_high must exceed swing_low")
        if retracement_low > swing_high or retracement_low < swing_low:
            raise ValueError("retracement_low should fall between swing low and high")

        swing_range = swing_high - swing_low
        price_targets = {}
        for level in EXT_LEVELS:
            multiplier = level / 100
            target_price = retracement_low + swing_range * multiplier
            price_targets[f"{level}"] = target_price

        return {
            "status": "success",
            "data": {
                "extension_levels": EXT_LEVELS,
                "price_targets": price_targets
            },
            "timestamp": datetime.now(timezone.utc).isoformat()
        }
    except (ValueError, TypeError, ZeroDivisionError) as e:
        logger.error(f"fibonacci_extension failed: {e}")
        _log_lesson(f"fibonacci_extension: {e}")
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
