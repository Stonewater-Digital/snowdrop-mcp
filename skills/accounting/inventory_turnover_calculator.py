"""Calculate inventory turnover ratio and days inventory outstanding.

MCP Tool Name: inventory_turnover_calculator
"""
from __future__ import annotations

from datetime import datetime, timezone
from typing import Any

TOOL_META: dict[str, Any] = {
    "name": "inventory_turnover_calculator",
    "description": (
        "Calculates inventory turnover ratio and average days to sell inventory."
    ),
    "inputSchema": {
        "type": "object",
        "properties": {
            "cogs": {
                "type": "number",
                "description": "Cost of goods sold for the period.",
            },
            "avg_inventory": {
                "type": "number",
                "description": "Average inventory value for the period.",
            },
        },
        "required": ["cogs", "avg_inventory"],
    },
}


def inventory_turnover_calculator(
    cogs: float, avg_inventory: float
) -> dict[str, Any]:
    """Calculate inventory turnover and days inventory outstanding."""
    try:
        cogs = float(cogs)
        avg_inventory = float(avg_inventory)

        if avg_inventory == 0:
            raise ValueError("avg_inventory must not be zero.")

        turnover = cogs / avg_inventory
        days_inventory = 365.0 / turnover if turnover != 0 else float("inf")

        return {
            "status": "ok",
            "data": {
                "turnover_ratio": round(turnover, 4),
                "days_inventory_outstanding": round(days_inventory, 2),
            },
            "timestamp": datetime.now(timezone.utc).isoformat(),
        }
    except Exception as exc:
        return {
            "status": "error",
            "data": {"error": str(exc)},
            "timestamp": datetime.now(timezone.utc).isoformat(),
        }
