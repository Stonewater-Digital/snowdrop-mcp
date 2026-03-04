"""Calculate capitalization rate for a real estate investment.

MCP Tool Name: cap_rate_calculator
"""
from __future__ import annotations
from datetime import datetime, timezone
from typing import Any

TOOL_META: dict[str, Any] = {
    "name": "cap_rate_calculator",
    "description": "Calculate capitalization rate (cap rate) from net operating income and property value. Cap rate = NOI / Property Value.",
    "inputSchema": {
        "type": "object",
        "properties": {
            "net_operating_income": {
                "type": "number",
                "description": "Annual net operating income in USD.",
            },
            "property_value": {
                "type": "number",
                "description": "Current property value or purchase price in USD.",
            },
        },
        "required": ["net_operating_income", "property_value"],
    },
}


def cap_rate_calculator(
    net_operating_income: float,
    property_value: float,
) -> dict[str, Any]:
    """Calculate capitalization rate."""
    try:
        if property_value <= 0:
            return {
                "status": "error",
                "data": {"error": "property_value must be positive."},
                "timestamp": datetime.now(timezone.utc).isoformat(),
            }

        cap_rate = net_operating_income / property_value * 100

        # General interpretation
        if cap_rate < 4:
            interpretation = "Low cap rate — typically core/prime assets in major markets. Lower risk, lower return."
        elif cap_rate < 7:
            interpretation = "Moderate cap rate — balanced risk/return profile."
        elif cap_rate < 10:
            interpretation = "Higher cap rate — may indicate value-add opportunity or higher risk."
        else:
            interpretation = "Very high cap rate — may signal distressed asset, high risk, or secondary market."

        return {
            "status": "ok",
            "data": {
                "net_operating_income": round(net_operating_income, 2),
                "property_value": round(property_value, 2),
                "cap_rate_pct": round(cap_rate, 3),
                "interpretation": interpretation,
            },
            "timestamp": datetime.now(timezone.utc).isoformat(),
        }
    except Exception as exc:
        return {
            "status": "error",
            "data": {"error": str(exc)},
            "timestamp": datetime.now(timezone.utc).isoformat(),
        }
