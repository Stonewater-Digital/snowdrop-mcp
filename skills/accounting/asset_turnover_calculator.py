"""Calculate asset turnover ratio measuring revenue efficiency from total assets.

MCP Tool Name: asset_turnover_calculator
"""
from __future__ import annotations

from datetime import datetime, timezone
from typing import Any

TOOL_META: dict[str, Any] = {
    "name": "asset_turnover_calculator",
    "description": (
        "Calculates the asset turnover ratio, measuring how efficiently a company "
        "generates revenue from its total assets."
    ),
    "inputSchema": {
        "type": "object",
        "properties": {
            "net_sales": {
                "type": "number",
                "description": "Net sales (revenue) for the period.",
            },
            "avg_total_assets": {
                "type": "number",
                "description": "Average total assets for the period.",
            },
        },
        "required": ["net_sales", "avg_total_assets"],
    },
}


def asset_turnover_calculator(
    net_sales: float, avg_total_assets: float
) -> dict[str, Any]:
    """Calculate asset turnover ratio."""
    try:
        net_sales = float(net_sales)
        avg_total_assets = float(avg_total_assets)

        if avg_total_assets == 0:
            raise ValueError("avg_total_assets must not be zero.")

        turnover = net_sales / avg_total_assets

        return {
            "status": "ok",
            "data": {
                "asset_turnover_ratio": round(turnover, 4),
            },
            "timestamp": datetime.now(timezone.utc).isoformat(),
        }
    except Exception as exc:
        return {
            "status": "error",
            "data": {"error": str(exc)},
            "timestamp": datetime.now(timezone.utc).isoformat(),
        }
