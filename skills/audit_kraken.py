"""
Executive Summary: Retrieves live Kraken exchange balances for TON, SOL, and USDC and returns USD-denominated values.

Inputs: None (reads KRAKEN_API_KEY and KRAKEN_SECRET from environment)
Outputs: dict with balances list (asset, balance, usd_value) and total_usd float
MCP Tool Name: audit_kraken
"""
import os
import logging
from typing import Any
from datetime import datetime, timezone

import ccxt

logger = logging.getLogger("snowdrop.skills")

# --- MCP Tool Metadata ---
TOOL_META = {
    "name": "audit_kraken",
    "description": "Retrieves live Kraken exchange balances for TON, SOL, and USDC, converts to USD, and returns a structured balance report.",
    "inputSchema": {
        "type": "object",
        "properties": {},
        "required": []
    },
    "outputSchema": {
        "type": "object",
        "properties": {
            "status": {"type": "string"},
            "data": {
                "type": "object",
                "properties": {
                    "balances": {
                        "type": "array",
                        "items": {
                            "type": "object",
                            "properties": {
                                "asset": {"type": "string"},
                                "balance": {"type": "number"},
                                "usd_value": {"type": "number"}
                            }
                        }
                    },
                    "total_usd": {"type": "number"}
                }
            },
            "timestamp": {"type": "string"}
        },
        "required": ["status", "timestamp"]
    }
}

# Assets to track and their Kraken trading pairs for USD pricing
TRACKED_ASSETS: dict[str, str] = {
    "TON": "TON/USD",
    "SOL": "SOL/USD",
    "USDC": "USDC/USD",
}


def audit_kraken(**kwargs: Any) -> dict:
    """Fetch live Kraken balances for TON, SOL, and USDC and compute USD values.

    Connects to the Kraken exchange via ccxt using API credentials from environment
    variables. Retrieves free (available) balances for the tracked assets and fetches
    the latest ticker price for each to compute a USD-denominated value.

    Args:
        **kwargs: Unused. Accepted for MCP dispatch compatibility.

    Returns:
        dict: A result dict with the following shape on success::

            {
                "status": "success",
                "data": {
                    "balances": [
                        {"asset": "TON", "balance": 10.5, "usd_value": 63.00},
                        ...
                    ],
                    "total_usd": 63.00
                },
                "timestamp": "2026-02-19T00:00:00+00:00"
            }

        On error::

            {
                "status": "error",
                "error": "<error message>",
                "timestamp": "2026-02-19T00:00:00+00:00"
            }
    """
    try:
        api_key = os.getenv("KRAKEN_API_KEY")
        secret = os.getenv("KRAKEN_SECRET")

        if not api_key or not secret:
            raise ValueError("KRAKEN_API_KEY and KRAKEN_SECRET must be set in environment")

        exchange = ccxt.kraken({
            "apiKey": api_key,
            "secret": secret,
        })

        raw_balance = exchange.fetch_balance()
        free_balances: dict[str, float] = raw_balance.get("free", {})

        balances: list[dict[str, Any]] = []
        total_usd: float = 0.0

        for asset, ticker_pair in TRACKED_ASSETS.items():
            balance: float = float(free_balances.get(asset, 0.0))

            if asset == "USDC":
                # USDC is pegged 1:1 to USD; avoid unnecessary ticker call
                usd_price: float = 1.0
            else:
                ticker = exchange.fetch_ticker(ticker_pair)
                usd_price = float(ticker.get("last", 0.0))

            usd_value: float = balance * usd_price
            total_usd += usd_value

            balances.append({
                "asset": asset,
                "balance": balance,
                "usd_value": round(usd_value, 2),
            })

        result: dict[str, Any] = {
            "balances": balances,
            "total_usd": round(total_usd, 2),
        }

        logger.info(f"audit_kraken: fetched {len(balances)} asset balances, total_usd={total_usd:.2f}")
        return {
            "status": "success",
            "data": result,
            "timestamp": datetime.now(timezone.utc).isoformat(),
        }

    except Exception as e:
        logger.error(f"audit_kraken failed: {e}")
        _log_lesson(f"audit_kraken: {e}")
        return {
            "status": "error",
            "error": str(e),
            "timestamp": datetime.now(timezone.utc).isoformat(),
        }


def _log_lesson(message: str) -> None:
    """Append a timestamped error lesson to logs/lessons.md.

    Args:
        message: Human-readable description of what went wrong.
    """
    with open("logs/lessons.md", "a") as f:
        f.write(f"- [{datetime.now(timezone.utc).isoformat()}] {message}\n")
