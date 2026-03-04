"""Fetch the CBOE Volatility Index (VIX) from FRED (series VIXCLS).

MCP Tool Name: vix_level_fetcher
"""
from __future__ import annotations
from datetime import datetime, timezone
from typing import Any
import os

TOOL_META: dict[str, Any] = {
    "name": "vix_level_fetcher",
    "description": "Fetch the CBOE Volatility Index (VIX) from FRED (series VIXCLS). Returns latest level with interpretation. Requires FRED_API_KEY.",
    "inputSchema": {
        "type": "object",
        "properties": {},
        "required": [],
    },
}


def vix_level_fetcher() -> dict[str, Any]:
    """Fetch the CBOE Volatility Index (VIX) from FRED."""
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
            "series_id": "VIXCLS",
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
        vix_value = latest["value"] if latest else None

        if vix_value is not None:
            if vix_value < 15:
                regime = "Low volatility — complacency, calm markets"
            elif vix_value < 20:
                regime = "Normal volatility — typical market conditions"
            elif vix_value < 30:
                regime = "Elevated volatility — market uncertainty or stress"
            elif vix_value < 40:
                regime = "High volatility — significant market fear"
            else:
                regime = "Extreme volatility — panic or crisis conditions"
        else:
            regime = "Unknown"

        return {
            "status": "ok",
            "data": {
                "series_id": "VIXCLS",
                "latest_value": vix_value,
                "latest_date": latest["date"] if latest else None,
                "regime": regime,
                "recent_history": clean[:20],
                "description": "CBOE Volatility Index (VIX) — measures the market's expectation of 30-day forward-looking volatility, derived from S&P 500 option prices. Often called the 'fear gauge'.",
            },
            "timestamp": datetime.now(timezone.utc).isoformat(),
        }
    except Exception as exc:
        return {
            "status": "error",
            "data": {"error": str(exc)},
            "timestamp": datetime.now(timezone.utc).isoformat(),
        }
