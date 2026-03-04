"""Calculate inventory reorder point given demand, lead time, and safety stock.

MCP Tool Name: inventory_reorder_point_calculator
"""
from __future__ import annotations
from datetime import datetime, timezone
from typing import Any

TOOL_META: dict[str, Any] = {
    "name": "inventory_reorder_point_calculator",
    "description": "Calculate the inventory reorder point: ROP = daily_demand * lead_time_days + safety_stock.",
    "inputSchema": {
        "type": "object",
        "properties": {
            "daily_demand": {"type": "number", "description": "Average daily unit demand."},
            "lead_time_days": {"type": "number", "description": "Supplier lead time in days."},
            "safety_stock": {"type": "number", "description": "Safety stock units (default 0).", "default": 0},
        },
        "required": ["daily_demand", "lead_time_days"],
    },
}


def inventory_reorder_point_calculator(
    daily_demand: float, lead_time_days: float, safety_stock: float = 0
) -> dict[str, Any]:
    """Calculate inventory reorder point."""
    try:
        if daily_demand < 0 or lead_time_days < 0 or safety_stock < 0:
            return {
                "status": "error",
                "data": {"error": "All inputs must be non-negative."},
                "timestamp": datetime.now(timezone.utc).isoformat(),
            }

        demand_during_lead = daily_demand * lead_time_days
        rop = demand_during_lead + safety_stock

        return {
            "status": "ok",
            "data": {
                "daily_demand": daily_demand,
                "lead_time_days": lead_time_days,
                "safety_stock": safety_stock,
                "demand_during_lead_time": round(demand_during_lead, 2),
                "reorder_point": round(rop, 2),
            },
            "timestamp": datetime.now(timezone.utc).isoformat(),
        }
    except Exception as exc:
        return {
            "status": "error",
            "data": {"error": str(exc)},
            "timestamp": datetime.now(timezone.utc).isoformat(),
        }
