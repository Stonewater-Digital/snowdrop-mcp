"""Calculate dividend yield as a percentage of stock price.

MCP Tool Name: dividend_yield_calculator
"""
from __future__ import annotations

from datetime import datetime, timezone
from typing import Any

TOOL_META: dict[str, Any] = {
    "name": "dividend_yield_calculator",
    "description": (
        "Calculates the dividend yield as a percentage of the current stock price."
    ),
    "inputSchema": {
        "type": "object",
        "properties": {
            "annual_dividend": {
                "type": "number",
                "description": "Total annual dividend per share.",
            },
            "stock_price": {
                "type": "number",
                "description": "Current stock price per share.",
            },
        },
        "required": ["annual_dividend", "stock_price"],
    },
}


def dividend_yield_calculator(
    annual_dividend: float, stock_price: float
) -> dict[str, Any]:
    """Calculate dividend yield."""
    try:
        annual_dividend = float(annual_dividend)
        stock_price = float(stock_price)

        if stock_price == 0:
            raise ValueError("stock_price must not be zero.")

        dividend_yield = (annual_dividend / stock_price) * 100

        return {
            "status": "ok",
            "data": {
                "dividend_yield_pct": round(dividend_yield, 4),
            },
            "timestamp": datetime.now(timezone.utc).isoformat(),
        }
    except Exception as exc:
        return {
            "status": "error",
            "data": {"error": str(exc)},
            "timestamp": datetime.now(timezone.utc).isoformat(),
        }
