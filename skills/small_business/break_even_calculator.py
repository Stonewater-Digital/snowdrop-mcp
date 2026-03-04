"""Calculate break-even point in units and revenue.

MCP Tool Name: break_even_calculator
"""
from __future__ import annotations
from datetime import datetime, timezone
from typing import Any

TOOL_META: dict[str, Any] = {
    "name": "break_even_calculator",
    "description": "Calculate the break-even point: units needed and revenue at which total costs equal total revenue.",
    "inputSchema": {
        "type": "object",
        "properties": {
            "fixed_costs": {"type": "number", "description": "Total fixed costs."},
            "price_per_unit": {"type": "number", "description": "Selling price per unit."},
            "variable_cost_per_unit": {"type": "number", "description": "Variable cost per unit."},
        },
        "required": ["fixed_costs", "price_per_unit", "variable_cost_per_unit"],
    },
}


def break_even_calculator(
    fixed_costs: float, price_per_unit: float, variable_cost_per_unit: float
) -> dict[str, Any]:
    """Calculate break-even point in units and revenue."""
    try:
        contribution_margin = price_per_unit - variable_cost_per_unit
        if contribution_margin <= 0:
            return {
                "status": "error",
                "data": {"error": "Price per unit must exceed variable cost per unit for a valid break-even."},
                "timestamp": datetime.now(timezone.utc).isoformat(),
            }

        units = fixed_costs / contribution_margin
        revenue = units * price_per_unit

        return {
            "status": "ok",
            "data": {
                "fixed_costs": fixed_costs,
                "price_per_unit": price_per_unit,
                "variable_cost_per_unit": variable_cost_per_unit,
                "contribution_margin": round(contribution_margin, 2),
                "break_even_units": round(units, 2),
                "break_even_revenue": round(revenue, 2),
            },
            "timestamp": datetime.now(timezone.utc).isoformat(),
        }
    except Exception as exc:
        return {
            "status": "error",
            "data": {"error": str(exc)},
            "timestamp": datetime.now(timezone.utc).isoformat(),
        }
