"""Fetch University of Michigan Consumer Sentiment Index from FRED (series UMCSENT).

MCP Tool Name: consumer_confidence_fetcher
"""
from __future__ import annotations
from datetime import datetime, timezone
from typing import Any
import os

TOOL_META: dict[str, Any] = {
    "name": "consumer_confidence_fetcher",
    "description": "Fetch the University of Michigan Consumer Sentiment Index from FRED (series UMCSENT). Returns latest value and 12-month trend. Requires FRED_API_KEY.",
    "inputSchema": {
        "type": "object",
        "properties": {},
        "required": [],
    },
}


def consumer_confidence_fetcher() -> dict[str, Any]:
    """Fetch the University of Michigan Consumer Sentiment Index."""
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
            "series_id": "UMCSENT",
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
        trend_12mo = clean[:12]

        # Calculate trend direction
        trend_direction = None
        if len(trend_12mo) >= 2 and trend_12mo[0]["value"] is not None and trend_12mo[-1]["value"] is not None:
            change = trend_12mo[0]["value"] - trend_12mo[-1]["value"]
            trend_direction = "improving" if change > 0 else "declining" if change < 0 else "stable"

        return {
            "status": "ok",
            "data": {
                "series_id": "UMCSENT",
                "latest_value": latest["value"] if latest else None,
                "latest_date": latest["date"] if latest else None,
                "trend_12mo": trend_12mo,
                "trend_direction": trend_direction,
                "description": "University of Michigan Consumer Sentiment Index (1966:Q1=100). Higher values indicate greater consumer confidence.",
            },
            "timestamp": datetime.now(timezone.utc).isoformat(),
        }
    except Exception as exc:
        return {
            "status": "error",
            "data": {"error": str(exc)},
            "timestamp": datetime.now(timezone.utc).isoformat(),
        }
