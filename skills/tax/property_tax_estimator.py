"""Estimate property tax from assessed value and mill rate.

MCP Tool Name: property_tax_estimator
"""
from __future__ import annotations
from datetime import datetime, timezone
from typing import Any

TOOL_META: dict[str, Any] = {
    "name": "property_tax_estimator",
    "description": "Estimate annual and monthly property tax from assessed value, mill rate, and optional homestead exemption.",
    "inputSchema": {
        "type": "object",
        "properties": {
            "assessed_value": {
                "type": "number",
                "description": "Assessed property value in USD.",
            },
            "mill_rate": {
                "type": "number",
                "description": "Mill rate (tax per $1,000 of assessed value). E.g. 25 means $25 per $1,000.",
            },
            "homestead_exemption": {
                "type": "number",
                "description": "Homestead exemption amount in USD.",
                "default": 0,
            },
        },
        "required": ["assessed_value", "mill_rate"],
    },
}


def property_tax_estimator(
    assessed_value: float,
    mill_rate: float,
    homestead_exemption: float = 0,
) -> dict[str, Any]:
    """Estimate property tax."""
    try:
        if assessed_value < 0 or mill_rate < 0 or homestead_exemption < 0:
            return {
                "status": "error",
                "data": {"error": "All values must be non-negative."},
                "timestamp": datetime.now(timezone.utc).isoformat(),
            }

        taxable_value = max(assessed_value - homestead_exemption, 0)
        annual_tax = taxable_value * mill_rate / 1000
        monthly_tax = annual_tax / 12
        effective_rate = (annual_tax / assessed_value * 100) if assessed_value > 0 else 0.0

        return {
            "status": "ok",
            "data": {
                "assessed_value": round(assessed_value, 2),
                "homestead_exemption": round(homestead_exemption, 2),
                "taxable_value": round(taxable_value, 2),
                "mill_rate": round(mill_rate, 4),
                "annual_tax": round(annual_tax, 2),
                "monthly_tax": round(monthly_tax, 2),
                "effective_rate_pct": round(effective_rate, 3),
            },
            "timestamp": datetime.now(timezone.utc).isoformat(),
        }
    except Exception as exc:
        return {
            "status": "error",
            "data": {"error": str(exc)},
            "timestamp": datetime.now(timezone.utc).isoformat(),
        }
