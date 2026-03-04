"""Calculate the value of carbon credits with market comparisons.

MCP Tool Name: carbon_credit_value_calculator
"""
from __future__ import annotations
from datetime import datetime, timezone
from typing import Any

TOOL_META: dict[str, Any] = {
    "name": "carbon_credit_value_calculator",
    "description": "Calculate the monetary value of carbon credits/offsets and compare across EU ETS, compliance, and voluntary carbon markets.",
    "inputSchema": {
        "type": "object",
        "properties": {
            "tons_co2": {
                "type": "number",
                "description": "Metric tons of CO2 equivalent.",
            },
            "price_per_ton": {
                "type": "number",
                "description": "Price per metric ton of CO2 in USD.",
                "default": 50.0,
            },
        },
        "required": ["tons_co2"],
    },
}

# Reference market prices (approximate, late 2024)
_MARKET_PRICES = {
    "eu_ets": {"price": 70.0, "name": "EU Emissions Trading System"},
    "california_cap_trade": {"price": 35.0, "name": "California Cap-and-Trade"},
    "rggi": {"price": 14.0, "name": "Regional Greenhouse Gas Initiative (US Northeast)"},
    "voluntary_high_quality": {"price": 15.0, "name": "Voluntary Market (high-quality, e.g. Gold Standard)"},
    "voluntary_standard": {"price": 5.0, "name": "Voluntary Market (standard offsets)"},
}


def carbon_credit_value_calculator(
    tons_co2: float,
    price_per_ton: float = 50.0,
) -> dict[str, Any]:
    """Calculate carbon credit value."""
    try:
        if tons_co2 < 0:
            return {
                "status": "error",
                "data": {"error": "tons_co2 must be non-negative."},
                "timestamp": datetime.now(timezone.utc).isoformat(),
            }
        if price_per_ton < 0:
            return {
                "status": "error",
                "data": {"error": "price_per_ton must be non-negative."},
                "timestamp": datetime.now(timezone.utc).isoformat(),
            }

        value = tons_co2 * price_per_ton

        market_comparison = {}
        for key, info in _MARKET_PRICES.items():
            market_comparison[key] = {
                "name": info["name"],
                "price_per_ton": info["price"],
                "total_value": round(tons_co2 * info["price"], 2),
            }

        return {
            "status": "ok",
            "data": {
                "tons_co2": round(tons_co2, 2),
                "price_per_ton": round(price_per_ton, 2),
                "total_value": round(value, 2),
                "market_comparison": market_comparison,
                "note": "Carbon credit prices are highly variable. EU ETS is the most liquid compliance market. Voluntary market prices depend on project quality and vintage.",
            },
            "timestamp": datetime.now(timezone.utc).isoformat(),
        }
    except Exception as exc:
        return {
            "status": "error",
            "data": {"error": str(exc)},
            "timestamp": datetime.now(timezone.utc).isoformat(),
        }
