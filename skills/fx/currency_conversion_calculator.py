"""Convert an amount between currencies using exchange rates.

MCP Tool Name: currency_conversion_calculator
"""
from __future__ import annotations
from datetime import datetime, timezone
from typing import Any

TOOL_META: dict[str, Any] = {
    "name": "currency_conversion_calculator",
    "description": "Convert an amount between two currencies given their USD exchange rates. converted = amount * to_rate / from_rate.",
    "inputSchema": {
        "type": "object",
        "properties": {
            "amount": {
                "type": "number",
                "description": "Amount to convert.",
            },
            "from_rate": {
                "type": "number",
                "description": "Exchange rate of source currency per USD (e.g. 1.0 for USD, 0.92 for EUR).",
                "default": 1.0,
            },
            "to_rate": {
                "type": "number",
                "description": "Exchange rate of target currency per USD.",
                "default": 1.0,
            },
        },
        "required": ["amount"],
    },
}


def currency_conversion_calculator(
    amount: float,
    from_rate: float = 1.0,
    to_rate: float = 1.0,
) -> dict[str, Any]:
    """Convert between currencies using exchange rates."""
    try:
        if from_rate <= 0 or to_rate <= 0:
            return {
                "status": "error",
                "data": {"error": "Exchange rates must be positive."},
                "timestamp": datetime.now(timezone.utc).isoformat(),
            }

        converted = amount * to_rate / from_rate
        effective_rate = to_rate / from_rate

        return {
            "status": "ok",
            "data": {
                "original_amount": round(amount, 6),
                "from_rate_per_usd": from_rate,
                "to_rate_per_usd": to_rate,
                "effective_rate": round(effective_rate, 6),
                "converted_amount": round(converted, 6),
            },
            "timestamp": datetime.now(timezone.utc).isoformat(),
        }
    except Exception as exc:
        return {
            "status": "error",
            "data": {"error": str(exc)},
            "timestamp": datetime.now(timezone.utc).isoformat(),
        }
