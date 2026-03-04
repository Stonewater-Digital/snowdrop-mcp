"""Calculate the debt-to-assets ratio measuring proportion of assets financed by debt.

MCP Tool Name: debt_to_assets_calculator
"""
from __future__ import annotations

from datetime import datetime, timezone
from typing import Any

TOOL_META: dict[str, Any] = {
    "name": "debt_to_assets_calculator",
    "description": (
        "Calculates the debt-to-assets ratio, showing the proportion of total "
        "assets financed through debt."
    ),
    "inputSchema": {
        "type": "object",
        "properties": {
            "total_debt": {
                "type": "number",
                "description": "Total debt (short-term + long-term).",
            },
            "total_assets": {
                "type": "number",
                "description": "Total assets.",
            },
        },
        "required": ["total_debt", "total_assets"],
    },
}


def debt_to_assets_calculator(
    total_debt: float, total_assets: float
) -> dict[str, Any]:
    """Calculate the debt-to-assets ratio."""
    try:
        total_debt = float(total_debt)
        total_assets = float(total_assets)

        if total_assets == 0:
            raise ValueError("total_assets must not be zero.")

        ratio = total_debt / total_assets

        return {
            "status": "ok",
            "data": {
                "debt_to_assets_ratio": round(ratio, 4),
                "debt_to_assets_pct": round(ratio * 100, 2),
            },
            "timestamp": datetime.now(timezone.utc).isoformat(),
        }
    except Exception as exc:
        return {
            "status": "error",
            "data": {"error": str(exc)},
            "timestamp": datetime.now(timezone.utc).isoformat(),
        }
