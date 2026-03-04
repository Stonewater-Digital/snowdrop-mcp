"""
Execuve Summary: Analyzes bull/bear put spreads for payoff and risk metrics.
Inputs: short_strike (float), short_premium (float), long_strike (float), long_premium (float), contracts (int), option_type (str)
Outputs: max_profit (float), max_loss (float), breakeven (float), risk_reward_ratio (float), probability_of_profit_estimate (float)
MCP Tool Name: put_spread_calculator
"""
import logging
import math
from datetime import datetime, timezone
from typing import Any

logger = logging.getLogger("snowdrop.skills")

CONTRACT_SIZE = 100

TOOL_META = {
    "name": "put_spread_calculator",
    "description": "Calculates payoff metrics for bull or bear put spreads.",
    "inputSchema": {
        "type": "object",
        "properties": {
            "short_strike": {"type": "number", "description": "Strike sold."},
            "short_premium": {"type": "number", "description": "Premium received for short put."},
            "long_strike": {"type": "number", "description": "Strike bought."},
            "long_premium": {"type": "number", "description": "Premium paid for long put."},
            "contracts": {"type": "integer", "description": "Number of spreads."},
            "option_type": {"type": "string", "description": "bull or bear."}
        },
        "required": ["short_strike", "short_premium", "long_strike", "long_premium", "contracts", "option_type"]
    },
    "outputSchema": {
        "type": "object", "properties": {"status": {"type": "string"}, "timestamp": {"type": "string"}, "data": {"type": "object"}}, "required": ["status", "timestamp"]
    }
}


def put_spread_calculator(**kwargs: Any) -> dict:
    """Quantifies payoff of bull/bear put spreads."""
    try:
        short_strike = kwargs.get("short_strike")
        short_premium = kwargs.get("short_premium")
        long_strike = kwargs.get("long_strike")
        long_premium = kwargs.get("long_premium")
        contracts = kwargs.get("contracts")
        spread_type = kwargs.get("option_type", "bull").lower()
        for label, value in (("short_strike", short_strike), ("short_premium", short_premium), ("long_strike", long_strike), ("long_premium", long_premium)):
            if not isinstance(value, (int, float)):
                raise ValueError(f"{label} must be numeric")
        if not isinstance(contracts, int) or contracts <= 0:
            raise ValueError("contracts must be positive integer")
        if spread_type not in {"bull", "bear"}:
            raise ValueError("option_type must be 'bull' or 'bear'")

        credit = short_premium - long_premium
        width = abs(short_strike - long_strike)
        if spread_type == "bull":
            max_profit = credit * CONTRACT_SIZE * contracts
            max_loss = (width - credit) * CONTRACT_SIZE * contracts
            breakeven = short_strike - credit
        else:
            max_profit = (width - credit) * CONTRACT_SIZE * contracts
            max_loss = credit * CONTRACT_SIZE * contracts
            breakeven = short_strike - (width - credit)
        risk_reward_ratio = max_profit / max_loss if max_loss else math.inf
        pop_estimate = max_profit / (max_profit + max_loss) if (max_profit + max_loss) else 0

        return {
            "status": "success",
            "data": {
                "max_profit": max_profit,
                "max_loss": max_loss,
                "breakeven": breakeven,
                "risk_reward_ratio": risk_reward_ratio,
                "probability_of_profit_estimate": pop_estimate
            },
            "timestamp": datetime.now(timezone.utc).isoformat()
        }
    except (ValueError, TypeError, ZeroDivisionError) as e:
        logger.error(f"put_spread_calculator failed: {e}")
        _log_lesson(f"put_spread_calculator: {e}")
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
