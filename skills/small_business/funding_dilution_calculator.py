"""
Executive Smary: Models ownership dilution across venture rounds including option pool refresh.
Inputs: rounds (list), founder_shares (float), option_pool_pct (float)
Outputs: ownership_after_each_round (list), dilution_per_round (list), share_price_per_round (list), total_dilution (float)
MCP Tool Name: funding_dilution_calculator
"""
import logging
from datetime import datetime, timezone
from typing import Any, Dict, List

logger = logging.getLogger("snowdrop.skills")

TOOL_META = {
    "name": "funding_dilution_calculator",
    "description": (
        "Walks through successive funding rounds to compute new share issuances, share "
        "prices, ownership percentages, and aggregate dilution for founders."
    ),
    "inputSchema": {
        "type": "object",
        "properties": {
            "rounds": {
                "type": "array",
                "description": "Funding rounds with name, pre_money_valuation, and investment_amount.",
                "items": {"type": "object"},
            },
            "founder_shares": {
                "type": "number",
                "description": "Outstanding founder shares prior to fundraising.",
            },
            "option_pool_pct": {
                "type": "number",
                "description": "Option pool target as decimal percentage of post-money.",
            },
        },
        "required": ["rounds", "founder_shares", "option_pool_pct"],
    },
    "outputSchema": {
        "type": "object",
        "properties": {
            "status": {"type": "string"},
            "timestamp": {"type": "string"},
            "data": {"type": "object"},
        },
        "required": ["status", "timestamp"],
    },
}


def funding_dilution_calculator(**kwargs: Any) -> dict:
    """Simulate dilution round-by-round based on pre-money valuations and investment amounts."""
    try:
        rounds_input = kwargs["rounds"]
        founder_shares = float(kwargs["founder_shares"])
        option_pool_pct = float(kwargs["option_pool_pct"])

        if not isinstance(rounds_input, list) or not rounds_input:
            raise ValueError("rounds must be a non-empty list")
        if founder_shares <= 0:
            raise ValueError("founder_shares must be positive")

        total_shares = founder_shares / (1 - option_pool_pct)
        founder_pct = founder_shares / total_shares
        ownership_history: List[Dict[str, Any]] = []
        dilution_per_round: List[Dict[str, Any]] = []
        share_prices: List[Dict[str, Any]] = []

        for round_data in rounds_input:
            name = str(round_data["name"])
            pre_money = float(round_data["pre_money_valuation"])
            investment = float(round_data["investment_amount"])
            share_price = pre_money / total_shares
            new_shares = investment / share_price
            total_shares += new_shares
            founder_pct = founder_shares / total_shares
            ownership_history.append({"round": name, "founder_pct": founder_pct})
            dilution_per_round.append({"round": name, "dilution": 1 - founder_pct})
            share_prices.append({"round": name, "share_price": share_price})

        total_dilution = 1 - founder_pct

        return {
            "status": "success",
            "data": {
                "ownership_after_each_round": ownership_history,
                "dilution_per_round": dilution_per_round,
                "share_price_per_round": share_prices,
                "total_dilution": total_dilution,
            },
            "timestamp": datetime.now(timezone.utc).isoformat(),
        }
    except (ValueError, TypeError, ZeroDivisionError) as e:
        logger.error(f"funding_dilution_calculator failed: {e}")
        _log_lesson(f"funding_dilution_calculator: {e}")
        return {
            "status": "error",
            "error": str(e),
            "timestamp": datetime.now(timezone.utc).isoformat(),
        }


def _log_lesson(message: str) -> None:
    try:
        with open("logs/lessons.md", "a") as f:
            f.write(f"- [{datetime.now(timezone.utc).isoformat()}] {message}\n")
    except OSError:
        pass
