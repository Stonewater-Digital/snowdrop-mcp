"""Fetch FX rates from the ExchangeRate API."""
from __future__ import annotations

import os
from datetime import datetime, timezone
from typing import Any

import requests

TOOL_META: dict[str, Any] = {
    "name": "fx_rate_fetcher",
    "description": "Retrieves spot FX quotes and inverse rates via ExchangeRate-API.",
    "inputSchema": {
        "type": "object",
        "properties": {
            "base_currency": {"type": "string", "default": "USD"},
            "target_currencies": {
                "type": "array",
                "items": {"type": "string"},
                "default": ["EUR", "GBP", "JPY"],
            },
        },
        "required": [],
    },
    "outputSchema": {
        "type": "object",
        "properties": {
            "status": {"type": "string"},
            "data": {"type": "object"},
            "timestamp": {"type": "string"},
        },
    },
}

_API_URL = "https://v6.exchangerate-api.com/v6/{key}/latest/{base}"


def fx_rate_fetcher(
    base_currency: str = "USD",
    target_currencies: list[str] | None = None,
    **_: Any,
) -> dict[str, Any]:
    """Return FX rates and inverse rates."""
    try:
        api_key = os.getenv("EXCHANGERATE_API_KEY")
        if not api_key:
            raise ValueError("EXCHANGERATE_API_KEY missing; see .env.template")
        targets = target_currencies or ["EUR", "GBP", "JPY"]
        response = requests.get(
            _API_URL.format(key=api_key, base=base_currency.upper()), timeout=10
        )
        response.raise_for_status()
        payload = response.json()
        rates = payload.get("conversion_rates", {})
        result: dict[str, dict[str, float | None]] = {}
        for currency in targets:
            rate = rates.get(currency.upper())
            if rate is None:
                continue
            result[currency.upper()] = {
                "rate": rate,
                "inverse": round(1 / rate, 6) if rate else None,
            }
        data = {
            "base_currency": base_currency.upper(),
            "rates": result,
            "fx_timestamp": payload.get("time_last_update_utc"),
        }
        return {
            "status": "success",
            "data": data,
            "timestamp": datetime.now(timezone.utc).isoformat(),
        }
    except Exception as exc:
        _log_lesson("fx_rate_fetcher", str(exc))
        return {
            "status": "error",
            "data": {"error": str(exc)},
            "timestamp": datetime.now(timezone.utc).isoformat(),
        }


def _log_lesson(skill_name: str, error: str) -> None:
    with open("logs/lessons.md", "a", encoding="utf-8") as handle:
        handle.write(f"- [{datetime.now(timezone.utc).isoformat()}] {skill_name}: {error}\n")
