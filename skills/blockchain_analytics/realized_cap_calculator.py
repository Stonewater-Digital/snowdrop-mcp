
"""
Executive Summary: Derives realized capitalization by summing UTXO cost bases and gauges unrealized gains.
Inputs: utxo_set (list[dict])
Outputs: realized_cap (float), market_cap_estimate (float), vs_market_cap (float), unrealized_profit_loss (float), pct_supply_in_profit (float)
MCP Tool Name: realized_cap_calculator
"""
import logging
import math
from datetime import datetime, timezone
from typing import Any, Sequence

logger = logging.getLogger("snowdrop.skills")

TOOL_META = {
    "name": "realized_cap_calculator",
    "description": "Computes realized capitalization from UTXO-style inputs and infers unrealized profit and supply composition.",
    "inputSchema": {
        "type": "object",
        "properties": {
            "utxo_set": {
                "type": "array",
                "description": "List of unspent outputs each containing amount and price_at_creation fields.",
                "items": {
                    "type": "object",
                    "properties": {
                        "amount": {"type": "number", "description": "Coin amount for the UTXO."},
                        "price_at_creation": {"type": "number", "description": "Price when the output was created in USD."}
                    },
                    "required": ["amount", "price_at_creation"]
                }
            }
        },
        "required": ["utxo_set"]
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


def realized_cap_calculator(**kwargs: Any) -> dict:
    """Aggregates realized cap using UTXO methodology (Glassnode / Coin Metrics standard)."""
    try:
        if "utxo_set" not in kwargs:
            raise ValueError("utxo_set is required")
        utxo_set: Sequence[dict] = kwargs["utxo_set"]
        if not isinstance(utxo_set, Sequence) or not utxo_set:
            raise ValueError("utxo_set must be a non-empty list")
        realized_cap = 0.0
        total_supply = 0.0
        highest_creation_price = 0.0
        supply_in_profit = 0.0
        for utxo in utxo_set:
            amount = float(utxo.get("amount", 0))
            creation_price = float(utxo.get("price_at_creation", 0))
            if amount < 0 or creation_price < 0:
                raise ValueError("UTXO amount and price must be non-negative")
            realized_cap += amount * creation_price
            total_supply += amount
            highest_creation_price = max(highest_creation_price, creation_price)
        if total_supply == 0:
            raise ZeroDivisionError("Total supply derived from UTXOs is zero")
        current_price_estimate = highest_creation_price or 0.0
        market_cap_estimate = total_supply * current_price_estimate
        for utxo in utxo_set:
            amount = float(utxo.get("amount", 0))
            creation_price = float(utxo.get("price_at_creation", 0))
            if creation_price < current_price_estimate:
                supply_in_profit += amount
        vs_market_cap = market_cap_estimate / realized_cap if realized_cap else math.inf
        unrealized_profit_loss = market_cap_estimate - realized_cap
        pct_supply_in_profit = (supply_in_profit / total_supply) * 100
        return {
            "status": "success",
            "data": {
                "realized_cap": realized_cap,
                "market_cap_estimate": market_cap_estimate,
                "vs_market_cap": vs_market_cap,
                "unrealized_profit_loss": unrealized_profit_loss,
                "pct_supply_in_profit": pct_supply_in_profit
            },
            "timestamp": datetime.now(timezone.utc).isoformat()
        }
    except (ValueError, TypeError, ZeroDivisionError) as e:
        logger.error(f"realized_cap_calculator failed: {e}")
        _log_lesson(f"realized_cap_calculator: {e}")
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
