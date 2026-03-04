"""Calculate breakeven spend to justify a credit card annual fee via rewards.

MCP Tool Name: annual_fee_breakeven_calculator
"""
from __future__ import annotations
from datetime import datetime, timezone
from typing import Any

TOOL_META: dict[str, Any] = {
    "name": "annual_fee_breakeven_calculator",
    "description": "Calculate how much you need to spend to break even on a credit card's annual fee through rewards earnings.",
    "inputSchema": {
        "type": "object",
        "properties": {
            "annual_fee": {"type": "number", "description": "Card annual fee in dollars."},
            "rewards_rate_pct": {"type": "number", "description": "Rewards rate as percentage (e.g., 2.0 for 2%)."},
            "avg_monthly_spend": {"type": "number", "description": "Average monthly spending on the card."},
        },
        "required": ["annual_fee", "rewards_rate_pct", "avg_monthly_spend"],
    },
}


def annual_fee_breakeven_calculator(
    annual_fee: float, rewards_rate_pct: float, avg_monthly_spend: float
) -> dict[str, Any]:
    """Calculate breakeven spend for card annual fee."""
    try:
        if rewards_rate_pct <= 0:
            return {
                "status": "error",
                "data": {"error": "rewards_rate_pct must be positive."},
                "timestamp": datetime.now(timezone.utc).isoformat(),
            }

        rewards_rate = rewards_rate_pct / 100
        breakeven_annual_spend = annual_fee / rewards_rate
        breakeven_monthly_spend = breakeven_annual_spend / 12

        annual_spend = avg_monthly_spend * 12
        annual_rewards = annual_spend * rewards_rate
        net_value = annual_rewards - annual_fee

        months_to_breakeven = None
        if avg_monthly_spend > 0 and rewards_rate > 0:
            monthly_rewards = avg_monthly_spend * rewards_rate
            if monthly_rewards > 0:
                months_to_breakeven = round(annual_fee / monthly_rewards, 1)

        return {
            "status": "ok",
            "data": {
                "annual_fee": annual_fee,
                "rewards_rate_pct": rewards_rate_pct,
                "avg_monthly_spend": avg_monthly_spend,
                "breakeven_annual_spend": round(breakeven_annual_spend, 2),
                "breakeven_monthly_spend": round(breakeven_monthly_spend, 2),
                "annual_rewards_earned": round(annual_rewards, 2),
                "net_annual_value": round(net_value, 2),
                "months_to_breakeven": months_to_breakeven,
                "worth_it": net_value > 0,
            },
            "timestamp": datetime.now(timezone.utc).isoformat(),
        }
    except Exception as exc:
        return {
            "status": "error",
            "data": {"error": str(exc)},
            "timestamp": datetime.now(timezone.utc).isoformat(),
        }
