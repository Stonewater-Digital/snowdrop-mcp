"""Analyze revolving credit costs: utilization, annual interest, and cost per dollar borrowed.

MCP Tool Name: revolving_credit_analyzer
"""
from __future__ import annotations
from datetime import datetime, timezone
from typing import Any

TOOL_META: dict[str, Any] = {
    "name": "revolving_credit_analyzer",
    "description": "Analyze revolving credit costs including annual interest cost, utilization ratio, and cost per dollar borrowed.",
    "inputSchema": {
        "type": "object",
        "properties": {
            "credit_limit": {"type": "number", "description": "Total credit limit."},
            "avg_balance": {"type": "number", "description": "Average revolving balance."},
            "apr": {"type": "number", "description": "Annual Percentage Rate as decimal."},
        },
        "required": ["credit_limit", "avg_balance", "apr"],
    },
}


def revolving_credit_analyzer(
    credit_limit: float, avg_balance: float, apr: float
) -> dict[str, Any]:
    """Analyze revolving credit costs."""
    try:
        if credit_limit <= 0:
            return {
                "status": "error",
                "data": {"error": "credit_limit must be positive."},
                "timestamp": datetime.now(timezone.utc).isoformat(),
            }

        utilization = (avg_balance / credit_limit) * 100 if credit_limit > 0 else 0.0
        annual_interest = avg_balance * apr
        cost_per_dollar = apr if avg_balance > 0 else 0.0

        return {
            "status": "ok",
            "data": {
                "credit_limit": credit_limit,
                "avg_balance": avg_balance,
                "apr_pct": round(apr * 100, 4),
                "utilization_pct": round(utilization, 2),
                "annual_interest_cost": round(annual_interest, 2),
                "monthly_interest_cost": round(annual_interest / 12, 2),
                "cost_per_dollar_borrowed": round(cost_per_dollar, 4),
            },
            "timestamp": datetime.now(timezone.utc).isoformat(),
        }
    except Exception as exc:
        return {
            "status": "error",
            "data": {"error": str(exc)},
            "timestamp": datetime.now(timezone.utc).isoformat(),
        }
