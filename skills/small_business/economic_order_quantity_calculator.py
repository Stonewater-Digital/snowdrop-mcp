"""Calculate Economic Order Quantity (EOQ) using the Wilson formula.

MCP Tool Name: economic_order_quantity_calculator
"""
from __future__ import annotations
import math
from datetime import datetime, timezone
from typing import Any

TOOL_META: dict[str, Any] = {
    "name": "economic_order_quantity_calculator",
    "description": "Calculate the Economic Order Quantity (EOQ): the optimal order size that minimizes total inventory costs. EOQ = sqrt(2 * annual_demand * order_cost / holding_cost).",
    "inputSchema": {
        "type": "object",
        "properties": {
            "annual_demand": {"type": "number", "description": "Annual unit demand."},
            "order_cost": {"type": "number", "description": "Cost per order placed."},
            "holding_cost": {"type": "number", "description": "Annual holding cost per unit."},
        },
        "required": ["annual_demand", "order_cost", "holding_cost"],
    },
}


def economic_order_quantity_calculator(
    annual_demand: float, order_cost: float, holding_cost: float
) -> dict[str, Any]:
    """Calculate Economic Order Quantity."""
    try:
        if annual_demand <= 0 or order_cost <= 0 or holding_cost <= 0:
            return {
                "status": "error",
                "data": {"error": "All inputs must be positive."},
                "timestamp": datetime.now(timezone.utc).isoformat(),
            }

        eoq = math.sqrt(2 * annual_demand * order_cost / holding_cost)
        orders_per_year = annual_demand / eoq
        total_order_cost = orders_per_year * order_cost
        total_holding_cost = (eoq / 2) * holding_cost
        total_cost = total_order_cost + total_holding_cost

        return {
            "status": "ok",
            "data": {
                "annual_demand": annual_demand,
                "order_cost": order_cost,
                "holding_cost_per_unit": holding_cost,
                "eoq": round(eoq, 2),
                "orders_per_year": round(orders_per_year, 2),
                "total_annual_order_cost": round(total_order_cost, 2),
                "total_annual_holding_cost": round(total_holding_cost, 2),
                "total_annual_inventory_cost": round(total_cost, 2),
            },
            "timestamp": datetime.now(timezone.utc).isoformat(),
        }
    except Exception as exc:
        return {
            "status": "error",
            "data": {"error": str(exc)},
            "timestamp": datetime.now(timezone.utc).isoformat(),
        }
