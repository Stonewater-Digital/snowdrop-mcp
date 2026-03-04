"""Convert crypto ↔ fiat values using Coingecko pricing."""
from __future__ import annotations

import os
from datetime import datetime, timezone
from typing import Any

import requests

TOOL_META: dict[str, Any] = {
    "name": "crypto_fiat_converter",
    "description": "Uses USD hub conversions (pending Thunder approval for transfers).",
    "inputSchema": {
        "type": "object",
        "properties": {
            "amount": {"type": "number"},
            "from_currency": {"type": "string"},
            "to_currency": {"type": "string"},
            "prices": {
                "type": "object",
                "description": "Optional override mapping currency -> USD rate or dict with usd key.",
            },
        },
        "required": ["amount", "from_currency", "to_currency"],
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

_FIAT = {"USD", "EUR", "GBP", "JPY", "CHF", "CAD"}
_CG_IDS = {
    "BTC": "bitcoin",
    "ETH": "ethereum",
    "TON": "toncoin",
    "SOL": "solana",
    "USDC": "usd-coin",
    "USDT": "tether",
}
_CG_URL = "https://pro-api.coingecko.com/api/v3/simple/price"


def crypto_fiat_converter(
    amount: float,
    from_currency: str,
    to_currency: str,
    prices: dict[str, Any] | None = None,
    **_: Any,
) -> dict[str, Any]:
    """Return converted amount, rate used, and provenance."""
    try:
        if amount < 0:
            raise ValueError("amount cannot be negative")
        if not from_currency or not to_currency:
            raise ValueError("from_currency and to_currency are required")

        source = "provided_prices" if prices else "coingecko"
        usd_rates = prices and _normalize_prices(prices) or _fetch_usd_rates(from_currency, to_currency)

        from_rate = usd_rates.get(from_currency.upper())
        to_rate = usd_rates.get(to_currency.upper())
        if from_rate is None or to_rate is None:
            raise ValueError("Missing rate for one of the currencies")

        usd_value = amount * from_rate
        converted_amount = usd_value / to_rate
        rate_used = converted_amount / amount if amount else 0.0

        data = {
            "converted_amount": round(converted_amount, 6),
            "rate_used": round(rate_used, 6),
            "rate_source": source,
            "path": [from_currency.upper(), "USD", to_currency.upper()],
            "execution_status": "pending_thunder_approval",
        }
        return {
            "status": "success",
            "data": data,
            "timestamp": datetime.now(timezone.utc).isoformat(),
        }
    except Exception as exc:
        _log_lesson("crypto_fiat_converter", str(exc))
        return {
            "status": "error",
            "data": {"error": str(exc)},
            "timestamp": datetime.now(timezone.utc).isoformat(),
        }


def _normalize_prices(prices: dict[str, Any]) -> dict[str, float]:
    normalized: dict[str, float] = {}
    for currency, value in prices.items():
        if isinstance(value, dict):
            rate = float(value.get("usd"))
        else:
            rate = float(value)
        normalized[currency.upper()] = rate
    return normalized


def _fetch_usd_rates(from_currency: str, to_currency: str) -> dict[str, float]:
    api_key = os.getenv("COINGECKO_API_KEY")
    if not api_key:
        raise ValueError("COINGECKO_API_KEY missing; see .env.template")
    currencies_needed = {from_currency.upper(), to_currency.upper()}
    fiats_needed = {cur for cur in currencies_needed if cur in _FIAT}
    crypto_needed = {cur for cur in currencies_needed if cur not in _FIAT}
    ids = {_CG_IDS.get(cur, cur.lower()) for cur in crypto_needed}
    ids.add("bitcoin")
    vs_currencies = {"usd"} | {fiat.lower() for fiat in fiats_needed}
    params = {
        "ids": ",".join(sorted(ids)),
        "vs_currencies": ",".join(sorted(vs_currencies)),
    }
    headers = {"x-cg-pro-api-key": api_key}
    response = requests.get(_CG_URL, params=params, headers=headers, timeout=10)
    response.raise_for_status()
    payload = response.json()

    usd_rates: dict[str, float] = {"USD": 1.0}
    btc_prices = payload.get("bitcoin", {})
    btc_usd = float(btc_prices.get("usd", 0.0))
    for fiat in fiats_needed:
        if fiat == "USD":
            continue
        fiat_key = fiat.lower()
        fiat_price = float(btc_prices.get(fiat_key, 0.0))
        if fiat_price == 0:
            continue
        usd_rates[fiat] = btc_usd / fiat_price

    for crypto in crypto_needed:
        cg_id = _CG_IDS.get(crypto, crypto.lower())
        price = payload.get(cg_id, {}).get("usd")
        if price:
            usd_rates[crypto] = float(price)

    return usd_rates


def _log_lesson(skill_name: str, error: str) -> None:
    with open("logs/lessons.md", "a", encoding="utf-8") as handle:
        handle.write(f"- [{datetime.now(timezone.utc).isoformat()}] {skill_name}: {error}\n")
