"""Calculate startup runway in months and estimated end date.

MCP Tool Name: runway_calculator
"""
from __future__ import annotations
from datetime import datetime, timezone, timedelta
from typing import Any

TOOL_META: dict[str, Any] = {
    "name": "runway_calculator",
    "description": "Calculate how many months of runway remain given current cash and monthly burn rate, plus estimated end date.",
    "inputSchema": {
        "type": "object",
        "properties": {
            "current_cash": {"type": "number", "description": "Current cash on hand."},
            "monthly_burn_rate": {"type": "number", "description": "Net monthly burn rate (positive = spending)."},
        },
        "required": ["current_cash", "monthly_burn_rate"],
    },
}


def runway_calculator(
    current_cash: float, monthly_burn_rate: float
) -> dict[str, Any]:
    """Calculate runway months and estimated end date."""
    try:
        if monthly_burn_rate <= 0:
            return {
                "status": "ok",
                "data": {
                    "current_cash": current_cash,
                    "monthly_burn_rate": monthly_burn_rate,
                    "runway_months": None,
                    "message": "Burn rate is zero or negative (profitable); runway is infinite.",
                },
                "timestamp": datetime.now(timezone.utc).isoformat(),
            }

        runway_months = current_cash / monthly_burn_rate
        now = datetime.now(timezone.utc)
        runway_date = now + timedelta(days=runway_months * 30.44)

        return {
            "status": "ok",
            "data": {
                "current_cash": current_cash,
                "monthly_burn_rate": monthly_burn_rate,
                "runway_months": round(runway_months, 1),
                "runway_years": round(runway_months / 12, 1),
                "estimated_end_date": runway_date.strftime("%Y-%m-%d"),
            },
            "timestamp": datetime.now(timezone.utc).isoformat(),
        }
    except Exception as exc:
        return {
            "status": "error",
            "data": {"error": str(exc)},
            "timestamp": datetime.now(timezone.utc).isoformat(),
        }
