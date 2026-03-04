
"""
Executive Summary: Applies the monetary equation of exchange to infer velocity and pricing pressure.
Inputs: transaction_volume (float), circulating_supply (float), average_holding_period_days (float)
Outputs: velocity (float), implied_price (float), network_value_if_held_longer (float), velocity_adjusted_value (float)
MCP Tool Name: token_velocity_calculator
"""
import logging
import math
from datetime import datetime, timezone
from typing import Any

logger = logging.getLogger("snowdrop.skills")

TOOL_META = {
    "name": "token_velocity_calculator",
    "description": "Computes MV=PQ velocity metrics and highlights value unlocked through slower token circulation.",
    "inputSchema": {
        "type": "object",
        "properties": {
            "transaction_volume": {
                "type": "number",
                "description": "Total economic throughput (P*Q) in USD over the measured period."
            },
            "circulating_supply": {
                "type": "number",
                "description": "Token supply actively circulating (in tokens)."
            },
            "average_holding_period_days": {
                "type": "number",
                "description": "Average number of days tokens stay in wallets before moving again."
            }
        },
        "required": ["transaction_volume", "circulating_supply", "average_holding_period_days"]
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


def token_velocity_calculator(**kwargs: Any) -> dict:
    """Implements the monetary equation of exchange to infer velocity."""
    try:
        required = ("transaction_volume", "circulating_supply", "average_holding_period_days")
        for field in required:
            if field not in kwargs:
                raise ValueError(f"Missing required field {field}")
        transaction_volume = float(kwargs["transaction_volume"])
        circulating_supply = float(kwargs["circulating_supply"])
        holding_days = float(kwargs["average_holding_period_days"])
        if transaction_volume <= 0 or circulating_supply <= 0 or holding_days <= 0:
            raise ValueError("All inputs must be positive")
        velocity = transaction_volume / circulating_supply
        implied_price = transaction_volume / (circulating_supply * max(velocity, 1e-9))
        retention_multiplier = holding_days / 365.0
        network_value_if_held_longer = transaction_volume * retention_multiplier
        velocity_adjusted_value = transaction_volume / velocity
        return {
            "status": "success",
            "data": {
                "velocity": velocity,
                "implied_price": implied_price,
                "network_value_if_held_longer": network_value_if_held_longer,
                "velocity_adjusted_value": velocity_adjusted_value
            },
            "timestamp": datetime.now(timezone.utc).isoformat()
        }
    except (ValueError, TypeError, ZeroDivisionError) as e:
        logger.error(f"token_velocity_calculator failed: {e}")
        _log_lesson(f"token_velocity_calculator: {e}")
        return {
            "status": "error",
            "error": str(e),
            "timestamp": datetime.now(timezone.utc).isoformat()
        }


def _log_lesson(message: str) -> None:
    try:
        with open("logs/lessons.md", "a", encoding="utf-8") as file:
            file.write(f"- [{datetime.now(timezone.utc).isoformat()}] {message}\n")
    except OSError:
        pass
