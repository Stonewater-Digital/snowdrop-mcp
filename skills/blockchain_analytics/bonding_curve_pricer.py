
"""
Executive Summary: Prices bonding-curve tokens across curve shapes and trade directions.
Inputs: curve_type (str), supply (float), reserve_balance (float), reserve_ratio (float), trade_amount (float)
Outputs: current_price (float), price_after_buy (float), price_after_sell (float), slippage (float), curve_visualization_points (list[dict])
MCP Tool Name: bonding_curve_pricer
"""
import logging
import math
from datetime import datetime, timezone
from typing import Any

logger = logging.getLogger("snowdrop.skills")

TOOL_META = {
    "name": "bonding_curve_pricer",
    "description": "Evaluates different bonding curve formulations (linear, exponential, Bancor) for price projection.",
    "inputSchema": {
        "type": "object",
        "properties": {
            "curve_type": {"type": "string", "description": "linear/polynomial/sigmoid/exponential"},
            "supply": {"type": "number", "description": "Current token supply"},
            "reserve_balance": {"type": "number", "description": "Reserve collateral balance"},
            "reserve_ratio": {"type": "number", "description": "Bancor-style reserve ratio (0-1)"},
            "trade_amount": {"type": "number", "description": "Tokens to buy or sell for evaluating slippage"}
        },
        "required": ["curve_type", "supply", "reserve_balance", "reserve_ratio", "trade_amount"]
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


def bonding_curve_pricer(**kwargs: Any) -> dict:
    """Implements generic bonding-curve equations (see Bancor protocol docs)."""
    try:
        curve = kwargs.get("curve_type", "linear").lower()
        supply = float(kwargs.get("supply", 0))
        reserve_balance = float(kwargs.get("reserve_balance", 0))
        reserve_ratio = float(kwargs.get("reserve_ratio", 0.5))
        trade_amount = float(kwargs.get("trade_amount", 0))
        if supply <= 0 or reserve_balance <= 0 or reserve_ratio <= 0:
            raise ValueError("supply, reserve_balance, reserve_ratio must be positive")
        if not 0 < reserve_ratio <= 1:
            raise ValueError("reserve_ratio must be within (0, 1]")
        current_price = reserve_balance / (supply * reserve_ratio)
        if curve == "linear":
            price_after_buy = current_price * (1 + trade_amount / supply)
            price_after_sell = max(0.0, current_price * (1 - trade_amount / supply))
        elif curve == "exponential":
            price_after_buy = current_price * math.exp(trade_amount / supply)
            price_after_sell = max(0.0, current_price * math.exp(-trade_amount / supply))
        elif curve == "polynomial":
            price_after_buy = current_price * (1 + (trade_amount / supply) ** 2)
            price_after_sell = max(0.0, current_price * (1 - (trade_amount / supply) ** 2))
        elif curve == "sigmoid":
            price_after_buy = current_price / (1 + math.exp(-trade_amount / supply))
            price_after_sell = current_price / (1 + math.exp(trade_amount / supply))
        else:
            raise ValueError("Unsupported curve_type")
        slippage = (price_after_buy - price_after_sell) / max(current_price, 1e-9)
        curve_visualization_points = [
            {"trade": delta, "price": reserve_balance / ((supply + delta) * reserve_ratio)}
            for delta in (-trade_amount, 0, trade_amount)
        ]
        return {
            "status": "success",
            "data": {
                "current_price": current_price,
                "price_after_buy": price_after_buy,
                "price_after_sell": price_after_sell,
                "slippage": slippage,
                "curve_visualization_points": curve_visualization_points
            },
            "timestamp": datetime.now(timezone.utc).isoformat()
        }
    except (ValueError, TypeError, ZeroDivisionError) as e:
        logger.error(f"bonding_curve_pricer failed: {e}")
        _log_lesson(f"bonding_curve_pricer: {e}")
        return {"status": "error", "error": str(e), "timestamp": datetime.now(timezone.utc).isoformat()}


def _log_lesson(message: str) -> None:
    try:
        with open("logs/lessons.md", "a", encoding="utf-8") as file:
            file.write(f"- [{datetime.now(timezone.utc).isoformat()}] {message}\n")
    except OSError:
        pass
