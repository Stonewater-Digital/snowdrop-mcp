"""Fetch the US Treasury yield curve across multiple maturities.

MCP Tool Name: yield_curve_fetcher
"""
from __future__ import annotations
from datetime import datetime, timezone
from typing import Any

TOOL_META: dict[str, Any] = {
    "name": "yield_curve_fetcher",
    "description": "Fetch the US Treasury yield curve across multiple maturities (1M to 30Y) from the Treasury Fiscal Data API. Includes inversion detection. No API key required.",
    "inputSchema": {
        "type": "object",
        "properties": {},
        "required": [],
    },
}

# Treasury security descriptions and their approximate maturity labels
_SECURITY_MATURITIES = [
    ("Treasury Bills", "1-Month", "1M"),
    ("Treasury Bills", "3-Month", "3M"),
    ("Treasury Bills", "6-Month", "6M"),
    ("Treasury Notes", "1-Year", "1Y"),
    ("Treasury Notes", "2-Year", "2Y"),
    ("Treasury Notes", "5-Year", "5Y"),
    ("Treasury Notes", "10-Year", "10Y"),
    ("Treasury Bonds", "30-Year", "30Y"),
]


def yield_curve_fetcher() -> dict[str, Any]:
    """Fetch the US Treasury yield curve across multiple maturities."""
    try:
        import httpx

        url = "https://api.fiscaldata.treasury.gov/services/api/fiscal_service/v2/accounting/od/avg_interest_rates"
        params = {
            "sort": "-record_date",
            "page[size]": "200",
        }

        with httpx.Client(timeout=30) as client:
            resp = client.get(url, params=params)
            resp.raise_for_status()
            data = resp.json()

        records = data.get("data", [])
        if not records:
            return {
                "status": "error",
                "data": {"error": "No data returned from Treasury API."},
                "timestamp": datetime.now(timezone.utc).isoformat(),
            }

        # Get the most recent record date
        latest_date = records[0]["record_date"]

        # Filter to latest date only
        latest_records = [r for r in records if r["record_date"] == latest_date]

        # Build yield curve
        curve: dict[str, float | None] = {}
        for sec_type, sec_term, label in _SECURITY_MATURITIES:
            for r in latest_records:
                desc = r.get("security_desc", "")
                term = r.get("security_term", "")
                if sec_type.lower() in desc.lower() and sec_term.lower() in term.lower():
                    try:
                        curve[label] = float(r["avg_interest_rate_amt"])
                    except (ValueError, KeyError):
                        curve[label] = None
                    break
            if label not in curve:
                curve[label] = None

        # Check for inversions
        inversions = []
        labels = [label for _, _, label in _SECURITY_MATURITIES]
        for i in range(len(labels)):
            for j in range(i + 1, len(labels)):
                short_label = labels[i]
                long_label = labels[j]
                short_rate = curve.get(short_label)
                long_rate = curve.get(long_label)
                if short_rate is not None and long_rate is not None and short_rate > long_rate:
                    inversions.append({
                        "short_maturity": short_label,
                        "long_maturity": long_label,
                        "short_rate": short_rate,
                        "long_rate": long_rate,
                        "inversion_bps": round((short_rate - long_rate) * 100, 1),
                    })

        # Key spread: 10Y-2Y
        spread_10y_2y = None
        if curve.get("10Y") is not None and curve.get("2Y") is not None:
            spread_10y_2y = round(curve["10Y"] - curve["2Y"], 4)

        return {
            "status": "ok",
            "data": {
                "date": latest_date,
                "yield_curve": curve,
                "spread_10y_2y": spread_10y_2y,
                "is_inverted": len(inversions) > 0,
                "inversions": inversions,
                "description": "US Treasury yield curve from Fiscal Data API (average interest rates). Inversion occurs when short-term yields exceed long-term yields.",
            },
            "timestamp": datetime.now(timezone.utc).isoformat(),
        }
    except Exception as exc:
        return {
            "status": "error",
            "data": {"error": str(exc)},
            "timestamp": datetime.now(timezone.utc).isoformat(),
        }
