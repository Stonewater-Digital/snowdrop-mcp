"""Calculate return on invested capital (ROIC) as a percentage.

MCP Tool Name: return_on_invested_capital_calculator
"""
from __future__ import annotations

from datetime import datetime, timezone
from typing import Any

TOOL_META: dict[str, Any] = {
    "name": "return_on_invested_capital_calculator",
    "description": (
        "Calculates return on invested capital (ROIC), measuring how effectively a "
        "company generates returns on capital invested by shareholders and debtholders."
    ),
    "inputSchema": {
        "type": "object",
        "properties": {
            "net_income": {
                "type": "number",
                "description": "Net income for the period.",
            },
            "dividends": {
                "type": "number",
                "description": "Dividends paid during the period.",
            },
            "total_capital": {
                "type": "number",
                "description": "Total invested capital (debt + equity).",
            },
        },
        "required": ["net_income", "dividends", "total_capital"],
    },
}


def return_on_invested_capital_calculator(
    net_income: float, dividends: float, total_capital: float
) -> dict[str, Any]:
    """Calculate return on invested capital."""
    try:
        net_income = float(net_income)
        dividends = float(dividends)
        total_capital = float(total_capital)

        if total_capital == 0:
            raise ValueError("total_capital must not be zero.")

        roic = ((net_income - dividends) / total_capital) * 100

        return {
            "status": "ok",
            "data": {
                "roic_pct": round(roic, 4),
            },
            "timestamp": datetime.now(timezone.utc).isoformat(),
        }
    except Exception as exc:
        return {
            "status": "error",
            "data": {"error": str(exc)},
            "timestamp": datetime.now(timezone.utc).isoformat(),
        }
