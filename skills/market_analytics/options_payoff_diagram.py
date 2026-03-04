"""
Execuve Summary: Builds a payoff diagram for multi-leg options strategies.
Inputs: legs (list[dict]), price_range (list[float])
Outputs: payoff_at_each_price (dict), max_profit (float), max_loss (float), breakeven_points (list[float]), strategy_name_detected (str)
MCP Tool Name: options_payoff_diagram
"""
import logging
import math
from datetime import datetime, timezone
from typing import Any

logger = logging.getLogger("snowdrop.skills")

TOOL_META = {
    "name": "options_payoff_diagram",
    "description": "Calculates strategy payoff across a price grid and identifies basic spread types.",
    "inputSchema": {
        "type": "object",
        "properties": {
            "legs": {"type": "array", "description": "List of option legs with type (call/put), strike, premium, quantity, direction (long/short)."},
            "price_range": {"type": "array", "description": "List of underlying prices to evaluate."}
        },
        "required": ["legs", "price_range"]
    },
    "outputSchema": {
        "type": "object", "properties": {"status": {"type": "string"}, "timestamp": {"type": "string"}, "data": {"type": "object"}}, "required": ["status", "timestamp"]
    }
}


def options_payoff_diagram(**kwargs: Any) -> dict:
    """Aggregates payoffs for each scenario in price_range."""
    try:
        legs = kwargs.get("legs")
        price_range = kwargs.get("price_range")
        if not isinstance(legs, list) or not isinstance(price_range, list):
            raise ValueError("legs and price_range must be lists")
        payoff = {}
        for price in price_range:
            total = 0.0
            for leg in legs:
                option_type = leg.get("type", "call").lower()
                strike = float(leg.get("strike"))
                premium = float(leg.get("premium", 0))
                quantity = int(leg.get("quantity", 1))
                direction = leg.get("direction", "long").lower()
                intrinsic = max(price - strike, 0) if option_type == "call" else max(strike - price, 0)
                leg_payoff = intrinsic - premium
                if direction == "short":
                    leg_payoff = -leg_payoff
                total += leg_payoff * quantity
            payoff[price] = total

        max_profit = max(payoff.values())
        max_loss = min(payoff.values())
        breakevens = [price for price, value in payoff.items() if abs(value) < 1e-6]
        strategy_name = _detect_strategy(legs)

        return {
            "status": "success",
            "data": {
                "payoff_at_each_price": payoff,
                "max_profit": max_profit,
                "max_loss": max_loss,
                "breakeven_points": breakevens,
                "strategy_name_detected": strategy_name
            },
            "timestamp": datetime.now(timezone.utc).isoformat()
        }
    except (ValueError, TypeError, ZeroDivisionError) as e:
        logger.error(f"options_payoff_diagram failed: {e}")
        _log_lesson(f"options_payoff_diagram: {e}")
        return {
            "status": "error",
            "error": str(e),
            "timestamp": datetime.now(timezone.utc).isoformat()
        }


def _detect_strategy(legs: list[dict]) -> str:
    if len(legs) == 2:
        types = {leg.get("type", "call").lower() for leg in legs}
        strikes = sorted(float(leg.get("strike")) for leg in legs)
        directions = [leg.get("direction", "long").lower() for leg in legs]
        if len(types) == 1 and directions.count("long") == directions.count("short") == 1:
            return "vertical_spread"
        if len(types) == 2 and all(direction == "long" for direction in directions):
            return "straddle"
    if len(legs) == 1:
        return f"single_{legs[0].get('type', 'call').lower()}"
    return "multi_leg"


def _log_lesson(message: str) -> None:
    try:
        with open("logs/lessons.md", "a") as f:
            f.write(f"- [{datetime.now(timezone.utc).isoformat()}] {message}\n")
    except OSError:
        pass
