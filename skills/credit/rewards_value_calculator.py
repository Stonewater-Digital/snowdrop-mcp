"""Calculate annual rewards value from credit card spending.

MCP Tool Name: rewards_value_calculator
"""
from __future__ import annotations
from datetime import datetime, timezone
from typing import Any

TOOL_META: dict[str, Any] = {
    "name": "rewards_value_calculator",
    "description": "Calculate the annual dollar value of credit card rewards based on monthly spending, rewards rate, and point value.",
    "inputSchema": {
        "type": "object",
        "properties": {
            "monthly_spend": {"type": "number", "description": "Average monthly credit card spending."},
            "rewards_rate_pct": {"type": "number", "description": "Rewards earning rate as percentage (e.g., 2.0 for 2%)."},
            "point_value": {"type": "number", "description": "Dollar value per point/mile (default 0.01).", "default": 0.01},
        },
        "required": ["monthly_spend", "rewards_rate_pct"],
    },
}


def rewards_value_calculator(
    monthly_spend: float, rewards_rate_pct: float, point_value: float = 0.01
) -> dict[str, Any]:
    """Calculate annual rewards value."""
    try:
        if monthly_spend < 0:
            return {
                "status": "error",
                "data": {"error": "monthly_spend must be non-negative."},
                "timestamp": datetime.now(timezone.utc).isoformat(),
            }

        rewards_rate = rewards_rate_pct / 100
        annual_spend = monthly_spend * 12
        annual_points = annual_spend * rewards_rate
        # If point_value == 0.01, then effectively rewards_rate_pct% cashback
        annual_value = annual_points * point_value
        monthly_value = annual_value / 12

        return {
            "status": "ok",
            "data": {
                "monthly_spend": monthly_spend,
                "annual_spend": round(annual_spend, 2),
                "rewards_rate_pct": rewards_rate_pct,
                "point_value": point_value,
                "annual_points_earned": round(annual_points, 2),
                "annual_rewards_value": round(annual_value, 2),
                "monthly_rewards_value": round(monthly_value, 2),
            },
            "timestamp": datetime.now(timezone.utc).isoformat(),
        }
    except Exception as exc:
        return {
            "status": "error",
            "data": {"error": str(exc)},
            "timestamp": datetime.now(timezone.utc).isoformat(),
        }
