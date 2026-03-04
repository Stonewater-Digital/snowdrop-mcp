"""Calculate gross and net burn rate.

MCP Tool Name: burn_rate_calculator
"""
from __future__ import annotations
from datetime import datetime, timezone
from typing import Any

TOOL_META: dict[str, Any] = {
    "name": "burn_rate_calculator",
    "description": "Calculate gross burn rate (cash spent per month) and net burn rate (accounting for revenue). Gross burn = (starting_cash - ending_cash) / months.",
    "inputSchema": {
        "type": "object",
        "properties": {
            "starting_cash": {"type": "number", "description": "Cash at start of period."},
            "ending_cash": {"type": "number", "description": "Cash at end of period."},
            "months": {"type": "number", "description": "Number of months in the period."},
            "revenue": {"type": "number", "description": "Optional total revenue earned during the period.", "default": 0},
        },
        "required": ["starting_cash", "ending_cash", "months"],
    },
}


def burn_rate_calculator(
    starting_cash: float, ending_cash: float, months: float, revenue: float = 0
) -> dict[str, Any]:
    """Calculate gross and net burn rate."""
    try:
        if months <= 0:
            return {
                "status": "error",
                "data": {"error": "months must be positive."},
                "timestamp": datetime.now(timezone.utc).isoformat(),
            }

        net_burn = (starting_cash - ending_cash) / months
        # Gross burn = net burn + monthly revenue (total spending before revenue)
        monthly_revenue = revenue / months
        gross_burn = net_burn + monthly_revenue

        return {
            "status": "ok",
            "data": {
                "starting_cash": starting_cash,
                "ending_cash": ending_cash,
                "months": months,
                "total_revenue": revenue,
                "monthly_revenue": round(monthly_revenue, 2),
                "gross_burn_rate": round(gross_burn, 2),
                "net_burn_rate": round(net_burn, 2),
            },
            "timestamp": datetime.now(timezone.utc).isoformat(),
        }
    except Exception as exc:
        return {
            "status": "error",
            "data": {"error": str(exc)},
            "timestamp": datetime.now(timezone.utc).isoformat(),
        }
