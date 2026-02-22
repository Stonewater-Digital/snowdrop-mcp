"""Aggregate TON/SOL/USD price feeds from multiple venues."""
from __future__ import annotations

from statistics import median
from datetime import datetime, timezone
from typing import Any

import ccxt
import requests

COINGECKO_URL = "https://api.coingecko.com/api/v3/simple/price"
ASSET_MAP = {
    "ton": {"coingecko_id": "toncoin", "kraken_pair": "TON/USD"},
    "sol": {"coingecko_id": "solana", "kraken_pair": "SOL/USD"},
    "usdc": {"coingecko_id": "usd-coin", "kraken_pair": "USDC/USD"},
}

TOOL_META: dict[str, Any] = {
    "name": "price_feed_aggregator",
    "description": "Fetches CoinGecko and Kraken prices then returns the median.",
    "inputSchema": {
        "type": "object",
        "properties": {
            "asset_symbol": {"type": "string", "description": "Asset ticker (TON/SOL/USDC)."},
        },
        "required": ["asset_symbol"],
    },
    "outputSchema": {
        "type": "object",
        "properties": {
            "status": {"type": "string"},
            "data": {
                "type": "object",
                "properties": {
                    "median_price": {"type": "number"},
                    "sources": {"type": "array"},
                },
            },
            "timestamp": {"type": "string"},
        },
    },
}


def price_feed_aggregator(asset_symbol: str, **_: Any) -> dict[str, Any]:
    """Compute median USD price for the requested asset."""
    try:
        key = asset_symbol.lower()
        if key not in ASSET_MAP:
            raise ValueError(f"Unsupported asset_symbol '{asset_symbol}'")
        mapping = ASSET_MAP[key]
        prices = []
        sources = []

        # CoinGecko
        params = {"ids": mapping["coingecko_id"], "vs_currencies": "usd"}
        cg_resp = requests.get(COINGECKO_URL, params=params, timeout=10)
        if cg_resp.ok:
            value = cg_resp.json().get(mapping["coingecko_id"], {}).get("usd")
            if value:
                prices.append(float(value))
                sources.append({"source": "coingecko", "price": float(value)})

        # Kraken
        exchange = ccxt.kraken()
        ticker = exchange.fetch_ticker(mapping["kraken_pair"])
        kraken_price = float(ticker.get("last"))
        prices.append(kraken_price)
        sources.append({"source": "kraken", "price": kraken_price})

        if not prices:
            raise RuntimeError("No price sources succeeded")

        data = {
            "asset_symbol": asset_symbol.upper(),
            "median_price": round(median(prices), 6),
            "sources": sources,
        }
        return {
            "status": "success",
            "data": data,
            "timestamp": datetime.now(timezone.utc).isoformat(),
        }
    except Exception as exc:
        _log_lesson("price_feed_aggregator", str(exc))
        return {
            "status": "error",
            "data": {"error": str(exc)},
            "timestamp": datetime.now(timezone.utc).isoformat(),
        }


def _log_lesson(skill_name: str, error: str) -> None:
    with open("logs/lessons.md", "a", encoding="utf-8") as handle:
        handle.write(f"- [{datetime.now(timezone.utc).isoformat()}] {skill_name}: {error}\n")
