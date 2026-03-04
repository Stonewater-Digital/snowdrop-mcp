"""
Execuve Summary: Calculates pivot points using multiple conventions (Standard, Fibonacci, Woodie, Camarilla, DeMark).
Inputs: high (float), low (float), close (float), open (float), method (str)
Outputs: pivot (float), support_levels (dict), resistance_levels (dict), method_used (str)
MCP Tool Name: pivot_point_calculator
"""
import logging
import math
from datetime import datetime, timezone
from typing import Any

logger = logging.getLogger("snowdrop.skills")

TOOL_META = {
    "name": "pivot_point_calculator",
    "description": "Computes pivot points and support/resistance for Standard, Fibonacci, Woodie, Camarilla, and DeMark methods.",
    "inputSchema": {
        "type": "object",
        "properties": {
            "high": {"type": "number", "description": "Prior high price."},
            "low": {"type": "number", "description": "Prior low price."},
            "close": {"type": "number", "description": "Prior close price."},
            "open": {"type": "number", "description": "Current/open price (required by Woodie, DeMark)."},
            "method": {"type": "string", "description": "standard/fibonacci/woodie/camarilla/demark."}
        },
        "required": ["high", "low", "close", "open", "method"]
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


METHODS = {"standard", "fibonacci", "woodie", "camarilla", "demark"}


def pivot_point_calculator(**kwargs: Any) -> dict:
    """Generates pivot point and S/R levels for the selected method."""
    try:
        high = kwargs.get("high")
        low = kwargs.get("low")
        close = kwargs.get("close")
        open_price = kwargs.get("open")
        method = kwargs.get("method")

        for name, value in (("high", high), ("low", low), ("close", close), ("open", open_price)):
            if not isinstance(value, (int, float)):
                raise ValueError(f"{name} must be numeric")
        if high < low:
            raise ValueError("high cannot be lower than low")
        if not isinstance(method, str) or method.lower() not in METHODS:
            raise ValueError("method must be one of standard/fibonacci/woodie/camarilla/demark")

        method = method.lower()
        resistance_levels: dict[str, float] = {}
        support_levels: dict[str, float] = {}

        if method == "standard":
            pivot = (high + low + close) / 3
            resistance_levels["R1"] = 2 * pivot - low
            resistance_levels["R2"] = pivot + (high - low)
            resistance_levels["R3"] = high + 2 * (pivot - low)
            support_levels["S1"] = 2 * pivot - high
            support_levels["S2"] = pivot - (high - low)
            support_levels["S3"] = low - 2 * (high - pivot)
        elif method == "fibonacci":
            pivot = (high + low + close) / 3
            diff = high - low
            for name, ratio in (("R1", 0.382), ("R2", 0.618), ("R3", 1.0)):
                resistance_levels[name] = pivot + ratio * diff
            for name, ratio in (("S1", 0.382), ("S2", 0.618), ("S3", 1.0)):
                support_levels[name] = pivot - ratio * diff
        elif method == "woodie":
            pivot = (high + low + 2 * open_price) / 4
            resistance_levels["R1"] = 2 * pivot - low
            resistance_levels["R2"] = pivot + (high - low)
            resistance_levels["R3"] = high + 2 * (pivot - low)
            support_levels["S1"] = 2 * pivot - high
            support_levels["S2"] = pivot - (high - low)
            support_levels["S3"] = low - 2 * (high - pivot)
        elif method == "camarilla":
            pivot = (high + low + close) / 3
            range_value = high - low
            for idx, factor in enumerate([1.1, 1.618, 2.0, 2.618], start=1):
                resistance_levels[f"R{idx}"] = close + (range_value * factor / 12)
                support_levels[f"S{idx}"] = close - (range_value * factor / 12)
        else:
            if close > open_price:
                x = 2 * high + low + close
            elif close < open_price:
                x = high + 2 * low + close
            else:
                x = high + low + 2 * close
            pivot = x / 4
            resistance_levels["R1"] = x / 2 - low
            support_levels["S1"] = x / 2 - high

        return {
            "status": "success",
            "data": {
                "pivot": pivot,
                "support_levels": support_levels,
                "resistance_levels": resistance_levels,
                "method_used": method
            },
            "timestamp": datetime.now(timezone.utc).isoformat()
        }
    except (ValueError, TypeError, ZeroDivisionError) as e:
        logger.error(f"pivot_point_calculator failed: {e}")
        _log_lesson(f"pivot_point_calculator: {e}")
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
