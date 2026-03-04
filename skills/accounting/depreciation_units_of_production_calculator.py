"""Calculate units-of-production depreciation based on actual output.

MCP Tool Name: depreciation_units_of_production_calculator
"""
from __future__ import annotations

from datetime import datetime, timezone
from typing import Any

TOOL_META: dict[str, Any] = {
    "name": "depreciation_units_of_production_calculator",
    "description": (
        "Calculates depreciation using the units-of-production method, allocating "
        "cost based on actual units produced relative to total estimated output."
    ),
    "inputSchema": {
        "type": "object",
        "properties": {
            "cost": {
                "type": "number",
                "description": "Original cost of the asset.",
            },
            "salvage_value": {
                "type": "number",
                "description": "Estimated residual value at end of useful life.",
            },
            "total_units": {
                "type": "number",
                "description": "Total estimated units the asset can produce over its life.",
            },
            "units_produced": {
                "type": "number",
                "description": "Units actually produced in the current period.",
            },
        },
        "required": ["cost", "salvage_value", "total_units", "units_produced"],
    },
}


def depreciation_units_of_production_calculator(
    cost: float, salvage_value: float, total_units: float, units_produced: float
) -> dict[str, Any]:
    """Calculate units-of-production depreciation."""
    try:
        cost = float(cost)
        salvage_value = float(salvage_value)
        total_units = float(total_units)
        units_produced = float(units_produced)

        if total_units <= 0:
            raise ValueError("total_units must be greater than zero.")

        depreciable_base = cost - salvage_value
        rate_per_unit = depreciable_base / total_units
        depreciation = rate_per_unit * units_produced

        return {
            "status": "ok",
            "data": {
                "rate_per_unit": round(rate_per_unit, 4),
                "depreciation_expense": round(depreciation, 2),
                "depreciable_base": round(depreciable_base, 2),
                "units_produced": units_produced,
                "total_units": total_units,
            },
            "timestamp": datetime.now(timezone.utc).isoformat(),
        }
    except Exception as exc:
        return {
            "status": "error",
            "data": {"error": str(exc)},
            "timestamp": datetime.now(timezone.utc).isoformat(),
        }
