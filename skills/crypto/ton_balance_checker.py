"""Check TON balances via TON Center API."""
from __future__ import annotations

import os
from datetime import datetime, timezone
from typing import Any

import requests

API_URL = "https://toncenter.com/api/v2/getAddressBalance"
NANO = 1_000_000_000

TOOL_META: dict[str, Any] = {
    "name": "ton_balance_checker",
    "description": "Queries TON Center for the configured wallet and returns TON balances.",
    "inputSchema": {"type": "object", "properties": {}},
    "outputSchema": {
        "type": "object",
        "properties": {
            "status": {"type": "string"},
            "data": {
                "type": "object",
                "properties": {
                    "address": {"type": "string"},
                    "balance_ton": {"type": "number"},
                },
            },
            "timestamp": {"type": "string"},
        },
    },
}


def ton_balance_checker(**_: Any) -> dict[str, Any]:
    """Fetch TON balance for the configured wallet."""
    try:
        address = os.getenv("TON_WALLET_ADDRESS")
        api_key = os.getenv("TON_API_KEY")
        if not address or not api_key:
            raise ValueError("TON_WALLET_ADDRESS and TON_API_KEY required (.env.template)")

        params = {"address": address}
        headers = {"X-API-Key": api_key}
        response = requests.get(API_URL, params=params, headers=headers, timeout=15)
        response.raise_for_status()
        payload = response.json()
        balance_nano = int(payload.get("result", 0))
        balance_ton = balance_nano / NANO
        data = {
            "address": address,
            "balance_ton": round(balance_ton, 4),
        }
        return {
            "status": "success",
            "data": data,
            "timestamp": datetime.now(timezone.utc).isoformat(),
        }
    except Exception as exc:
        _log_lesson("ton_balance_checker", str(exc))
        return {
            "status": "error",
            "data": {"error": str(exc)},
            "timestamp": datetime.now(timezone.utc).isoformat(),
        }


def _log_lesson(skill_name: str, error: str) -> None:
    with open("logs/lessons.md", "a", encoding="utf-8") as handle:
        handle.write(f"- [{datetime.now(timezone.utc).isoformat()}] {skill_name}: {error}\n")
