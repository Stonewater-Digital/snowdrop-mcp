"""Fetch WTI crude oil price from FRED (series DCOILWTICO).

MCP Tool Name: crude_oil_price_fetcher
"""
from __future__ import annotations
from datetime import datetime, timezone
from typing import Any
import os

TOOL_META: dict[str, Any] = {
    "name": "crude_oil_price_fetcher",
    "description": "Fetch WTI (West Texas Intermediate) crude oil spot price from FRED (series DCOILWTICO). Requires FRED_API_KEY.",
    "inputSchema": {
        "type": "object",
        "properties": {},
        "required": [],
    },
}


def crude_oil_price_fetcher() -> dict[str, Any]:
    """Fetch WTI crude oil spot price from FRED."""
    try:
        api_key = os.environ.get("FRED_API_KEY", "")
        if not api_key:
            return {
                "status": "error",
                "data": {
                    "error": "FRED_API_KEY environment variable is not set. "
                    "Get a free key at https://fred.stlouisfed.org/docs/api/api_key.html"
                },
                "timestamp": datetime.now(timezone.utc).isoformat(),
            }

        import httpx

        url = "https://api.stlouisfed.org/fred/series/observations"
        params = {
            "series_id": "DCOILWTICO",
            "api_key": api_key,
            "file_type": "json",
            "sort_order": "desc",
            "limit": "60",
        }

        with httpx.Client(timeout=30) as client:
            resp = client.get(url, params=params)
            resp.raise_for_status()
            data = resp.json()

        observations = data.get("observations", [])
        clean = [
            {
                "date": obs["date"],
                "value": float(obs["value"]) if obs["value"] != "." else None,
            }
            for obs in observations
            if obs["value"] != "."
        ]

        latest = clean[0] if clean else None

        return {
            "status": "ok",
            "data": {
                "series_id": "DCOILWTICO",
                "latest_price_usd": latest["value"] if latest else None,
                "latest_date": latest["date"] if latest else None,
                "unit": "USD per barrel",
                "recent_history": clean[:20],
                "description": "Crude Oil Prices: West Texas Intermediate (WTI) — Cushing, Oklahoma. Dollars per barrel, not seasonally adjusted.",
            },
            "timestamp": datetime.now(timezone.utc).isoformat(),
        }
    except Exception as exc:
        return {
            "status": "error",
            "data": {"error": str(exc)},
            "timestamp": datetime.now(timezone.utc).isoformat(),
        }
