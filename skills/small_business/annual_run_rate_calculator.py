"""Calculate Annual Run Rate (ARR) from a partial period's revenue.

MCP Tool Name: annual_run_rate_calculator
"""
from __future__ import annotations
from datetime import datetime, timezone
from typing import Any

TOOL_META: dict[str, Any] = {
    "name": "annual_run_rate_calculator",
    "description": "Calculate Annual Run Rate by annualizing a partial period's revenue: ARR = revenue * (12 / period_months).",
    "inputSchema": {
        "type": "object",
        "properties": {
            "current_period_revenue": {"type": "number", "description": "Revenue earned in the current period."},
            "period_months": {"type": "number", "description": "Number of months in the current period."},
        },
        "required": ["current_period_revenue", "period_months"],
    },
}


def annual_run_rate_calculator(
    current_period_revenue: float, period_months: float
) -> dict[str, Any]:
    """Calculate Annual Run Rate from partial-period revenue."""
    try:
        if period_months <= 0:
            return {
                "status": "error",
                "data": {"error": "period_months must be positive."},
                "timestamp": datetime.now(timezone.utc).isoformat(),
            }

        arr = current_period_revenue * (12 / period_months)
        monthly_avg = current_period_revenue / period_months

        return {
            "status": "ok",
            "data": {
                "current_period_revenue": current_period_revenue,
                "period_months": period_months,
                "monthly_average": round(monthly_avg, 2),
                "annual_run_rate": round(arr, 2),
            },
            "timestamp": datetime.now(timezone.utc).isoformat(),
        }
    except Exception as exc:
        return {
            "status": "error",
            "data": {"error": str(exc)},
            "timestamp": datetime.now(timezone.utc).isoformat(),
        }
