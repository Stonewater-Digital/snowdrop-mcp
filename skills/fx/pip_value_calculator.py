"""Calculate pip value for a forex position.

MCP Tool Name: pip_value_calculator
"""
from __future__ import annotations
from datetime import datetime, timezone
from typing import Any

TOOL_META: dict[str, Any] = {
    "name": "pip_value_calculator",
    "description": "Calculate the monetary value of a single pip for a given currency pair and lot size. Handles JPY pairs (pip = 0.01) and standard pairs (pip = 0.0001).",
    "inputSchema": {
        "type": "object",
        "properties": {
            "pair": {
                "type": "string",
                "description": "Currency pair (e.g. 'EUR/USD', 'USD/JPY').",
            },
            "lot_size": {
                "type": "number",
                "description": "Position size in units of base currency.",
                "default": 100000,
            },
            "account_currency": {
                "type": "string",
                "description": "Account denomination currency.",
                "default": "USD",
            },
            "exchange_rate": {
                "type": "number",
                "description": "Current exchange rate of the pair (quote currency per base currency). Used to convert pip value to account currency if needed.",
                "default": 1.0,
            },
        },
        "required": ["pair"],
    },
}

_JPY_PAIRS = {"JPY"}


def pip_value_calculator(
    pair: str,
    lot_size: float = 100000,
    account_currency: str = "USD",
    exchange_rate: float = 1.0,
) -> dict[str, Any]:
    """Calculate pip value for a forex position."""
    try:
        pair = pair.upper().strip().replace(" ", "")
        # Normalize separators
        if "/" in pair:
            base, quote = pair.split("/")
        elif len(pair) == 6:
            base, quote = pair[:3], pair[3:]
        else:
            return {
                "status": "error",
                "data": {"error": f"Cannot parse pair '{pair}'. Use format 'EUR/USD' or 'EURUSD'."},
                "timestamp": datetime.now(timezone.utc).isoformat(),
            }

        is_jpy = quote in _JPY_PAIRS or base in _JPY_PAIRS
        pip_size = 0.01 if is_jpy else 0.0001

        # Pip value in quote currency
        pip_value_quote = pip_size * lot_size

        # Convert to account currency
        account_currency = account_currency.upper().strip()
        if account_currency == quote:
            pip_value_account = pip_value_quote
        elif account_currency == base:
            pip_value_account = pip_value_quote / exchange_rate if exchange_rate != 0 else 0
        else:
            # If account currency is neither base nor quote, use exchange_rate as conversion
            pip_value_account = pip_value_quote / exchange_rate if exchange_rate != 0 else 0

        return {
            "status": "ok",
            "data": {
                "pair": f"{base}/{quote}",
                "lot_size": lot_size,
                "pip_size": pip_size,
                "pip_value_quote_currency": round(pip_value_quote, 4),
                "pip_value_account_currency": round(pip_value_account, 4),
                "account_currency": account_currency,
                "exchange_rate_used": exchange_rate,
            },
            "timestamp": datetime.now(timezone.utc).isoformat(),
        }
    except Exception as exc:
        return {
            "status": "error",
            "data": {"error": str(exc)},
            "timestamp": datetime.now(timezone.utc).isoformat(),
        }
