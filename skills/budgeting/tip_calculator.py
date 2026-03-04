"""Calculate tip amount and total bill with optional split.

MCP Tool Name: tip_calculator
"""
from __future__ import annotations
from datetime import datetime, timezone
from typing import Any

TOOL_META: dict[str, Any] = {
    "name": "tip_calculator",
    "description": "Calculates tip amount, total bill, and per-person cost with optional group split.",
    "inputSchema": {
        "type": "object",
        "properties": {
            "bill_amount": {
                "type": "number",
                "description": "Total bill amount before tip in dollars.",
            },
            "tip_percentage": {
                "type": "number",
                "description": "Tip percentage (default: 18).",
            },
            "num_people": {
                "type": "integer",
                "description": "Number of people splitting (default: 1).",
            },
        },
        "required": ["bill_amount"],
    },
}


def tip_calculator(
    bill_amount: float, tip_percentage: float = 18.0, num_people: int = 1
) -> dict[str, Any]:
    """Calculates tip and total with optional split."""
    try:
        if bill_amount <= 0:
            return {
                "status": "error",
                "data": {"error": "Bill amount must be a positive number."},
                "timestamp": datetime.now(timezone.utc).isoformat(),
            }
        if num_people <= 0:
            return {
                "status": "error",
                "data": {"error": "Number of people must be at least 1."},
                "timestamp": datetime.now(timezone.utc).isoformat(),
            }

        tip = round(bill_amount * (tip_percentage / 100), 2)
        total = round(bill_amount + tip, 2)
        per_person = round(total / num_people, 2)

        # Show range of common tip amounts
        tip_options = {}
        for pct in [15, 18, 20, 25]:
            t = round(bill_amount * (pct / 100), 2)
            tip_options[f"{pct}%"] = {
                "tip": t,
                "total": round(bill_amount + t, 2),
                "per_person": round((bill_amount + t) / num_people, 2),
            }

        return {
            "status": "ok",
            "data": {
                "bill_amount": bill_amount,
                "tip_percentage": tip_percentage,
                "tip_amount": tip,
                "total": total,
                "num_people": num_people,
                "per_person": per_person,
                "tip_options": tip_options,
            },
            "timestamp": datetime.now(timezone.utc).isoformat(),
        }
    except Exception as exc:
        return {
            "status": "error",
            "data": {"error": str(exc)},
            "timestamp": datetime.now(timezone.utc).isoformat(),
        }
