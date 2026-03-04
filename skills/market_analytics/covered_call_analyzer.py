"""
Execuve Summary: Evaluates a covered call trade's payoff metrics.
Inputs: stock_price (float), strike (float), premium (float), days_to_expiry (int), cost_basis (float)
Outputs: max_profit (float), max_profit_pct (float), downside_protection_pct (float), breakeven (float), static_return (float), if_called_return (float), annualized_return (float)
MCP Tool Name: covered_call_analyzer
"""
import logging
import math
from datetime import datetime, timezone
from typing import Any

logger = logging.getLogger("snowdrop.skills")

TOOL_META = {
    "name": "covered_call_analyzer",
    "description": "Computes payoff, breakeven, and annualized returns for a covered call position.",
    "inputSchema": {
        "type": "object",
        "properties": {
            "stock_price": {"type": "number", "description": "Current stock price."},
            "strike": {"type": "number", "description": "Call strike price."},
            "premium": {"type": "number", "description": "Premium received per share."},
            "days_to_expiry": {"type": "integer", "description": "Days until option expiration."},
            "cost_basis": {"type": "number", "description": "Underlying cost basis per share."}
        },
        "required": ["stock_price", "strike", "premium", "days_to_expiry", "cost_basis"]
    },
    "outputSchema": {
        "type": "object", "properties": {"status": {"type": "string"}, "timestamp": {"type": "string"}, "data": {"type": "object"}}, "required": ["status", "timestamp"]
    }
}


def covered_call_analyzer(**kwargs: Any) -> dict:
    """Evaluates key payoff stats for a covered call trade."""
    try:
        stock_price = kwargs.get("stock_price")
        strike = kwargs.get("strike")
        premium = kwargs.get("premium")
        days = kwargs.get("days_to_expiry")
        cost_basis = kwargs.get("cost_basis")
        for label, value in (("stock_price", stock_price), ("strike", strike), ("premium", premium), ("days_to_expiry", days), ("cost_basis", cost_basis)):
            if not isinstance(value, (int, float)) or value <= 0:
                raise ValueError(f"{label} must be positive number")

        max_profit = (strike - cost_basis) + premium if strike >= cost_basis else premium + (strike - cost_basis)
        max_profit_pct = max_profit / cost_basis
        breakeven = cost_basis - premium
        downside_protection_pct = premium / cost_basis
        static_return = premium / cost_basis
        if_called_return = max_profit_pct
        annualized_return = (if_called_return) * (365 / days)

        return {
            "status": "success",
            "data": {
                "max_profit": max_profit,
                "max_profit_pct": max_profit_pct,
                "downside_protection_pct": downside_protection_pct,
                "breakeven": breakeven,
                "static_return": static_return,
                "if_called_return": if_called_return,
                "annualized_return": annualized_return
            },
            "timestamp": datetime.now(timezone.utc).isoformat()
        }
    except (ValueError, TypeError, ZeroDivisionError) as e:
        logger.error(f"covered_call_analyzer failed: {e}")
        _log_lesson(f"covered_call_analyzer: {e}")
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
