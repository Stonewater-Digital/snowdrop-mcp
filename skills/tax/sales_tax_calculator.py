"""Calculate sales tax given state and local rates.

MCP Tool Name: sales_tax_calculator
"""
from __future__ import annotations
from datetime import datetime, timezone
from typing import Any

TOOL_META: dict[str, Any] = {
    "name": "sales_tax_calculator",
    "description": "Calculate total sales tax from state and local rates. Returns tax amount, total cost, and combined rate.",
    "inputSchema": {
        "type": "object",
        "properties": {
            "purchase_amount": {
                "type": "number",
                "description": "Purchase amount before tax in USD.",
            },
            "state_rate": {
                "type": "number",
                "description": "State sales tax rate as a decimal (e.g. 0.06 for 6%).",
            },
            "local_rate": {
                "type": "number",
                "description": "Local (city/county) sales tax rate as a decimal.",
                "default": 0.0,
            },
        },
        "required": ["purchase_amount", "state_rate"],
    },
}


def sales_tax_calculator(
    purchase_amount: float,
    state_rate: float,
    local_rate: float = 0.0,
) -> dict[str, Any]:
    """Calculate sales tax."""
    try:
        if purchase_amount < 0:
            return {
                "status": "error",
                "data": {"error": "purchase_amount must be non-negative."},
                "timestamp": datetime.now(timezone.utc).isoformat(),
            }
        if state_rate < 0 or local_rate < 0:
            return {
                "status": "error",
                "data": {"error": "Tax rates must be non-negative."},
                "timestamp": datetime.now(timezone.utc).isoformat(),
            }

        combined_rate = state_rate + local_rate
        state_tax = purchase_amount * state_rate
        local_tax = purchase_amount * local_rate
        total_tax = state_tax + local_tax
        total_cost = purchase_amount + total_tax

        return {
            "status": "ok",
            "data": {
                "purchase_amount": round(purchase_amount, 2),
                "state_rate_pct": round(state_rate * 100, 3),
                "local_rate_pct": round(local_rate * 100, 3),
                "combined_rate_pct": round(combined_rate * 100, 3),
                "state_tax": round(state_tax, 2),
                "local_tax": round(local_tax, 2),
                "total_tax": round(total_tax, 2),
                "total_cost": round(total_cost, 2),
            },
            "timestamp": datetime.now(timezone.utc).isoformat(),
        }
    except Exception as exc:
        return {
            "status": "error",
            "data": {"error": str(exc)},
            "timestamp": datetime.now(timezone.utc).isoformat(),
        }
