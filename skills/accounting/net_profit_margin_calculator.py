"""Calculate net profit margin as a percentage of revenue.

MCP Tool Name: net_profit_margin_calculator
"""
from __future__ import annotations

from datetime import datetime, timezone
from typing import Any

TOOL_META: dict[str, Any] = {
    "name": "net_profit_margin_calculator",
    "description": (
        "Calculates net profit margin as a percentage, measuring the proportion "
        "of revenue that becomes bottom-line profit."
    ),
    "inputSchema": {
        "type": "object",
        "properties": {
            "net_income": {
                "type": "number",
                "description": "Net income for the period.",
            },
            "revenue": {
                "type": "number",
                "description": "Total revenue.",
            },
        },
        "required": ["net_income", "revenue"],
    },
}


def net_profit_margin_calculator(
    net_income: float, revenue: float
) -> dict[str, Any]:
    """Calculate net profit margin."""
    try:
        net_income = float(net_income)
        revenue = float(revenue)

        if revenue == 0:
            raise ValueError("revenue must not be zero.")

        margin = (net_income / revenue) * 100

        return {
            "status": "ok",
            "data": {
                "net_profit_margin_pct": round(margin, 4),
            },
            "timestamp": datetime.now(timezone.utc).isoformat(),
        }
    except Exception as exc:
        return {
            "status": "error",
            "data": {"error": str(exc)},
            "timestamp": datetime.now(timezone.utc).isoformat(),
        }
