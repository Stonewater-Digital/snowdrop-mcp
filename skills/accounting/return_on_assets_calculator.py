"""Calculate return on assets (ROA) as a percentage.

MCP Tool Name: return_on_assets_calculator
"""
from __future__ import annotations

from datetime import datetime, timezone
from typing import Any

TOOL_META: dict[str, Any] = {
    "name": "return_on_assets_calculator",
    "description": (
        "Calculates return on assets (ROA) as a percentage, measuring how "
        "efficiently a company uses its assets to generate profit."
    ),
    "inputSchema": {
        "type": "object",
        "properties": {
            "net_income": {
                "type": "number",
                "description": "Net income for the period.",
            },
            "avg_total_assets": {
                "type": "number",
                "description": "Average total assets for the period.",
            },
        },
        "required": ["net_income", "avg_total_assets"],
    },
}


def return_on_assets_calculator(
    net_income: float, avg_total_assets: float
) -> dict[str, Any]:
    """Calculate return on assets."""
    try:
        net_income = float(net_income)
        avg_total_assets = float(avg_total_assets)

        if avg_total_assets == 0:
            raise ValueError("avg_total_assets must not be zero.")

        roa = (net_income / avg_total_assets) * 100

        return {
            "status": "ok",
            "data": {
                "roa_pct": round(roa, 4),
            },
            "timestamp": datetime.now(timezone.utc).isoformat(),
        }
    except Exception as exc:
        return {
            "status": "error",
            "data": {"error": str(exc)},
            "timestamp": datetime.now(timezone.utc).isoformat(),
        }
