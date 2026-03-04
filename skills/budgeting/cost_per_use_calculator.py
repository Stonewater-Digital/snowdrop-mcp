"""Calculate cost per use for a purchase to evaluate value.

MCP Tool Name: cost_per_use_calculator
"""
from __future__ import annotations
from datetime import datetime, timezone
from typing import Any

TOOL_META: dict[str, Any] = {
    "name": "cost_per_use_calculator",
    "description": "Calculates cost per use for a purchase and provides value assessment.",
    "inputSchema": {
        "type": "object",
        "properties": {
            "purchase_price": {
                "type": "number",
                "description": "The purchase price in dollars.",
            },
            "expected_uses": {
                "type": "integer",
                "description": "The expected number of times the item will be used.",
            },
        },
        "required": ["purchase_price", "expected_uses"],
    },
}


def cost_per_use_calculator(purchase_price: float, expected_uses: int) -> dict[str, Any]:
    """Calculates cost per use for a purchase."""
    try:
        if purchase_price <= 0:
            return {
                "status": "error",
                "data": {"error": "Purchase price must be a positive number."},
                "timestamp": datetime.now(timezone.utc).isoformat(),
            }
        if expected_uses <= 0:
            return {
                "status": "error",
                "data": {"error": "Expected uses must be at least 1."},
                "timestamp": datetime.now(timezone.utc).isoformat(),
            }

        cost_per_use = round(purchase_price / expected_uses, 2)

        # Value assessment
        if cost_per_use < 1:
            assessment = "Excellent value — less than $1 per use."
        elif cost_per_use < 5:
            assessment = "Good value — reasonable cost per use."
        elif cost_per_use < 20:
            assessment = "Moderate value — consider if there are cheaper alternatives."
        else:
            assessment = "Low value — high cost per use. Consider renting, borrowing, or finding a more affordable option."

        # Break-even comparison points
        breakeven_points = {}
        for target_cpu in [1.0, 2.0, 5.0]:
            uses_needed = round(purchase_price / target_cpu)
            if uses_needed > expected_uses:
                breakeven_points[f"${target_cpu:.2f}_per_use"] = {
                    "uses_needed": uses_needed,
                    "additional_uses": uses_needed - expected_uses,
                }

        return {
            "status": "ok",
            "data": {
                "purchase_price": purchase_price,
                "expected_uses": expected_uses,
                "cost_per_use": cost_per_use,
                "assessment": assessment,
                "breakeven_targets": breakeven_points if breakeven_points else "Already below all standard thresholds.",
            },
            "timestamp": datetime.now(timezone.utc).isoformat(),
        }
    except Exception as exc:
        return {
            "status": "error",
            "data": {"error": str(exc)},
            "timestamp": datetime.now(timezone.utc).isoformat(),
        }
