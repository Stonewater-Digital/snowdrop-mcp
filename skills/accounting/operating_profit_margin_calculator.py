"""Calculate operating profit margin as a percentage of revenue.

MCP Tool Name: operating_profit_margin_calculator
"""
from __future__ import annotations

from datetime import datetime, timezone
from typing import Any

TOOL_META: dict[str, Any] = {
    "name": "operating_profit_margin_calculator",
    "description": (
        "Calculates operating profit margin as a percentage, showing how much "
        "profit a company makes from operations before interest and taxes."
    ),
    "inputSchema": {
        "type": "object",
        "properties": {
            "operating_income": {
                "type": "number",
                "description": "Operating income (EBIT).",
            },
            "revenue": {
                "type": "number",
                "description": "Total revenue.",
            },
        },
        "required": ["operating_income", "revenue"],
    },
}


def operating_profit_margin_calculator(
    operating_income: float, revenue: float
) -> dict[str, Any]:
    """Calculate operating profit margin."""
    try:
        operating_income = float(operating_income)
        revenue = float(revenue)

        if revenue == 0:
            raise ValueError("revenue must not be zero.")

        margin = (operating_income / revenue) * 100

        return {
            "status": "ok",
            "data": {
                "operating_profit_margin_pct": round(margin, 4),
            },
            "timestamp": datetime.now(timezone.utc).isoformat(),
        }
    except Exception as exc:
        return {
            "status": "error",
            "data": {"error": str(exc)},
            "timestamp": datetime.now(timezone.utc).isoformat(),
        }
