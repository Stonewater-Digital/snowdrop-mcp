"""Calculate profit margin percentage from cost and selling price.

MCP Tool Name: margin_calculator
"""
from __future__ import annotations
from datetime import datetime, timezone
from typing import Any

TOOL_META: dict[str, Any] = {
    "name": "margin_calculator",
    "description": "Calculate profit margin percentage: (selling_price - cost) / selling_price * 100.",
    "inputSchema": {
        "type": "object",
        "properties": {
            "cost": {"type": "number", "description": "Product cost."},
            "selling_price": {"type": "number", "description": "Selling price."},
        },
        "required": ["cost", "selling_price"],
    },
}


def margin_calculator(cost: float, selling_price: float) -> dict[str, Any]:
    """Calculate profit margin percentage."""
    try:
        if selling_price <= 0:
            return {
                "status": "error",
                "data": {"error": "selling_price must be positive."},
                "timestamp": datetime.now(timezone.utc).isoformat(),
            }

        margin = (selling_price - cost) / selling_price * 100

        return {
            "status": "ok",
            "data": {
                "cost": cost,
                "selling_price": selling_price,
                "profit": round(selling_price - cost, 2),
                "margin_pct": round(margin, 2),
            },
            "timestamp": datetime.now(timezone.utc).isoformat(),
        }
    except Exception as exc:
        return {
            "status": "error",
            "data": {"error": str(exc)},
            "timestamp": datetime.now(timezone.utc).isoformat(),
        }
