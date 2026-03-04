"""Calculate markup percentage from cost and selling price.

MCP Tool Name: markup_calculator
"""
from __future__ import annotations
from datetime import datetime, timezone
from typing import Any

TOOL_META: dict[str, Any] = {
    "name": "markup_calculator",
    "description": "Calculate markup percentage: (selling_price - cost) / cost * 100.",
    "inputSchema": {
        "type": "object",
        "properties": {
            "cost": {"type": "number", "description": "Product cost."},
            "selling_price": {"type": "number", "description": "Selling price."},
        },
        "required": ["cost", "selling_price"],
    },
}


def markup_calculator(cost: float, selling_price: float) -> dict[str, Any]:
    """Calculate markup percentage."""
    try:
        if cost <= 0:
            return {
                "status": "error",
                "data": {"error": "cost must be positive."},
                "timestamp": datetime.now(timezone.utc).isoformat(),
            }

        markup = (selling_price - cost) / cost * 100

        return {
            "status": "ok",
            "data": {
                "cost": cost,
                "selling_price": selling_price,
                "profit": round(selling_price - cost, 2),
                "markup_pct": round(markup, 2),
            },
            "timestamp": datetime.now(timezone.utc).isoformat(),
        }
    except Exception as exc:
        return {
            "status": "error",
            "data": {"error": str(exc)},
            "timestamp": datetime.now(timezone.utc).isoformat(),
        }
