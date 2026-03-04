"""Calculate sum-of-the-years-digits depreciation.

MCP Tool Name: depreciation_sum_of_years_calculator
"""
from __future__ import annotations

from datetime import datetime, timezone
from typing import Any

TOOL_META: dict[str, Any] = {
    "name": "depreciation_sum_of_years_calculator",
    "description": (
        "Calculates depreciation using the sum-of-the-years-digits method, returning "
        "a year-by-year schedule with declining depreciation amounts."
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
        },
        "required": ["cost", "salvage_value", "useful_life"],
    },
}


def depreciation_sum_of_years_calculator(
    cost: float, salvage_value: float, useful_life: int
) -> dict[str, Any]:
    """Calculate sum-of-the-years-digits depreciation."""
    try:
        cost = float(cost)
        salvage_value = float(salvage_value)
        useful_life = int(useful_life)

        if useful_life <= 0:
            raise ValueError("useful_life must be greater than zero.")

        syd = useful_life * (useful_life + 1) / 2
        depreciable_base = cost - salvage_value
        book_value = cost
        accumulated = 0.0
        schedule = []

        for year in range(1, useful_life + 1):
            fraction = (useful_life - year + 1) / syd
            depreciation = depreciable_base * fraction
            book_value -= depreciation
            accumulated += depreciation
            schedule.append({
                "year": year,
                "depreciation_expense": round(depreciation, 2),
                "fraction": round(fraction, 6),
                "accumulated_depreciation": round(accumulated, 2),
                "book_value": round(book_value, 2),
            })

        return {
            "status": "ok",
            "data": {
                "sum_of_years_digits": int(syd),
                "depreciable_base": round(depreciable_base, 2),
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
