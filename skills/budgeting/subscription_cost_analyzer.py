"""Analyze total cost of subscriptions and identify savings opportunities.

MCP Tool Name: subscription_cost_analyzer
"""
from __future__ import annotations
from datetime import datetime, timezone
from typing import Any

TOOL_META: dict[str, Any] = {
    "name": "subscription_cost_analyzer",
    "description": "Analyzes subscription costs: total monthly and annual spending, sorted by cost.",
    "inputSchema": {
        "type": "object",
        "properties": {
            "subscriptions": {
                "type": "array",
                "description": "List of subscriptions with name and monthly cost.",
                "items": {
                    "type": "object",
                    "properties": {
                        "name": {"type": "string"},
                        "monthly_cost": {"type": "number"},
                    },
                    "required": ["name", "monthly_cost"],
                },
            },
        },
        "required": ["subscriptions"],
    },
}


def subscription_cost_analyzer(subscriptions: list[dict[str, Any]]) -> dict[str, Any]:
    """Analyzes subscription costs."""
    try:
        if not subscriptions:
            return {
                "status": "error",
                "data": {"error": "At least one subscription is required."},
                "timestamp": datetime.now(timezone.utc).isoformat(),
            }

        total_monthly = sum(s["monthly_cost"] for s in subscriptions)
        total_annual = round(total_monthly * 12, 2)

        breakdown = []
        for s in subscriptions:
            annual = round(s["monthly_cost"] * 12, 2)
            pct = round((s["monthly_cost"] / total_monthly) * 100, 2) if total_monthly > 0 else 0
            breakdown.append({
                "name": s["name"],
                "monthly_cost": round(s["monthly_cost"], 2),
                "annual_cost": annual,
                "percentage_of_total": pct,
            })

        breakdown.sort(key=lambda x: x["monthly_cost"], reverse=True)

        # Calculate what this money could be worth invested
        invested_10yr = round(total_monthly * 12 * (((1 + 0.07 / 12) ** 120 - 1) / (0.07 / 12)), 2)

        return {
            "status": "ok",
            "data": {
                "total_monthly": round(total_monthly, 2),
                "total_annual": total_annual,
                "num_subscriptions": len(subscriptions),
                "subscriptions_by_cost": breakdown,
                "most_expensive": breakdown[0]["name"] if breakdown else None,
                "daily_cost": round(total_annual / 365, 2),
                "investment_opportunity_cost_10yr": invested_10yr,
                "note": f"If you invested ${round(total_monthly, 2)}/month at 7% return for 10 years, it would grow to ${invested_10yr:,.2f}.",
            },
            "timestamp": datetime.now(timezone.utc).isoformat(),
        }
    except Exception as exc:
        return {
            "status": "error",
            "data": {"error": str(exc)},
            "timestamp": datetime.now(timezone.utc).isoformat(),
        }
