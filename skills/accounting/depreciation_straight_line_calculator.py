"""Calculate straight-line depreciation over the useful life of an asset.

MCP Tool Name: depreciation_straight_line_calculator
"""
from __future__ import annotations

from datetime import datetime, timezone
from typing import Any

TOOL_META: dict[str, Any] = {
    "name": "depreciation_straight_line_calculator",
    "description": (
        "Calculates annual depreciation expense using the straight-line method, "
        "returning per-year depreciation and a full schedule."
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


def depreciation_straight_line_calculator(
    cost: float, salvage_value: float, useful_life: int
) -> dict[str, Any]:
    """Calculate straight-line depreciation."""
    try:
        cost = float(cost)
        salvage_value = float(salvage_value)
        useful_life = int(useful_life)

        if useful_life <= 0:
            raise ValueError("useful_life must be greater than zero.")
        depreciable_base = cost - salvage_value
        annual_depreciation = depreciable_base / useful_life

        schedule = []
        book_value = cost
        for year in range(1, useful_life + 1):
            book_value -= annual_depreciation
            schedule.append({
                "year": year,
                "depreciation_expense": round(annual_depreciation, 2),
                "accumulated_depreciation": round(annual_depreciation * year, 2),
                "book_value": round(book_value, 2),
            })

        return {
            "status": "ok",
            "data": {
                "annual_depreciation": round(annual_depreciation, 2),
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
