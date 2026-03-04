"""Calculate the quick (acid-test) ratio excluding inventory from current assets.

MCP Tool Name: quick_ratio_calculator
"""
from __future__ import annotations

from datetime import datetime, timezone
from typing import Any

TOOL_META: dict[str, Any] = {
    "name": "quick_ratio_calculator",
    "description": (
        "Calculates the quick ratio (acid-test ratio) by excluding inventory from "
        "current assets, providing a stricter measure of short-term liquidity."
    ),
    "inputSchema": {
        "type": "object",
        "properties": {
            "current_assets": {
                "type": "number",
                "description": "Total current assets.",
            },
            "inventory": {
                "type": "number",
                "description": "Inventory value to exclude from current assets.",
            },
            "current_liabilities": {
                "type": "number",
                "description": "Total current liabilities.",
            },
        },
        "required": ["current_assets", "inventory", "current_liabilities"],
    },
}


def quick_ratio_calculator(
    current_assets: float, inventory: float, current_liabilities: float
) -> dict[str, Any]:
    """Calculate the quick (acid-test) ratio."""
    try:
        current_assets = float(current_assets)
        inventory = float(inventory)
        current_liabilities = float(current_liabilities)

        if current_liabilities == 0:
            raise ValueError("current_liabilities must not be zero.")

        quick_assets = current_assets - inventory
        ratio = quick_assets / current_liabilities

        return {
            "status": "ok",
            "data": {
                "quick_ratio": round(ratio, 4),
                "quick_assets": round(quick_assets, 2),
            },
            "timestamp": datetime.now(timezone.utc).isoformat(),
        }
    except Exception as exc:
        return {
            "status": "error",
            "data": {"error": str(exc)},
            "timestamp": datetime.now(timezone.utc).isoformat(),
        }
