"""Calculate gross rent multiplier (GRM) for a property.

MCP Tool Name: gross_rent_multiplier_calculator
"""
from __future__ import annotations
from datetime import datetime, timezone
from typing import Any

TOOL_META: dict[str, Any] = {
    "name": "gross_rent_multiplier_calculator",
    "description": "Calculate gross rent multiplier (GRM = Property Price / Gross Annual Rent). Lower GRM generally indicates better value.",
    "inputSchema": {
        "type": "object",
        "properties": {
            "property_price": {
                "type": "number",
                "description": "Property purchase price in USD.",
            },
            "gross_annual_rent": {
                "type": "number",
                "description": "Gross annual rental income in USD.",
            },
        },
        "required": ["property_price", "gross_annual_rent"],
    },
}


def gross_rent_multiplier_calculator(
    property_price: float,
    gross_annual_rent: float,
) -> dict[str, Any]:
    """Calculate gross rent multiplier."""
    try:
        if gross_annual_rent <= 0:
            return {
                "status": "error",
                "data": {"error": "gross_annual_rent must be positive."},
                "timestamp": datetime.now(timezone.utc).isoformat(),
            }
        if property_price < 0:
            return {
                "status": "error",
                "data": {"error": "property_price must be non-negative."},
                "timestamp": datetime.now(timezone.utc).isoformat(),
            }

        grm = property_price / gross_annual_rent
        gross_monthly_rent = gross_annual_rent / 12
        price_per_monthly_rent = property_price / gross_monthly_rent

        return {
            "status": "ok",
            "data": {
                "property_price": round(property_price, 2),
                "gross_annual_rent": round(gross_annual_rent, 2),
                "gross_monthly_rent": round(gross_monthly_rent, 2),
                "grm": round(grm, 2),
                "price_per_monthly_rent": round(price_per_monthly_rent, 2),
                "note": "GRM ignores vacancy and expenses. Use cap rate for a more complete picture.",
            },
            "timestamp": datetime.now(timezone.utc).isoformat(),
        }
    except Exception as exc:
        return {
            "status": "error",
            "data": {"error": str(exc)},
            "timestamp": datetime.now(timezone.utc).isoformat(),
        }
