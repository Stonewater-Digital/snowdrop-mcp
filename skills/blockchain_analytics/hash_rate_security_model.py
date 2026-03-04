
"""
Executive Summary: Estimates PoW security budgets and 51% attack costs using network economic inputs.
Inputs: network_hash_rate (float), block_reward (float), token_price (float), electricity_cost_kwh (float), hardware_efficiency (float)
Outputs: attack_cost_1hr (float), attack_cost_24hr (float), security_budget_daily (float), breakeven_hash_price (float)
MCP Tool Name: hash_rate_security_model
"""
import logging
import math
from datetime import datetime, timezone
from typing import Any

logger = logging.getLogger("snowdrop.skills")

TOOL_META = {
    "name": "hash_rate_security_model",
    "description": "Calculates PoW security metrics and estimated 51% attack costs drawing from Nakamoto consensus economics.",
    "inputSchema": {
        "type": "object",
        "properties": {
            "network_hash_rate": {
                "type": "number",
                "description": "Total network hash rate in hashes per second."
            },
            "block_reward": {
                "type": "number",
                "description": "Block reward including fees in native tokens."
            },
            "token_price": {
                "type": "number",
                "description": "Spot token price in USD."
            },
            "electricity_cost_kwh": {
                "type": "number",
                "description": "Electricity cost per kWh in USD for miners."
            },
            "hardware_efficiency": {
                "type": "number",
                "description": "Hardware efficiency expressed as joules per terahash."
            }
        },
        "required": ["network_hash_rate", "block_reward", "token_price", "electricity_cost_kwh", "hardware_efficiency"]
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


def hash_rate_security_model(**kwargs: Any) -> dict:
    """Computes security budgets and attack costs using standard PoW energy economics."""
    try:
        required = ("network_hash_rate", "block_reward", "token_price", "electricity_cost_kwh", "hardware_efficiency")
        for field in required:
            if field not in kwargs:
                raise ValueError(f"Missing required field {field}")
        hash_rate = float(kwargs["network_hash_rate"])
        block_reward = float(kwargs["block_reward"])
        token_price = float(kwargs["token_price"])
        electricity_cost = float(kwargs["electricity_cost_kwh"])
        hardware_eff = float(kwargs["hardware_efficiency"])
        if any(value <= 0 for value in (hash_rate, block_reward, token_price, electricity_cost, hardware_eff)):
            raise ValueError("All inputs must be positive")
        block_value = block_reward * token_price
        blocks_per_day = 144.0
        security_budget_daily = block_value * blocks_per_day
        power_consumption_kw = (hash_rate / 1e12) * hardware_eff / 1000
        hourly_energy_cost = power_consumption_kw * electricity_cost
        attack_cost_1hr = (security_budget_daily / 24) + hourly_energy_cost
        attack_cost_24hr = attack_cost_1hr * 24
        breakeven_hash_price = (security_budget_daily / hash_rate) * 1e12
        return {
            "status": "success",
            "data": {
                "attack_cost_1hr": attack_cost_1hr,
                "attack_cost_24hr": attack_cost_24hr,
                "security_budget_daily": security_budget_daily,
                "breakeven_hash_price": breakeven_hash_price
            },
            "timestamp": datetime.now(timezone.utc).isoformat()
        }
    except (ValueError, TypeError, ZeroDivisionError) as e:
        logger.error(f"hash_rate_security_model failed: {e}")
        _log_lesson(f"hash_rate_security_model: {e}")
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
