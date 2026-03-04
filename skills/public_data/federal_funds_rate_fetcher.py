"""Fetch the Federal Funds Rate from FRED (series FEDFUNDS).

MCP Tool Name: federal_funds_rate_fetcher
"""
from __future__ import annotations
from datetime import datetime, timezone
from typing import Any
import os

TOOL_META: dict[str, Any] = {
    "name": "federal_funds_rate_fetcher",
    "description": "Fetch the effective Federal Funds Rate from FRED (series FEDFUNDS). Returns latest rate and recent history. Requires FRED_API_KEY.",
    "inputSchema": {
        "type": "object",
        "properties": {},
        "required": [],
    },
}


def federal_funds_rate_fetcher() -> dict[str, Any]:
    """Fetch the effective Federal Funds Rate from FRED."""
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
            "series_id": "FEDFUNDS",
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
                "rate": float(obs["value"]) if obs["value"] != "." else None,
            }
            for obs in observations
        ]

        latest = clean[0] if clean else None
        history = clean[:12]

        return {
            "status": "ok",
            "data": {
                "series_id": "FEDFUNDS",
                "latest_rate": latest["rate"] if latest else None,
                "latest_date": latest["date"] if latest else None,
                "history_12mo": history,
                "description": "Effective Federal Funds Rate (monthly average, percent, not seasonally adjusted).",
            },
            "timestamp": datetime.now(timezone.utc).isoformat(),
        }
    except Exception as exc:
        return {
            "status": "error",
            "data": {"error": str(exc)},
            "timestamp": datetime.now(timezone.utc).isoformat(),
        }
