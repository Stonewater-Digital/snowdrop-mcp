"""Calculate property ROI including income and appreciation.

MCP Tool Name: property_roi_calculator
"""
from __future__ import annotations
from datetime import datetime, timezone
from typing import Any

TOOL_META: dict[str, Any] = {
    "name": "property_roi_calculator",
    "description": "Calculate property return on investment from annual income, expenses, current value, and purchase price. Includes cash flow ROI and total ROI with appreciation.",
    "inputSchema": {
        "type": "object",
        "properties": {
            "annual_income": {
                "type": "number",
                "description": "Total annual income from the property in USD.",
            },
            "annual_expenses": {
                "type": "number",
                "description": "Total annual expenses (taxes, insurance, maintenance, management, debt service) in USD.",
            },
            "property_value": {
                "type": "number",
                "description": "Current market value of the property in USD.",
            },
            "purchase_price": {
                "type": "number",
                "description": "Original purchase price in USD.",
            },
        },
        "required": ["annual_income", "annual_expenses", "property_value", "purchase_price"],
    },
}


def property_roi_calculator(
    annual_income: float,
    annual_expenses: float,
    property_value: float,
    purchase_price: float,
) -> dict[str, Any]:
    """Calculate property ROI."""
    try:
        if purchase_price <= 0:
            return {
                "status": "error",
                "data": {"error": "purchase_price must be positive."},
                "timestamp": datetime.now(timezone.utc).isoformat(),
            }

        net_income = annual_income - annual_expenses
        cash_flow_roi = net_income / purchase_price * 100

        appreciation = property_value - purchase_price
        appreciation_pct = appreciation / purchase_price * 100

        total_annual_return = net_income + appreciation
        total_roi = total_annual_return / purchase_price * 100

        return {
            "status": "ok",
            "data": {
                "annual_income": round(annual_income, 2),
                "annual_expenses": round(annual_expenses, 2),
                "net_annual_income": round(net_income, 2),
                "monthly_net_income": round(net_income / 12, 2),
                "purchase_price": round(purchase_price, 2),
                "current_value": round(property_value, 2),
                "appreciation": round(appreciation, 2),
                "appreciation_pct": round(appreciation_pct, 2),
                "cash_flow_roi_pct": round(cash_flow_roi, 2),
                "total_roi_pct": round(total_roi, 2),
            },
            "timestamp": datetime.now(timezone.utc).isoformat(),
        }
    except Exception as exc:
        return {
            "status": "error",
            "data": {"error": str(exc)},
            "timestamp": datetime.now(timezone.utc).isoformat(),
        }
