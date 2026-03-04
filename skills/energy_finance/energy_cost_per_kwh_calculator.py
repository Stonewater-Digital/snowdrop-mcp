"""Calculate energy cost per kWh and compare to national average.

MCP Tool Name: energy_cost_per_kwh_calculator
"""
from __future__ import annotations
from datetime import datetime, timezone
from typing import Any

TOOL_META: dict[str, Any] = {
    "name": "energy_cost_per_kwh_calculator",
    "description": "Calculate electricity cost per kWh from monthly bill and usage. Compares to the US national average (~$0.16/kWh).",
    "inputSchema": {
        "type": "object",
        "properties": {
            "monthly_bill": {
                "type": "number",
                "description": "Monthly electricity bill in USD.",
            },
            "kwh_used": {
                "type": "number",
                "description": "Kilowatt-hours consumed in the billing period.",
            },
        },
        "required": ["monthly_bill", "kwh_used"],
    },
}

_NATIONAL_AVG = 0.16  # US average residential rate $/kWh


def energy_cost_per_kwh_calculator(
    monthly_bill: float,
    kwh_used: float,
) -> dict[str, Any]:
    """Calculate energy cost per kWh."""
    try:
        if kwh_used <= 0:
            return {
                "status": "error",
                "data": {"error": "kwh_used must be positive."},
                "timestamp": datetime.now(timezone.utc).isoformat(),
            }
        if monthly_bill < 0:
            return {
                "status": "error",
                "data": {"error": "monthly_bill must be non-negative."},
                "timestamp": datetime.now(timezone.utc).isoformat(),
            }

        cost_per_kwh = monthly_bill / kwh_used
        vs_national = cost_per_kwh - _NATIONAL_AVG
        vs_national_pct = (vs_national / _NATIONAL_AVG * 100) if _NATIONAL_AVG > 0 else 0

        annual_cost = monthly_bill * 12
        annual_kwh = kwh_used * 12

        if cost_per_kwh < 0.10:
            assessment = "Very low — well below national average."
        elif cost_per_kwh < 0.14:
            assessment = "Below average — competitive rate."
        elif cost_per_kwh < 0.18:
            assessment = "Near national average."
        elif cost_per_kwh < 0.25:
            assessment = "Above average — consider efficiency improvements or rate shopping."
        else:
            assessment = "High — significantly above average. Investigate alternative providers or solar."

        return {
            "status": "ok",
            "data": {
                "monthly_bill": round(monthly_bill, 2),
                "kwh_used": round(kwh_used, 2),
                "cost_per_kwh": round(cost_per_kwh, 4),
                "national_average": _NATIONAL_AVG,
                "vs_national_avg": round(vs_national, 4),
                "vs_national_avg_pct": round(vs_national_pct, 1),
                "estimated_annual_cost": round(annual_cost, 2),
                "estimated_annual_kwh": round(annual_kwh, 2),
                "assessment": assessment,
            },
            "timestamp": datetime.now(timezone.utc).isoformat(),
        }
    except Exception as exc:
        return {
            "status": "error",
            "data": {"error": str(exc)},
            "timestamp": datetime.now(timezone.utc).isoformat(),
        }
