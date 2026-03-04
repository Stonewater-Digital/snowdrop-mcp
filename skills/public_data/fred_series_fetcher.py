"""Fetch economic data series from the Federal Reserve Economic Data (FRED) API.

MCP Tool Name: fred_series_fetcher
"""
from __future__ import annotations
from datetime import datetime, timezone
from typing import Any
import os

TOOL_META: dict[str, Any] = {
    "name": "fred_series_fetcher",
    "description": "Fetch economic data series observations from the FRED API by series ID (e.g., GDP, UNRATE, CPIAUCSL). Requires FRED_API_KEY environment variable.",
    "inputSchema": {
        "type": "object",
        "properties": {
            "series_id": {
                "type": "string",
                "description": "FRED series ID (e.g., 'GDP', 'UNRATE', 'CPIAUCSL').",
            },
            "observation_start": {
                "type": "string",
                "description": "Start date in YYYY-MM-DD format. Optional.",
            },
            "observation_end": {
                "type": "string",
                "description": "End date in YYYY-MM-DD format. Optional.",
            },
        },
        "required": ["series_id"],
    },
}


def fred_series_fetcher(
    series_id: str,
    observation_start: str = "",
    observation_end: str = "",
) -> dict[str, Any]:
    """Fetch economic data series observations from the FRED API."""
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

        params: dict[str, str] = {
            "series_id": series_id,
            "api_key": api_key,
            "file_type": "json",
        }
        if observation_start:
            params["observation_start"] = observation_start
        if observation_end:
            params["observation_end"] = observation_end

        url = "https://api.stlouisfed.org/fred/series/observations"
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

        return {
            "status": "ok",
            "data": {
                "series_id": series_id,
                "count": len(clean),
                "observations": clean,
            },
            "timestamp": datetime.now(timezone.utc).isoformat(),
        }
    except Exception as exc:
        return {
            "status": "error",
            "data": {"error": str(exc)},
            "timestamp": datetime.now(timezone.utc).isoformat(),
        }
