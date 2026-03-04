"""Fetch commodity price data from FRED by mapping commodity names to series IDs.

MCP Tool Name: commodity_index_fetcher
"""
from __future__ import annotations
from datetime import datetime, timezone
from typing import Any
import os

# Map common commodity names to FRED series IDs
_COMMODITY_SERIES: dict[str, dict[str, str]] = {
    "gold": {"series_id": "GOLDAMGBD228NLBM", "description": "Gold Fixing Price (London, USD/troy oz)"},
    "silver": {"series_id": "SLVPRUSD", "description": "Silver Fixing Price (London, USD/troy oz)"},
    "oil": {"series_id": "DCOILWTICO", "description": "WTI Crude Oil (USD/barrel)"},
    "wti": {"series_id": "DCOILWTICO", "description": "WTI Crude Oil (USD/barrel)"},
    "brent": {"series_id": "DCOILBRENTEU", "description": "Brent Crude Oil (USD/barrel)"},
    "natural_gas": {"series_id": "DHHNGSP", "description": "Henry Hub Natural Gas (USD/MMBtu)"},
    "copper": {"series_id": "PCOPPUSDM", "description": "Global Copper Price (USD/metric ton, monthly)"},
    "aluminum": {"series_id": "PALUMUSDM", "description": "Global Aluminum Price (USD/metric ton, monthly)"},
    "wheat": {"series_id": "PWHEAMTUSDM", "description": "Global Wheat Price (USD/metric ton, monthly)"},
    "corn": {"series_id": "PMAIZMTUSDM", "description": "Global Maize/Corn Price (USD/metric ton, monthly)"},
    "cotton": {"series_id": "PCOTTINDUSDM", "description": "Cotton Price Index (USD, monthly)"},
    "sugar": {"series_id": "PSUGAISAUSDM", "description": "Global Sugar Price (USD cents/lb, monthly)"},
    "coffee": {"series_id": "PCOFFOTMUSDM", "description": "Global Coffee Price (USD cents/lb, monthly)"},
}

TOOL_META: dict[str, Any] = {
    "name": "commodity_index_fetcher",
    "description": "Fetch commodity price data from FRED. Supports: gold, silver, oil/wti, brent, natural_gas, copper, aluminum, wheat, corn, cotton, sugar, coffee. Requires FRED_API_KEY.",
    "inputSchema": {
        "type": "object",
        "properties": {
            "commodity": {
                "type": "string",
                "description": "Commodity name (e.g., 'gold', 'oil', 'copper', 'wheat').",
                "default": "gold",
            },
        },
        "required": [],
    },
}


def commodity_index_fetcher(commodity: str = "gold") -> dict[str, Any]:
    """Fetch commodity price data from FRED."""
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

        key = commodity.lower().replace(" ", "_")
        if key not in _COMMODITY_SERIES:
            return {
                "status": "error",
                "data": {
                    "error": f"Unknown commodity '{commodity}'. Available: {', '.join(sorted(_COMMODITY_SERIES.keys()))}",
                },
                "timestamp": datetime.now(timezone.utc).isoformat(),
            }

        series_info = _COMMODITY_SERIES[key]
        series_id = series_info["series_id"]

        import httpx

        url = "https://api.stlouisfed.org/fred/series/observations"
        params = {
            "series_id": series_id,
            "api_key": api_key,
            "file_type": "json",
            "sort_order": "desc",
            "limit": "30",
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
                "commodity": commodity,
                "series_id": series_id,
                "description": series_info["description"],
                "latest_value": latest["value"] if latest else None,
                "latest_date": latest["date"] if latest else None,
                "recent_history": clean[:20],
            },
            "timestamp": datetime.now(timezone.utc).isoformat(),
        }
    except Exception as exc:
        return {
            "status": "error",
            "data": {"error": str(exc)},
            "timestamp": datetime.now(timezone.utc).isoformat(),
        }
