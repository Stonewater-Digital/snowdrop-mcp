"""Calculate gross profit margin as a percentage of revenue.

MCP Tool Name: gross_profit_margin_calculator
"""
from __future__ import annotations

from datetime import datetime, timezone
from typing import Any

TOOL_META: dict[str, Any] = {
    "name": "gross_profit_margin_calculator",
    "description": (
        "Calculates gross profit margin as a percentage, measuring the proportion "
        "of revenue retained after direct production costs."
    ),
    "inputSchema": {
        "type": "object",
        "properties": {
            "revenue": {
                "type": "number",
                "description": "Total revenue.",
            },
            "cogs": {
                "type": "number",
                "description": "Cost of goods sold.",
            },
        },
        "required": ["revenue", "cogs"],
    },
}


def gross_profit_margin_calculator(
    revenue: float, cogs: float
) -> dict[str, Any]:
    """Calculate gross profit margin."""
    try:
        revenue = float(revenue)
        cogs = float(cogs)

        if revenue == 0:
            raise ValueError("revenue must not be zero.")

        gross_profit = revenue - cogs
        margin = (gross_profit / revenue) * 100

        return {
            "status": "ok",
            "data": {
                "gross_profit": round(gross_profit, 2),
                "gross_profit_margin_pct": round(margin, 4),
            },
            "timestamp": datetime.now(timezone.utc).isoformat(),
        }
    except Exception as exc:
        return {
            "status": "error",
            "data": {"error": str(exc)},
            "timestamp": datetime.now(timezone.utc).isoformat(),
        }
