"""Fetch currency exchange rates from a free API.

MCP Tool Name: exchange_rate_fetcher
"""
from __future__ import annotations
from datetime import datetime, timezone
from typing import Any

TOOL_META: dict[str, Any] = {
    "name": "exchange_rate_fetcher",
    "description": "Fetch currency exchange rate between two currencies using a free API. Returns rate and inverse.",
    "inputSchema": {
        "type": "object",
        "properties": {
            "base_currency": {
                "type": "string",
                "description": "Base currency ISO 4217 code (e.g., 'USD').",
                "default": "USD",
            },
            "target_currency": {
                "type": "string",
                "description": "Target currency ISO 4217 code (e.g., 'EUR').",
                "default": "EUR",
            },
        },
        "required": [],
    },
}


def exchange_rate_fetcher(
    base_currency: str = "USD",
    target_currency: str = "EUR",
) -> dict[str, Any]:
    """Fetch currency exchange rate between two currencies."""
    try:
        import httpx

        base = base_currency.upper()
        target = target_currency.upper()

        # Try exchangerate.host (free, no key required)
        rate = None
        source = None

        try:
            with httpx.Client(timeout=15) as client:
                resp = client.get(
                    f"https://open.er-api.com/v6/latest/{base}"
                )
                if resp.status_code == 200:
                    data = resp.json()
                    rates = data.get("rates", {})
                    if target in rates:
                        rate = rates[target]
                        source = "open.er-api.com"
        except Exception:
            pass

        if rate is None:
            # Fallback: try another free API
            try:
                with httpx.Client(timeout=15) as client:
                    resp = client.get(
                        f"https://api.exchangerate-api.com/v4/latest/{base}"
                    )
                    if resp.status_code == 200:
                        data = resp.json()
                        rates = data.get("rates", {})
                        if target in rates:
                            rate = rates[target]
                            source = "exchangerate-api.com"
            except Exception:
                pass

        if rate is None:
            return {
                "status": "error",
                "data": {
                    "error": f"Could not fetch exchange rate for {base}/{target}. "
                    "Free API may be temporarily unavailable."
                },
                "timestamp": datetime.now(timezone.utc).isoformat(),
            }

        inverse_rate = 1.0 / rate if rate != 0 else None

        return {
            "status": "ok",
            "data": {
                "base_currency": base,
                "target_currency": target,
                "rate": round(rate, 6),
                "inverse_rate": round(inverse_rate, 6) if inverse_rate else None,
                "interpretation": f"1 {base} = {rate:.4f} {target}",
                "inverse_interpretation": f"1 {target} = {inverse_rate:.4f} {base}" if inverse_rate else None,
                "source": source,
            },
            "timestamp": datetime.now(timezone.utc).isoformat(),
        }
    except Exception as exc:
        return {
            "status": "error",
            "data": {"error": str(exc)},
            "timestamp": datetime.now(timezone.utc).isoformat(),
        }
