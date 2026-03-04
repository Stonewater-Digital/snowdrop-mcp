"""Allocate a portfolio equally across N assets.

MCP Tool Name: equal_weight_allocator
"""
from __future__ import annotations

from datetime import datetime, timezone
from typing import Any

TOOL_META: dict[str, Any] = {
    "name": "equal_weight_allocator",
    "description": (
        "Allocates a total portfolio value equally across a specified number of "
        "assets, returning weight and dollar allocation per asset."
    ),
    "inputSchema": {
        "type": "object",
        "properties": {
            "num_assets": {
                "type": "integer",
                "description": "Number of assets to allocate across (must be > 0).",
            },
            "total_value": {
                "type": "number",
                "description": "Total portfolio value to allocate (default 10000).",
            },
        },
        "required": ["num_assets"],
    },
}


def equal_weight_allocator(
    num_assets: int, total_value: float = 10000.0
) -> dict[str, Any]:
    """Allocate portfolio equally across N assets."""
    try:
        num_assets = int(num_assets)
        total_value = float(total_value)

        if num_assets <= 0:
            raise ValueError("num_assets must be greater than zero.")

        weight = 1.0 / num_assets
        allocation = total_value / num_assets

        allocations = [
            {
                "asset": i + 1,
                "weight": round(weight, 6),
                "value": round(allocation, 2),
            }
            for i in range(num_assets)
        ]

        return {
            "status": "ok",
            "data": {
                "num_assets": num_assets,
                "weight_per_asset": round(weight, 6),
                "value_per_asset": round(allocation, 2),
                "total_value": total_value,
                "allocations": allocations,
            },
            "timestamp": datetime.now(timezone.utc).isoformat(),
        }
    except Exception as exc:
        return {
            "status": "error",
            "data": {"error": str(exc)},
            "timestamp": datetime.now(timezone.utc).isoformat(),
        }
