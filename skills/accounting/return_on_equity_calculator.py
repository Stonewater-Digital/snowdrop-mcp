"""Calculate return on equity (ROE) as a percentage.

MCP Tool Name: return_on_equity_calculator
"""
from __future__ import annotations

from datetime import datetime, timezone
from typing import Any

TOOL_META: dict[str, Any] = {
    "name": "return_on_equity_calculator",
    "description": (
        "Calculates return on equity (ROE) as a percentage, measuring profitability "
        "relative to shareholders equity."
    ),
    "inputSchema": {
        "type": "object",
        "properties": {
            "net_income": {
                "type": "number",
                "description": "Net income for the period.",
            },
            "avg_shareholders_equity": {
                "type": "number",
                "description": "Average shareholders equity for the period.",
            },
        },
        "required": ["net_income", "avg_shareholders_equity"],
    },
}


def return_on_equity_calculator(
    net_income: float, avg_shareholders_equity: float
) -> dict[str, Any]:
    """Calculate return on equity."""
    try:
        net_income = float(net_income)
        avg_shareholders_equity = float(avg_shareholders_equity)

        if avg_shareholders_equity == 0:
            raise ValueError("avg_shareholders_equity must not be zero.")

        roe = (net_income / avg_shareholders_equity) * 100

        return {
            "status": "ok",
            "data": {
                "roe_pct": round(roe, 4),
            },
            "timestamp": datetime.now(timezone.utc).isoformat(),
        }
    except Exception as exc:
        return {
            "status": "error",
            "data": {"error": str(exc)},
            "timestamp": datetime.now(timezone.utc).isoformat(),
        }
