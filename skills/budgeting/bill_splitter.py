"""Split a bill evenly among a group with tip calculation.

MCP Tool Name: bill_splitter
"""
from __future__ import annotations
from datetime import datetime, timezone
from typing import Any

TOOL_META: dict[str, Any] = {
    "name": "bill_splitter",
    "description": "Splits a total bill amount evenly among a group of people, including tip calculation.",
    "inputSchema": {
        "type": "object",
        "properties": {
            "total_amount": {
                "type": "number",
                "description": "Total bill amount before tip in dollars.",
            },
            "num_people": {
                "type": "integer",
                "description": "Number of people splitting the bill.",
            },
            "tip_pct": {
                "type": "number",
                "description": "Tip percentage (default: 18).",
            },
        },
        "required": ["total_amount", "num_people"],
    },
}


def bill_splitter(
    total_amount: float, num_people: int, tip_pct: float = 18.0
) -> dict[str, Any]:
    """Splits a bill among people with tip."""
    try:
        if total_amount <= 0:
            return {
                "status": "error",
                "data": {"error": "Total amount must be a positive number."},
                "timestamp": datetime.now(timezone.utc).isoformat(),
            }
        if num_people <= 0:
            return {
                "status": "error",
                "data": {"error": "Number of people must be at least 1."},
                "timestamp": datetime.now(timezone.utc).isoformat(),
            }

        tip_amount = round(total_amount * (tip_pct / 100), 2)
        total_with_tip = round(total_amount + tip_amount, 2)
        per_person = round(total_with_tip / num_people, 2)
        tip_per_person = round(tip_amount / num_people, 2)

        return {
            "status": "ok",
            "data": {
                "subtotal": total_amount,
                "tip_percentage": tip_pct,
                "tip_amount": tip_amount,
                "total_with_tip": total_with_tip,
                "num_people": num_people,
                "per_person_total": per_person,
                "per_person_tip": tip_per_person,
                "per_person_subtotal": round(total_amount / num_people, 2),
            },
            "timestamp": datetime.now(timezone.utc).isoformat(),
        }
    except Exception as exc:
        return {
            "status": "error",
            "data": {"error": str(exc)},
            "timestamp": datetime.now(timezone.utc).isoformat(),
        }
