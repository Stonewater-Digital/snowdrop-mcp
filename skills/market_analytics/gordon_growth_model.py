"""
Execuve Summary: Values a dividend stream using the Gordon Growth Model.
Inputs: current_dividend (float), growth_rate (float), required_return (float), current_price (float|None)
Outputs: intrinsic_value (float), dividend_yield (float|None), implied_growth_at_current_price (float|None), sensitivity_table (dict)
MCP Tool Name: gordon_growth_model
"""
import logging
import math
from datetime import datetime, timezone
from typing import Any

logger = logging.getLogger("snowdrop.skills")

TOOL_META = {
    "name": "gordon_growth_model",
    "description": "Computes intrinsic value using Gordon Growth, plus yield and growth sensitivity.",
    "inputSchema": {
        "type": "object",
        "properties": {
            "current_dividend": {"type": "number", "description": "Most recent annual dividend per share."},
            "growth_rate": {"type": "number", "description": "Expected perpetual growth (decimal)."},
            "required_return": {"type": "number", "description": "Investor required return (decimal)."},
            "current_price": {"type": "number", "description": "Optional current market price."}
        },
        "required": ["current_dividend", "growth_rate", "required_return"]
    },
    "outputSchema": {
        "type": "object", "properties": {"status": {"type": "string"}, "timestamp": {"type": "string"}, "data": {"type": "object"}}, "required": ["status", "timestamp"]
    }
}


def gordon_growth_model(**kwargs: Any) -> dict:
    """Calculates Gordon Growth intrinsic value and optional implied growth from current price."""
    try:
        dividend = kwargs.get("current_dividend")
        growth = kwargs.get("growth_rate")
        required = kwargs.get("required_return")
        current_price = kwargs.get("current_price")
        for label, value in (("current_dividend", dividend), ("growth_rate", growth), ("required_return", required)):
            if not isinstance(value, (int, float)):
                raise ValueError(f"{label} must be numeric")
        if growth >= required:
            raise ValueError("growth_rate must be less than required_return for convergence")

        dividend_next = dividend * (1 + growth)
        intrinsic_value = dividend_next / (required - growth)
        dividend_yield = (dividend / current_price) if isinstance(current_price, (int, float)) and current_price else None
        implied_growth = None
        if isinstance(current_price, (int, float)) and current_price > 0:
            implied_growth = _solve_implied_growth(dividend, required, current_price)

        sensitivity_table = {}
        for delta in (-0.01, 0, 0.01):
            g = growth + delta
            if g >= required:
                sensitivity_table[f"growth_{round((g)*100,2)}"] = math.inf
            else:
                sensitivity_table[f"growth_{round((g)*100,2)}"] = dividend * (1 + g) / (required - g)

        return {
            "status": "success",
            "data": {
                "intrinsic_value": intrinsic_value,
                "dividend_yield": dividend_yield,
                "implied_growth_at_current_price": implied_growth,
                "sensitivity_table": sensitivity_table
            },
            "timestamp": datetime.now(timezone.utc).isoformat()
        }
    except (ValueError, TypeError, ZeroDivisionError) as e:
        logger.error(f"gordon_growth_model failed: {e}")
        _log_lesson(f"gordon_growth_model: {e}")
        return {
            "status": "error",
            "error": str(e),
            "timestamp": datetime.now(timezone.utc).isoformat()
        }


def _solve_implied_growth(dividend: float, required: float, price: float) -> float | None:
    g_low, g_high = -0.5, required - 1e-6
    for _ in range(50):
        g_mid = (g_low + g_high) / 2
        if g_mid >= required:
            g_high = required - 1e-6
            continue
        value = dividend * (1 + g_mid) / (required - g_mid)
        if abs(value - price) < 1e-6:
            return g_mid
        if value > price:
            g_high = g_mid
        else:
            g_low = g_mid
    return None


def _log_lesson(message: str) -> None:
    try:
        with open("logs/lessons.md", "a") as f:
            f.write(f"- [{datetime.now(timezone.utc).isoformat()}] {message}\n")
    except OSError:
        pass
