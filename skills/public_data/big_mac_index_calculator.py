"""Calculate the Big Mac Index for currency valuation comparison.

MCP Tool Name: big_mac_index_calculator
"""
from __future__ import annotations
from datetime import datetime, timezone
from typing import Any

TOOL_META: dict[str, Any] = {
    "name": "big_mac_index_calculator",
    "description": "Calculate the Big Mac Index to assess whether a currency is over- or under-valued relative to the US dollar based on purchasing power parity.",
    "inputSchema": {
        "type": "object",
        "properties": {
            "local_price": {
                "type": "number",
                "description": "Price of a Big Mac in local currency.",
            },
            "local_currency": {
                "type": "string",
                "description": "ISO 4217 currency code (e.g., 'GBP', 'JPY', 'EUR').",
            },
            "usd_price": {
                "type": "number",
                "description": "Price of a Big Mac in USD.",
                "default": 5.69,
            },
            "exchange_rate": {
                "type": "number",
                "description": "Actual market exchange rate (local currency per 1 USD).",
            },
        },
        "required": ["local_price", "local_currency", "exchange_rate"],
    },
}


def big_mac_index_calculator(
    local_price: float,
    local_currency: str,
    exchange_rate: float,
    usd_price: float = 5.69,
) -> dict[str, Any]:
    """Calculate the Big Mac Index for currency valuation."""
    try:
        if usd_price == 0:
            return {
                "status": "error",
                "data": {"error": "USD Big Mac price cannot be zero."},
                "timestamp": datetime.now(timezone.utc).isoformat(),
            }
        if exchange_rate == 0:
            return {
                "status": "error",
                "data": {"error": "Exchange rate cannot be zero."},
                "timestamp": datetime.now(timezone.utc).isoformat(),
            }

        # Implied PPP exchange rate
        implied_rate = local_price / usd_price

        # Over/under valuation percentage
        valuation_pct = (implied_rate - exchange_rate) / exchange_rate * 100

        # Price in USD at market rate
        local_price_in_usd = local_price / exchange_rate

        if valuation_pct > 10:
            assessment = f"{local_currency} appears overvalued by {abs(valuation_pct):.1f}% against USD"
        elif valuation_pct < -10:
            assessment = f"{local_currency} appears undervalued by {abs(valuation_pct):.1f}% against USD"
        else:
            assessment = f"{local_currency} appears roughly fairly valued against USD (within 10% band)"

        return {
            "status": "ok",
            "data": {
                "local_price": local_price,
                "local_currency": local_currency.upper(),
                "usd_price": usd_price,
                "actual_exchange_rate": exchange_rate,
                "implied_ppp_rate": round(implied_rate, 4),
                "local_price_in_usd": round(local_price_in_usd, 2),
                "valuation_pct": round(valuation_pct, 2),
                "assessment": assessment,
                "note": "The Big Mac Index is an informal measure of purchasing power parity (PPP). "
                "It has limitations: local input costs, taxes, trade barriers, and market structures "
                "all affect local Big Mac prices beyond pure currency valuation.",
            },
            "timestamp": datetime.now(timezone.utc).isoformat(),
        }
    except Exception as exc:
        return {
            "status": "error",
            "data": {"error": str(exc)},
            "timestamp": datetime.now(timezone.utc).isoformat(),
        }
