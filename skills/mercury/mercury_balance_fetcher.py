"""Fetch Mercury cash balances."""
from __future__ import annotations

import os
from datetime import datetime, timezone
from typing import Any

import requests

API_BASE = "https://api.mercury.com/api/v1"

TOOL_META: dict[str, Any] = {
    "name": "mercury_balance_fetcher",
    "description": "Retrieves account balances from Mercury's /api/v1/accounts endpoint.",
    "inputSchema": {
        "type": "object",
        "properties": {
            "status": {
                "type": "string",
                "description": "Optional Mercury status filter (active/closed).",
            }
        },
    },
    "outputSchema": {
        "type": "object",
        "properties": {
            "status": {"type": "string"},
            "data": {
                "type": "object",
                "properties": {
                    "accounts": {"type": "array"},
                    "total_balance": {"type": "number"},
                },
            },
            "timestamp": {"type": "string"},
        },
    },
}


def mercury_balance_fetcher(status: str | None = None, **_: Any) -> dict[str, Any]:
    """Fetch balances from Mercury."""
    try:
        token = os.getenv("MERCURY_API_TOKEN")
        if not token:
            raise ValueError("MERCURY_API_TOKEN missing; see .env.template")

        headers = {"Authorization": f"Bearer {token}"}
        params = {"status": status} if status else None
        response = requests.get(f"{API_BASE}/accounts", headers=headers, params=params, timeout=15)
        response.raise_for_status()
        payload = response.json()
        accounts = payload.get("accounts", payload.get("data", []))

        normalized = []
        total_balance = 0.0
        for account in accounts:
            balance = float(account.get("currentBalance", account.get("balance", 0.0)))
            total_balance += balance
            normalized.append({
                "id": account.get("id"),
                "name": account.get("name"),
                "currency": account.get("currency", "USD"),
                "balance": round(balance, 2),
                "status": account.get("status"),
            })

        data = {
            "accounts": normalized,
            "total_balance": round(total_balance, 2),
        }
        return {
            "status": "success",
            "data": data,
            "timestamp": datetime.now(timezone.utc).isoformat(),
        }
    except Exception as exc:
        _log_lesson("mercury_balance_fetcher", str(exc))
        return {
            "status": "error",
            "data": {"error": str(exc)},
            "timestamp": datetime.now(timezone.utc).isoformat(),
        }


def _log_lesson(skill_name: str, error: str) -> None:
    with open("logs/lessons.md", "a", encoding="utf-8") as handle:
        handle.write(f"- [{datetime.now(timezone.utc).isoformat()}] {skill_name}: {error}\n")
