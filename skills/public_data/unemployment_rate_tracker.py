"""Track US unemployment rate using BLS API with static fallback data.

MCP Tool Name: unemployment_rate_tracker
"""
from __future__ import annotations
from datetime import datetime, timezone
from typing import Any
import os

# Static fallback: recent monthly unemployment rates (seasonally adjusted)
_FALLBACK_DATA: list[dict[str, Any]] = [
    {"year": 2025, "month": 2, "rate": 4.1},
    {"year": 2025, "month": 1, "rate": 4.0},
    {"year": 2024, "month": 12, "rate": 4.1},
    {"year": 2024, "month": 11, "rate": 4.2},
    {"year": 2024, "month": 10, "rate": 4.1},
    {"year": 2024, "month": 9, "rate": 4.1},
    {"year": 2024, "month": 8, "rate": 4.2},
    {"year": 2024, "month": 7, "rate": 4.3},
    {"year": 2024, "month": 6, "rate": 4.1},
    {"year": 2024, "month": 5, "rate": 4.0},
    {"year": 2024, "month": 4, "rate": 3.9},
    {"year": 2024, "month": 3, "rate": 3.8},
]

TOOL_META: dict[str, Any] = {
    "name": "unemployment_rate_tracker",
    "description": "Track the US unemployment rate (BLS series LNS14000000). Uses BLS API if BLS_API_KEY is set, otherwise returns static recent data.",
    "inputSchema": {
        "type": "object",
        "properties": {
            "months": {
                "type": "integer",
                "description": "Number of recent months of data to return.",
                "default": 12,
            },
        },
        "required": [],
    },
}


def unemployment_rate_tracker(months: int = 12) -> dict[str, Any]:
    """Track the US unemployment rate."""
    try:
        api_key = os.environ.get("BLS_API_KEY", "")
        source = "static_fallback"
        data_points: list[dict[str, Any]] = []

        if api_key:
            try:
                import httpx

                now = datetime.now(timezone.utc)
                payload = {
                    "seriesid": ["LNS14000000"],
                    "startyear": str(now.year - 1),
                    "endyear": str(now.year),
                    "registrationkey": api_key,
                }
                with httpx.Client(timeout=30) as client:
                    resp = client.post(
                        "https://api.bls.gov/publicAPI/v2/timeseries/data/",
                        json=payload,
                    )
                    resp.raise_for_status()
                    result = resp.json()

                for series in result.get("Results", {}).get("series", []):
                    for entry in series.get("data", []):
                        period = entry.get("period", "")
                        if period.startswith("M"):
                            data_points.append({
                                "year": int(entry["year"]),
                                "month": int(period[1:]),
                                "rate": float(entry["value"]),
                            })

                if data_points:
                    data_points.sort(key=lambda x: (x["year"], x["month"]), reverse=True)
                    source = "bls_api"
            except Exception:
                pass

        if not data_points:
            data_points = _FALLBACK_DATA[:months]
            source = "static_fallback"

        data_points = data_points[:months]
        latest = data_points[0] if data_points else None

        return {
            "status": "ok",
            "data": {
                "series_id": "LNS14000000",
                "source": source,
                "latest_rate": latest["rate"] if latest else None,
                "latest_period": f"{latest['year']}-{latest['month']:02d}" if latest else None,
                "count": len(data_points),
                "observations": data_points,
                "note": "Seasonally adjusted civilian unemployment rate."
                + (" Data is from static fallback. Set BLS_API_KEY for live data." if source == "static_fallback" else ""),
            },
            "timestamp": datetime.now(timezone.utc).isoformat(),
        }
    except Exception as exc:
        return {
            "status": "error",
            "data": {"error": str(exc)},
            "timestamp": datetime.now(timezone.utc).isoformat(),
        }
