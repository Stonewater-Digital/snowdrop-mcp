"""Track US housing starts from FRED (series HOUST).

MCP Tool Name: housing_starts_tracker
"""
from __future__ import annotations
from datetime import datetime, timezone
from typing import Any
import os

TOOL_META: dict[str, Any] = {
    "name": "housing_starts_tracker",
    "description": "Track US housing starts from FRED (series HOUST). Returns latest value and year-over-year change. Requires FRED_API_KEY.",
    "inputSchema": {
        "type": "object",
        "properties": {},
        "required": [],
    },
}


def housing_starts_tracker() -> dict[str, Any]:
    """Track US housing starts from FRED."""
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
            "series_id": "HOUST",
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
        yoy_change = None
        if len(clean) >= 13 and clean[0]["value"] is not None and clean[12]["value"] is not None:
            yoy_change = round((clean[0]["value"] - clean[12]["value"]) / clean[12]["value"] * 100, 2)

        return {
            "status": "ok",
            "data": {
                "series_id": "HOUST",
                "latest_value": latest["value"] if latest else None,
                "latest_date": latest["date"] if latest else None,
                "yoy_change_pct": yoy_change,
                "recent_history": clean[:12],
                "description": "Housing Starts: Total New Privately Owned Housing Units Started (thousands of units, seasonally adjusted annual rate).",
            },
            "timestamp": datetime.now(timezone.utc).isoformat(),
        }
    except Exception as exc:
        return {
            "status": "error",
            "data": {"error": str(exc)},
            "timestamp": datetime.now(timezone.utc).isoformat(),
        }
