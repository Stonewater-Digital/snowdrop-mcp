"""Allocate a budget across categories using the envelope method.

MCP Tool Name: envelope_budget_allocator
"""
from __future__ import annotations
from datetime import datetime, timezone
from typing import Any

TOOL_META: dict[str, Any] = {
    "name": "envelope_budget_allocator",
    "description": "Allocates a total budget across categories by percentage using the envelope budgeting method. Validates percentages sum to 100.",
    "inputSchema": {
        "type": "object",
        "properties": {
            "total_budget": {
                "type": "number",
                "description": "Total monthly budget to allocate in dollars.",
            },
            "categories": {
                "type": "array",
                "description": "List of categories with name and percentage allocation.",
                "items": {
                    "type": "object",
                    "properties": {
                        "name": {"type": "string"},
                        "percentage": {"type": "number", "description": "Percentage of total budget (e.g., 25 for 25%)."},
                    },
                    "required": ["name", "percentage"],
                },
            },
        },
        "required": ["total_budget", "categories"],
    },
}


def envelope_budget_allocator(
    total_budget: float, categories: list[dict[str, Any]]
) -> dict[str, Any]:
    """Allocates budget across categories by percentage."""
    try:
        if total_budget <= 0:
            return {
                "status": "error",
                "data": {"error": "Total budget must be a positive number."},
                "timestamp": datetime.now(timezone.utc).isoformat(),
            }
        if not categories:
            return {
                "status": "error",
                "data": {"error": "At least one category is required."},
                "timestamp": datetime.now(timezone.utc).isoformat(),
            }

        total_pct = sum(c["percentage"] for c in categories)
        pct_valid = abs(total_pct - 100) < 0.01

        envelopes = []
        for c in categories:
            amount = round(total_budget * (c["percentage"] / 100), 2)
            envelopes.append({
                "name": c["name"],
                "percentage": c["percentage"],
                "allocated_amount": amount,
                "weekly_amount": round(amount / 4.33, 2),
            })

        envelopes.sort(key=lambda x: x["allocated_amount"], reverse=True)
        total_allocated = sum(e["allocated_amount"] for e in envelopes)

        return {
            "status": "ok",
            "data": {
                "total_budget": total_budget,
                "total_percentage": round(total_pct, 2),
                "percentages_valid": pct_valid,
                "total_allocated": round(total_allocated, 2),
                "unallocated": round(total_budget - total_allocated, 2),
                "envelopes": envelopes,
                "num_categories": len(envelopes),
                "warning": None if pct_valid else f"Percentages sum to {round(total_pct, 2)}%, not 100%. Adjust categories.",
            },
            "timestamp": datetime.now(timezone.utc).isoformat(),
        }
    except Exception as exc:
        return {
            "status": "error",
            "data": {"error": str(exc)},
            "timestamp": datetime.now(timezone.utc).isoformat(),
        }
