"""
Execuve Summary: Estimates the earnings-implied move from an ATM straddle.
Inputs: atm_straddle_price (float), stock_price (float), days_to_expiry (int)
Outputs: implied_move_pct (float), implied_move_dollars (float), expected_range (dict), annualized_implied_vol (float)
MCP Tool Name: options_implied_move
"""
import logging
import math
from datetime import datetime, timezone
from typing import Any

logger = logging.getLogger("snowdrop.skills")

TOOL_META = {
    "name": "options_implied_move",
    "description": "Converts ATM straddle pricing into implied move, range, and annualized IV approximation.",
    "inputSchema": {
        "type": "object",
        "properties": {
            "atm_straddle_price": {"type": "number", "description": "Cost of ATM straddle (call+put)."},
            "stock_price": {"type": "number", "description": "Underlying price."},
            "days_to_expiry": {"type": "integer", "description": "Days until the option expires."}
        },
        "required": ["atm_straddle_price", "stock_price", "days_to_expiry"]
    },
    "outputSchema": {
        "type": "object", "properties": {"status": {"type": "string"}, "timestamp": {"type": "string"}, "data": {"type": "object"}}, "required": ["status", "timestamp"]
    }
}


def options_implied_move(**kwargs: Any) -> dict:
    """Computes implied move using ATM straddle cost."""
    try:
        straddle = kwargs.get("atm_straddle_price")
        price = kwargs.get("stock_price")
        days = kwargs.get("days_to_expiry")
        if not isinstance(straddle, (int, float)) or not isinstance(price, (int, float)):
            raise ValueError("atm_straddle_price and stock_price must be numeric")
        if not isinstance(days, int) or days <= 0:
            raise ValueError("days_to_expiry must be positive integer")
        if price <= 0:
            raise ValueError("stock_price must be positive")

        implied_move_pct = straddle / price
        implied_move_dollars = straddle
        expected_range = {
            "lower": price - straddle,
            "upper": price + straddle
        }
        annualized_iv = implied_move_pct * math.sqrt(365 / days)

        return {
            "status": "success",
            "data": {
                "implied_move_pct": implied_move_pct,
                "implied_move_dollars": implied_move_dollars,
                "expected_range": expected_range,
                "annualized_implied_vol": annualized_iv
            },
            "timestamp": datetime.now(timezone.utc).isoformat()
        }
    except (ValueError, TypeError, ZeroDivisionError) as e:
        logger.error(f"options_implied_move failed: {e}")
        _log_lesson(f"options_implied_move: {e}")
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
