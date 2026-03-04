"""Calculate declining-balance depreciation with configurable acceleration factor.

MCP Tool Name: depreciation_declining_balance_calculator
"""
from __future__ import annotations

from datetime import datetime, timezone
from typing import Any

TOOL_META: dict[str, Any] = {
    "name": "depreciation_declining_balance_calculator",
    "description": (
        "Calculates depreciation using the declining-balance method (default double "
        "declining). Returns a year-by-year schedule clamped to salvage value."
    ),
    "inputSchema": {
        "type": "object",
        "properties": {
            "cost": {
                "type": "number",
                "description": "Original cost of the asset.",
            },
            "salvage_value": {
                "type": "number",
                "description": "Estimated residual value at end of useful life.",
            },
            "useful_life": {
                "type": "integer",
                "description": "Useful life of the asset in years (must be > 0).",
            },
            "factor": {
                "type": "number",
                "description": "Acceleration factor (default 2.0 for double-declining).",
            },
        },
        "required": ["cost", "salvage_value", "useful_life"],
    },
}


def depreciation_declining_balance_calculator(
    cost: float, salvage_value: float, useful_life: int, factor: float = 2.0
) -> dict[str, Any]:
    """Calculate declining-balance depreciation."""
    try:
        cost = float(cost)
        salvage_value = float(salvage_value)
        useful_life = int(useful_life)
        factor = float(factor)

        if useful_life <= 0:
            raise ValueError("useful_life must be greater than zero.")
        if factor <= 0:
            raise ValueError("factor must be greater than zero.")

        rate = factor / useful_life
        book_value = cost
        accumulated = 0.0
        schedule = []

        for year in range(1, useful_life + 1):
            depreciation = book_value * rate
            # Clamp so book value does not drop below salvage
            if book_value - depreciation < salvage_value:
                depreciation = book_value - salvage_value
            if depreciation < 0:
                depreciation = 0.0
            book_value -= depreciation
            accumulated += depreciation
            schedule.append({
                "year": year,
                "depreciation_expense": round(depreciation, 2),
                "accumulated_depreciation": round(accumulated, 2),
                "book_value": round(book_value, 2),
            })

        return {
            "status": "ok",
            "data": {
                "rate": round(rate, 6),
                "schedule": schedule,
            },
            "timestamp": datetime.now(timezone.utc).isoformat(),
        }
    except Exception as exc:
        return {
            "status": "error",
            "data": {"error": str(exc)},
            "timestamp": datetime.now(timezone.utc).isoformat(),
        }
