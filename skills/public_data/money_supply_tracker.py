"""Track US money supply (M1 or M2) from FRED.

MCP Tool Name: money_supply_tracker
"""
from __future__ import annotations
from datetime import datetime, timezone
from typing import Any
import os

TOOL_META: dict[str, Any] = {
    "name": "money_supply_tracker",
    "description": "Track US money supply from FRED. Supports M1 (M1SL) and M2 (M2SL) measures. Returns latest value and trend. Requires FRED_API_KEY.",
    "inputSchema": {
        "type": "object",
        "properties": {
            "measure": {
                "type": "string",
                "description": "Money supply measure: 'M1' or 'M2'.",
                "default": "M2",
                "enum": ["M1", "M2"],
            },
        },
        "required": [],
    },
}

_SERIES_MAP = {
    "M1": "M1SL",
    "M2": "M2SL",
}


def money_supply_tracker(measure: str = "M2") -> dict[str, Any]:
    """Track US money supply from FRED."""
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

        measure_upper = measure.upper()
        series_id = _SERIES_MAP.get(measure_upper)
        if not series_id:
            return {
                "status": "error",
                "data": {"error": f"Invalid measure '{measure}'. Use 'M1' or 'M2'."},
                "timestamp": datetime.now(timezone.utc).isoformat(),
            }

        import httpx

        url = "https://api.stlouisfed.org/fred/series/observations"
        params = {
            "series_id": series_id,
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

        descriptions = {
            "M1": "M1 Money Stock: currency, demand deposits, other checkable deposits, travelers' checks (billions of dollars, seasonally adjusted).",
            "M2": "M2 Money Stock: M1 plus savings deposits, small time deposits, money market funds (billions of dollars, seasonally adjusted).",
        }

        return {
            "status": "ok",
            "data": {
                "series_id": series_id,
                "measure": measure_upper,
                "latest_value": latest["value"] if latest else None,
                "latest_date": latest["date"] if latest else None,
                "yoy_change_pct": yoy_change,
                "recent_history": clean[:12],
                "description": descriptions.get(measure_upper, ""),
            },
            "timestamp": datetime.now(timezone.utc).isoformat(),
        }
    except Exception as exc:
        return {
            "status": "error",
            "data": {"error": str(exc)},
            "timestamp": datetime.now(timezone.utc).isoformat(),
        }
