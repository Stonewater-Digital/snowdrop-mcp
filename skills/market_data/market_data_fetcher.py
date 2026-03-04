"""Fetch spot prices from CoinGecko."""
from __future__ import annotations

import os
from datetime import datetime, timezone
from typing import Any

import requests

TOOL_META: dict[str, Any] = {
    "name": "market_data_fetcher",
    "description": "Pulls CoinGecko quotes and 24h change metrics.",
    "inputSchema": {
        "type": "object",
        "properties": {
            "assets": {
                "type": "array",
                "items": {"type": "string"},
            },
            "vs_currency": {"type": "string", "default": "usd"},
        },
        "required": ["assets"],
    },
    "outputSchema": {
        "type": "object",
        "properties": {
            "status": {"type": "string"},
            "data": {
                "type": "object",
                "properties": {
                    "quotes": {"type": "object"},
                },
            },
            "timestamp": {"type": "string"},
        },
    },
}


def market_data_fetcher(
    assets: list[str],
    vs_currency: str = "usd",
    **_: Any,
) -> dict[str, Any]:
    """Call CoinGecko Simple Price endpoint and return price snapshots."""

    try:
        if not assets:
            raise ValueError("assets must include at least one identifier")
        headers = {}
        api_key = os.getenv("COINGECKO_API_KEY")
        if api_key:
            headers["x-cg-pro-api-key"] = api_key

        endpoint = "https://api.coingecko.com/api/v3/simple/price"
        params = {
            "ids": ",".join(assets),
            "vs_currencies": vs_currency,
            "include_24hr_change": "true",
        }
        response = requests.get(endpoint, params=params, headers=headers, timeout=10)
        response.raise_for_status()
        payload = response.json()
        quotes: dict[str, dict[str, Any]] = {}
        for asset in assets:
            asset_payload = payload.get(asset.lower())
            if not asset_payload:
                continue
            quotes[asset] = {
                "price": asset_payload.get(vs_currency.lower()),
                "change_24h_pct": asset_payload.get(f"{vs_currency.lower()}_24h_change"),
                "source": "coingecko",
            }

        return {
            "status": "success",
            "data": {"quotes": quotes},
            "timestamp": datetime.now(timezone.utc).isoformat(),
        }
    except Exception as exc:
        _log_lesson("market_data_fetcher", str(exc))
        return {
            "status": "error",
            "data": {"error": str(exc)},
            "timestamp": datetime.now(timezone.utc).isoformat(),
        }


def _log_lesson(skill_name: str, error: str) -> None:
    """Append a Ralph Wiggum lesson entry."""

    with open("logs/lessons.md", "a", encoding="utf-8") as handle:
        handle.write(f"- [{datetime.now(timezone.utc).isoformat()}] {skill_name}: {error}\n")
