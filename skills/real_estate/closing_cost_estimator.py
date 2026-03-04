"""Estimate closing costs for a home purchase.

MCP Tool Name: closing_cost_estimator
"""
from __future__ import annotations
from datetime import datetime, timezone
from typing import Any

TOOL_META: dict[str, Any] = {
    "name": "closing_cost_estimator",
    "description": "Estimate closing costs for a home purchase (2-5% of price). Itemizes title insurance, appraisal, origination fees, escrow, recording fees, and more.",
    "inputSchema": {
        "type": "object",
        "properties": {
            "home_price": {
                "type": "number",
                "description": "Home purchase price in USD.",
            },
            "location": {
                "type": "string",
                "description": "General location indicator affecting cost range: low, average, or high.",
                "enum": ["low", "average", "high"],
                "default": "average",
            },
        },
        "required": ["home_price"],
    },
}

# Cost factors as percentage of home price or fixed amounts
_LOCATION_MULTIPLIERS = {
    "low": 0.85,     # ~2% total
    "average": 1.0,  # ~3% total
    "high": 1.25,    # ~4-5% total
}


def closing_cost_estimator(
    home_price: float,
    location: str = "average",
) -> dict[str, Any]:
    """Estimate closing costs."""
    try:
        if home_price <= 0:
            return {
                "status": "error",
                "data": {"error": "home_price must be positive."},
                "timestamp": datetime.now(timezone.utc).isoformat(),
            }

        location = location.lower().strip()
        if location not in _LOCATION_MULTIPLIERS:
            return {
                "status": "error",
                "data": {"error": f"Invalid location '{location}'. Must be low, average, or high."},
                "timestamp": datetime.now(timezone.utc).isoformat(),
            }

        mult = _LOCATION_MULTIPLIERS[location]

        # Itemized estimates
        origination_fee = home_price * 0.005 * mult  # ~0.5% loan origination
        appraisal = 500 * mult
        credit_report = 50
        title_search = 400 * mult
        title_insurance = home_price * 0.005 * mult  # ~0.5%
        survey = 500 * mult
        recording_fees = 300 * mult
        transfer_tax = home_price * 0.002 * mult  # varies widely
        attorney_fees = 1000 * mult
        escrow_prepaid = home_price * 0.004 * mult  # ~2-3 months taxes+insurance
        flood_cert = 25
        inspection = 450 * mult

        items = {
            "loan_origination_fee": round(origination_fee, 2),
            "appraisal": round(appraisal, 2),
            "credit_report": round(credit_report, 2),
            "title_search": round(title_search, 2),
            "title_insurance": round(title_insurance, 2),
            "survey": round(survey, 2),
            "recording_fees": round(recording_fees, 2),
            "transfer_tax": round(transfer_tax, 2),
            "attorney_fees": round(attorney_fees, 2),
            "escrow_prepaids": round(escrow_prepaid, 2),
            "flood_certification": round(flood_cert, 2),
            "home_inspection": round(inspection, 2),
        }

        total = sum(items.values())
        pct_of_price = total / home_price * 100

        return {
            "status": "ok",
            "data": {
                "home_price": round(home_price, 2),
                "location_cost_level": location,
                "itemized_costs": items,
                "total_closing_costs": round(total, 2),
                "pct_of_home_price": round(pct_of_price, 2),
                "note": "Actual costs vary by lender, state, and municipality. This is an estimate.",
            },
            "timestamp": datetime.now(timezone.utc).isoformat(),
        }
    except Exception as exc:
        return {
            "status": "error",
            "data": {"error": str(exc)},
            "timestamp": datetime.now(timezone.utc).isoformat(),
        }
