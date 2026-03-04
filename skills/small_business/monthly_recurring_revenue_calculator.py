"""Calculate Monthly Recurring Revenue (MRR) and ARR from subscription data.

MCP Tool Name: monthly_recurring_revenue_calculator
"""
from __future__ import annotations
from datetime import datetime, timezone
from typing import Any

TOOL_META: dict[str, Any] = {
    "name": "monthly_recurring_revenue_calculator",
    "description": "Calculate Monthly Recurring Revenue (MRR) and Annual Recurring Revenue (ARR) from a list of subscription plans.",
    "inputSchema": {
        "type": "object",
        "properties": {
            "subscriptions": {
                "type": "array",
                "description": "List of subscription plans.",
                "items": {
                    "type": "object",
                    "properties": {
                        "plan": {"type": "string", "description": "Plan name."},
                        "count": {"type": "integer", "description": "Number of subscribers."},
                        "price": {"type": "number", "description": "Monthly price per subscriber."},
                    },
                    "required": ["plan", "count", "price"],
                },
            },
        },
        "required": ["subscriptions"],
    },
}


def monthly_recurring_revenue_calculator(
    subscriptions: list[dict[str, Any]],
) -> dict[str, Any]:
    """Calculate MRR and ARR from subscription data."""
    try:
        if not subscriptions:
            return {
                "status": "error",
                "data": {"error": "subscriptions list must not be empty."},
                "timestamp": datetime.now(timezone.utc).isoformat(),
            }

        plan_details = []
        total_mrr = 0.0
        total_subs = 0
        for sub in subscriptions:
            plan_mrr = sub["count"] * sub["price"]
            total_mrr += plan_mrr
            total_subs += sub["count"]
            plan_details.append({
                "plan": sub["plan"],
                "subscribers": sub["count"],
                "price": sub["price"],
                "plan_mrr": round(plan_mrr, 2),
            })

        arr = total_mrr * 12
        arpu = total_mrr / total_subs if total_subs > 0 else 0

        return {
            "status": "ok",
            "data": {
                "plans": plan_details,
                "total_subscribers": total_subs,
                "mrr": round(total_mrr, 2),
                "arr": round(arr, 2),
                "arpu": round(arpu, 2),
            },
            "timestamp": datetime.now(timezone.utc).isoformat(),
        }
    except Exception as exc:
        return {
            "status": "error",
            "data": {"error": str(exc)},
            "timestamp": datetime.now(timezone.utc).isoformat(),
        }
