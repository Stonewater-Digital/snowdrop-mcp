"""Calculate money market yield (MMY) for a discount instrument.

MCP Tool Name: money_market_yield_calculator
"""
from __future__ import annotations
from datetime import datetime, timezone
from typing import Any

TOOL_META: dict[str, Any] = {
    "name": "money_market_yield_calculator",
    "description": "Calculate the money market yield (MMY) for a discount instrument. MMY = ((face - price) / price) * (360 / days_to_maturity).",
    "inputSchema": {
        "type": "object",
        "properties": {
            "face_value": {
                "type": "number",
                "description": "Face (par) value of the instrument.",
            },
            "purchase_price": {
                "type": "number",
                "description": "Purchase price paid for the instrument.",
            },
            "days_to_maturity": {
                "type": "integer",
                "description": "Number of days until maturity.",
            },
        },
        "required": ["face_value", "purchase_price", "days_to_maturity"],
    },
}


def money_market_yield_calculator(
    face_value: float, purchase_price: float, days_to_maturity: int
) -> dict[str, Any]:
    """Calculate money market yield for a discount instrument."""
    try:
        if purchase_price <= 0:
            return {
                "status": "error",
                "data": {"error": "purchase_price must be positive."},
                "timestamp": datetime.now(timezone.utc).isoformat(),
            }
        if days_to_maturity <= 0:
            return {
                "status": "error",
                "data": {"error": "days_to_maturity must be positive."},
                "timestamp": datetime.now(timezone.utc).isoformat(),
            }

        discount = face_value - purchase_price
        mmy = (discount / purchase_price) * (360 / days_to_maturity)

        return {
            "status": "ok",
            "data": {
                "face_value": face_value,
                "purchase_price": purchase_price,
                "days_to_maturity": days_to_maturity,
                "discount": round(discount, 2),
                "money_market_yield": round(mmy, 8),
                "money_market_yield_pct": round(mmy * 100, 4),
            },
            "timestamp": datetime.now(timezone.utc).isoformat(),
        }
    except Exception as exc:
        return {
            "status": "error",
            "data": {"error": str(exc)},
            "timestamp": datetime.now(timezone.utc).isoformat(),
        }
