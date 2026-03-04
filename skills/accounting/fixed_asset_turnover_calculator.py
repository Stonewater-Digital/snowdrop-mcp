"""Calculate fixed asset turnover ratio measuring revenue per dollar of fixed assets.

MCP Tool Name: fixed_asset_turnover_calculator
"""
from __future__ import annotations

from datetime import datetime, timezone
from typing import Any

TOOL_META: dict[str, Any] = {
    "name": "fixed_asset_turnover_calculator",
    "description": (
        "Calculates the fixed asset turnover ratio, measuring how efficiently a company "
        "generates revenue from its net fixed assets (PP&E)."
    ),
    "inputSchema": {
        "type": "object",
        "properties": {
            "net_sales": {
                "type": "number",
                "description": "Net sales (revenue) for the period.",
            },
            "net_fixed_assets": {
                "type": "number",
                "description": "Net fixed assets (property, plant & equipment less depreciation).",
            },
        },
        "required": ["net_sales", "net_fixed_assets"],
    },
}


def fixed_asset_turnover_calculator(
    net_sales: float, net_fixed_assets: float
) -> dict[str, Any]:
    """Calculate fixed asset turnover ratio."""
    try:
        net_sales = float(net_sales)
        net_fixed_assets = float(net_fixed_assets)

        if net_fixed_assets == 0:
            raise ValueError("net_fixed_assets must not be zero.")

        turnover = net_sales / net_fixed_assets

        return {
            "status": "ok",
            "data": {
                "fixed_asset_turnover_ratio": round(turnover, 4),
            },
            "timestamp": datetime.now(timezone.utc).isoformat(),
        }
    except Exception as exc:
        return {
            "status": "error",
            "data": {"error": str(exc)},
            "timestamp": datetime.now(timezone.utc).isoformat(),
        }
