"""Calculate customer retention rate.

MCP Tool Name: customer_retention_rate_calculator
"""
from __future__ import annotations
from datetime import datetime, timezone
from typing import Any

TOOL_META: dict[str, Any] = {
    "name": "customer_retention_rate_calculator",
    "description": "Calculate customer retention rate: retained = end_customers - new_customers; rate = retained / start_customers * 100.",
    "inputSchema": {
        "type": "object",
        "properties": {
            "start_customers": {"type": "integer", "description": "Customers at start of period."},
            "end_customers": {"type": "integer", "description": "Customers at end of period."},
            "new_customers": {"type": "integer", "description": "New customers acquired during the period."},
        },
        "required": ["start_customers", "end_customers", "new_customers"],
    },
}


def customer_retention_rate_calculator(
    start_customers: int, end_customers: int, new_customers: int
) -> dict[str, Any]:
    """Calculate customer retention rate."""
    try:
        if start_customers <= 0:
            return {
                "status": "error",
                "data": {"error": "start_customers must be positive."},
                "timestamp": datetime.now(timezone.utc).isoformat(),
            }

        retained = end_customers - new_customers
        lost = start_customers - retained
        retention_rate = (retained / start_customers) * 100
        churn_rate = 100 - retention_rate

        return {
            "status": "ok",
            "data": {
                "start_customers": start_customers,
                "end_customers": end_customers,
                "new_customers": new_customers,
                "retained_customers": retained,
                "lost_customers": lost,
                "retention_rate_pct": round(retention_rate, 2),
                "churn_rate_pct": round(churn_rate, 2),
            },
            "timestamp": datetime.now(timezone.utc).isoformat(),
        }
    except Exception as exc:
        return {
            "status": "error",
            "data": {"error": str(exc)},
            "timestamp": datetime.now(timezone.utc).isoformat(),
        }
