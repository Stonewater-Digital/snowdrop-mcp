"""Track macroeconomic indicators via the FRED API."""
from __future__ import annotations

import os
from datetime import datetime, timezone
from typing import Any

import requests

TOOL_META: dict[str, Any] = {
    "name": "macro_indicator_tracker",
    "description": "Fetches recent FRED indicators and computes MoM trends.",
    "inputSchema": {
        "type": "object",
        "properties": {
            "indicators": {
                "type": "array",
                "items": {"type": "string"},
            },
            "periods": {"type": "integer", "default": 12},
        },
        "required": ["indicators"],
    },
    "outputSchema": {
        "type": "object",
        "properties": {
            "status": {"type": "string"},
            "data": {
                "type": "object",
                "properties": {
                    "indicators": {"type": "object"},
                },
            },
            "timestamp": {"type": "string"},
        },
    },
}


def macro_indicator_tracker(
    indicators: list[str],
    periods: int = 12,
    **_: Any,
) -> dict[str, Any]:
    """Fetch FRED observations and compute month-over-month deltas."""

    try:
        if not indicators:
            raise ValueError("indicators list cannot be empty")
        if periods <= 0:
            raise ValueError("periods must be positive")

        api_key = os.getenv("FRED_API_KEY")
        if not api_key:
            raise ValueError("FRED_API_KEY missing; see .env.template")

        indicator_data: dict[str, Any] = {}
        for series_id in indicators:
            series_payload = _fetch_series(series_id, periods, api_key)
            indicator_data[series_id] = series_payload

        return {
            "status": "success",
            "data": {"indicators": indicator_data},
            "timestamp": datetime.now(timezone.utc).isoformat(),
        }
    except Exception as exc:
        _log_lesson("macro_indicator_tracker", str(exc))
        return {
            "status": "error",
            "data": {"error": str(exc)},
            "timestamp": datetime.now(timezone.utc).isoformat(),
        }


def _fetch_series(series_id: str, limit: int, api_key: str) -> dict[str, Any]:
    endpoint = "https://api.stlouisfed.org/fred/series/observations"
    params = {
        "series_id": series_id,
        "api_key": api_key,
        "file_type": "json",
        "sort_order": "desc",
        "limit": limit,
    }
    response = requests.get(endpoint, params=params, timeout=15)
    response.raise_for_status()
    data = response.json()
    observations = data.get("observations", [])
    cleaned: list[dict[str, Any]] = []
    for obs in observations:
        value = obs.get("value")
        try:
            numeric_value = float(value)
        except (TypeError, ValueError):
            continue
        cleaned.append({"date": obs.get("date"), "value": numeric_value})

    cleaned.sort(key=lambda x: x["date"], reverse=True)
    latest = cleaned[0] if cleaned else {"value": None}
    mom_change = None
    if len(cleaned) >= 2 and cleaned[1]["value"] not in (None, 0):
        mom_change = ((latest["value"] - cleaned[1]["value"]) / cleaned[1]["value"]) * 100

    return {
        "latest_value": latest["value"],
        "mom_change_pct": None if mom_change is None else round(mom_change, 3),
        "observations": cleaned,
    }


def _log_lesson(skill_name: str, error: str) -> None:
    """Append a Ralph Wiggum lesson entry."""

    with open("logs/lessons.md", "a", encoding="utf-8") as handle:
        handle.write(f"- [{datetime.now(timezone.utc).isoformat()}] {skill_name}: {error}\n")
