"""Calculate vacancy rate and estimate revenue loss.

MCP Tool Name: vacancy_rate_calculator
"""
from __future__ import annotations
from datetime import datetime, timezone
from typing import Any

TOOL_META: dict[str, Any] = {
    "name": "vacancy_rate_calculator",
    "description": "Calculate vacancy rate from total and vacant units. Estimates revenue loss based on vacancy.",
    "inputSchema": {
        "type": "object",
        "properties": {
            "total_units": {
                "type": "integer",
                "description": "Total number of units in the property.",
            },
            "vacant_units": {
                "type": "integer",
                "description": "Number of currently vacant units.",
            },
        },
        "required": ["total_units", "vacant_units"],
    },
}


def vacancy_rate_calculator(
    total_units: int,
    vacant_units: int,
) -> dict[str, Any]:
    """Calculate vacancy rate and estimate revenue loss."""
    try:
        if total_units <= 0:
            return {
                "status": "error",
                "data": {"error": "total_units must be positive."},
                "timestamp": datetime.now(timezone.utc).isoformat(),
            }
        if vacant_units < 0 or vacant_units > total_units:
            return {
                "status": "error",
                "data": {"error": "vacant_units must be between 0 and total_units."},
                "timestamp": datetime.now(timezone.utc).isoformat(),
            }

        occupied = total_units - vacant_units
        vacancy_rate = vacant_units / total_units * 100
        occupancy_rate = occupied / total_units * 100

        # National average vacancy rate ~6%
        national_avg = 6.0
        vs_national = vacancy_rate - national_avg

        if vacancy_rate <= 3:
            assessment = "Very low vacancy — strong demand, possible rent increase opportunity."
        elif vacancy_rate <= 6:
            assessment = "Healthy vacancy — near market equilibrium."
        elif vacancy_rate <= 10:
            assessment = "Elevated vacancy — review pricing, marketing, and property condition."
        else:
            assessment = "High vacancy — significant revenue loss. Investigate market conditions and property issues."

        return {
            "status": "ok",
            "data": {
                "total_units": total_units,
                "vacant_units": vacant_units,
                "occupied_units": occupied,
                "vacancy_rate_pct": round(vacancy_rate, 2),
                "occupancy_rate_pct": round(occupancy_rate, 2),
                "vs_national_avg_pct": round(vs_national, 2),
                "assessment": assessment,
                "note": "Revenue loss = vacancy_rate * potential_gross_income. Provide gross income to net_operating_income_calculator for full analysis.",
            },
            "timestamp": datetime.now(timezone.utc).isoformat(),
        }
    except Exception as exc:
        return {
            "status": "error",
            "data": {"error": str(exc)},
            "timestamp": datetime.now(timezone.utc).isoformat(),
        }
