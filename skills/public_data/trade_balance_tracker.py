"""Track US trade balance from FRED (series BOPGSTB).

MCP Tool Name: trade_balance_tracker
"""
from __future__ import annotations
from datetime import datetime, timezone
from typing import Any
import os

TOOL_META: dict[str, Any] = {
    "name": "trade_balance_tracker",
    "description": "Track the US trade balance (goods and services) from FRED (series BOPGSTB). Returns latest value. Requires FRED_API_KEY.",
    "inputSchema": {
        "type": "object",
        "properties": {},
        "required": [],
    },
}


def trade_balance_tracker() -> dict[str, Any]:
    """Track the US trade balance from FRED."""
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
            "series_id": "BOPGSTB",
            "api_key": api_key,
            "file_type": "json",
            "sort_order": "desc",
            "limit": "24",
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
        ]

        latest = clean[0] if clean else None

        return {
            "status": "ok",
            "data": {
                "series_id": "BOPGSTB",
                "latest_value": latest["value"] if latest else None,
                "latest_date": latest["date"] if latest else None,
                "recent_history": clean[:12],
                "description": "Trade Balance: Goods and Services, Balance of Payments Basis (millions of dollars, seasonally adjusted). Negative values indicate a trade deficit.",
            },
            "timestamp": datetime.now(timezone.utc).isoformat(),
        }
    except Exception as exc:
        return {
            "status": "error",
            "data": {"error": str(exc)},
            "timestamp": datetime.now(timezone.utc).isoformat(),
        }
