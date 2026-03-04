"""Track the S&P 500 price-to-earnings ratio with historical comparison.

MCP Tool Name: sp500_pe_ratio_tracker
"""
from __future__ import annotations
from datetime import datetime, timezone
from typing import Any

# Hardcoded recent P/E data (S&P 500 trailing 12-month P/E ratio, approximate year-end values)
_PE_HISTORY: list[dict[str, Any]] = [
    {"year": 2025, "pe_ratio": 23.5, "note": "estimated mid-year"},
    {"year": 2024, "pe_ratio": 24.8, "note": "year-end"},
    {"year": 2023, "pe_ratio": 22.4, "note": "year-end"},
    {"year": 2022, "pe_ratio": 18.1, "note": "year-end"},
    {"year": 2021, "pe_ratio": 26.7, "note": "year-end"},
    {"year": 2020, "pe_ratio": 37.3, "note": "year-end, elevated due to COVID earnings drop"},
    {"year": 2019, "pe_ratio": 23.2, "note": "year-end"},
    {"year": 2018, "pe_ratio": 18.9, "note": "year-end"},
    {"year": 2017, "pe_ratio": 23.6, "note": "year-end"},
    {"year": 2016, "pe_ratio": 23.7, "note": "year-end"},
    {"year": 2015, "pe_ratio": 20.0, "note": "year-end"},
]

TOOL_META: dict[str, Any] = {
    "name": "sp500_pe_ratio_tracker",
    "description": "Get S&P 500 price-to-earnings ratio with historical comparison. Uses hardcoded recent data and historical averages.",
    "inputSchema": {
        "type": "object",
        "properties": {},
        "required": [],
    },
}


def sp500_pe_ratio_tracker() -> dict[str, Any]:
    """Get S&P 500 price-to-earnings ratio with historical comparison."""
    try:
        current = _PE_HISTORY[0]
        pe_values = [entry["pe_ratio"] for entry in _PE_HISTORY]
        recent_avg = sum(pe_values) / len(pe_values)

        historical_avg = 16.0  # Long-run average since ~1870
        current_pe = current["pe_ratio"]

        if current_pe > historical_avg * 1.5:
            valuation = "Significantly above historical average — potentially overvalued"
        elif current_pe > historical_avg * 1.2:
            valuation = "Above historical average — elevated valuation"
        elif current_pe > historical_avg * 0.8:
            valuation = "Near historical average — roughly fair value"
        else:
            valuation = "Below historical average — potentially undervalued"

        premium_to_historical = round((current_pe - historical_avg) / historical_avg * 100, 1)

        return {
            "status": "ok",
            "data": {
                "current_estimate": {
                    "pe_ratio": current_pe,
                    "year": current["year"],
                    "note": current["note"],
                },
                "historical_average": historical_avg,
                "recent_10y_average": round(recent_avg, 1),
                "premium_to_historical_pct": premium_to_historical,
                "valuation_assessment": valuation,
                "history": _PE_HISTORY,
                "context": (
                    "The long-run average S&P 500 P/E ratio is approximately 15-17x. "
                    "Lower P/E ratios generally indicate cheaper valuations (or depressed earnings). "
                    "Higher P/E ratios can indicate overvaluation or strong growth expectations. "
                    "The Shiller CAPE ratio (cyclically adjusted) uses 10-year average earnings for smoother comparison."
                ),
                "note": "P/E data is approximate and based on trailing 12-month earnings. For real-time data, use a financial data provider.",
            },
            "timestamp": datetime.now(timezone.utc).isoformat(),
        }
    except Exception as exc:
        return {
            "status": "error",
            "data": {"error": str(exc)},
            "timestamp": datetime.now(timezone.utc).isoformat(),
        }
