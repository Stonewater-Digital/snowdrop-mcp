"""Calculate a cross rate from two USD-based exchange rates.

MCP Tool Name: cross_rate_calculator
"""
from __future__ import annotations
from datetime import datetime, timezone
from typing import Any

TOOL_META: dict[str, Any] = {
    "name": "cross_rate_calculator",
    "description": "Calculate a cross exchange rate from two USD-based rates. cross_rate = base_usd_rate / quote_usd_rate.",
    "inputSchema": {
        "type": "object",
        "properties": {
            "base_usd_rate": {
                "type": "number",
                "description": "USD rate for the base currency (e.g. EUR/USD = 1.08 means 1 EUR = 1.08 USD).",
            },
            "quote_usd_rate": {
                "type": "number",
                "description": "USD rate for the quote currency (e.g. GBP/USD = 1.27 means 1 GBP = 1.27 USD).",
            },
        },
        "required": ["base_usd_rate", "quote_usd_rate"],
    },
}


def cross_rate_calculator(
    base_usd_rate: float,
    quote_usd_rate: float,
) -> dict[str, Any]:
    """Calculate cross rate from two USD-based rates."""
    try:
        if quote_usd_rate <= 0 or base_usd_rate <= 0:
            return {
                "status": "error",
                "data": {"error": "Exchange rates must be positive."},
                "timestamp": datetime.now(timezone.utc).isoformat(),
            }

        cross_rate = base_usd_rate / quote_usd_rate
        inverse_rate = quote_usd_rate / base_usd_rate

        return {
            "status": "ok",
            "data": {
                "base_usd_rate": base_usd_rate,
                "quote_usd_rate": quote_usd_rate,
                "cross_rate": round(cross_rate, 6),
                "inverse_cross_rate": round(inverse_rate, 6),
            },
            "timestamp": datetime.now(timezone.utc).isoformat(),
        }
    except Exception as exc:
        return {
            "status": "error",
            "data": {"error": str(exc)},
            "timestamp": datetime.now(timezone.utc).isoformat(),
        }
