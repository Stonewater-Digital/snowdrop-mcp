"""Calculate customer churn rate and annualized churn.

MCP Tool Name: churn_rate_calculator
"""
from __future__ import annotations
from datetime import datetime, timezone
from typing import Any

TOOL_META: dict[str, Any] = {
    "name": "churn_rate_calculator",
    "description": "Calculate customer churn rate for a period and annualized churn rate.",
    "inputSchema": {
        "type": "object",
        "properties": {
            "start_customers": {"type": "integer", "description": "Customers at start of period."},
            "lost_customers": {"type": "integer", "description": "Customers lost during the period."},
            "period_months": {"type": "integer", "description": "Period length in months (default 1).", "default": 1},
        },
        "required": ["start_customers", "lost_customers"],
    },
}


def churn_rate_calculator(
    start_customers: int, lost_customers: int, period_months: int = 1
) -> dict[str, Any]:
    """Calculate churn rate and annualized churn."""
    try:
        if start_customers <= 0:
            return {
                "status": "error",
                "data": {"error": "start_customers must be positive."},
                "timestamp": datetime.now(timezone.utc).isoformat(),
            }
        if lost_customers < 0:
            return {
                "status": "error",
                "data": {"error": "lost_customers must be non-negative."},
                "timestamp": datetime.now(timezone.utc).isoformat(),
            }
        if period_months <= 0:
            return {
                "status": "error",
                "data": {"error": "period_months must be positive."},
                "timestamp": datetime.now(timezone.utc).isoformat(),
            }

        churn_pct = (lost_customers / start_customers) * 100
        monthly_churn = churn_pct / period_months
        # Annualized: 1 - (1 - monthly_rate)^12
        annualized = (1 - (1 - monthly_churn / 100) ** 12) * 100
        retention_pct = 100 - churn_pct

        return {
            "status": "ok",
            "data": {
                "start_customers": start_customers,
                "lost_customers": lost_customers,
                "period_months": period_months,
                "churn_rate_pct": round(churn_pct, 2),
                "monthly_churn_pct": round(monthly_churn, 2),
                "annualized_churn_pct": round(annualized, 2),
                "retention_rate_pct": round(retention_pct, 2),
            },
            "timestamp": datetime.now(timezone.utc).isoformat(),
        }
    except Exception as exc:
        return {
            "status": "error",
            "data": {"error": str(exc)},
            "timestamp": datetime.now(timezone.utc).isoformat(),
        }
