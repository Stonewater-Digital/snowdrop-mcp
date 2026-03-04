"""Convert between energy units (BTU, kWh, MJ, therms, gallons of oil, cubic feet of natural gas).

MCP Tool Name: btu_conversion_calculator
"""
from __future__ import annotations
from datetime import datetime, timezone
from typing import Any

TOOL_META: dict[str, Any] = {
    "name": "btu_conversion_calculator",
    "description": "Convert between energy units: BTU, kWh, MJ, therms, gallons_oil, and cubic_feet_gas.",
    "inputSchema": {
        "type": "object",
        "properties": {
            "amount": {
                "type": "number",
                "description": "Amount of energy to convert.",
            },
            "from_unit": {
                "type": "string",
                "description": "Source energy unit.",
                "enum": ["btu", "kwh", "mj", "therms", "gallons_oil", "cubic_feet_gas"],
            },
            "to_unit": {
                "type": "string",
                "description": "Target energy unit.",
                "enum": ["btu", "kwh", "mj", "therms", "gallons_oil", "cubic_feet_gas"],
            },
        },
        "required": ["amount", "from_unit", "to_unit"],
    },
}

# Conversion factors to BTU (1 unit = X BTU)
_TO_BTU: dict[str, float] = {
    "btu": 1.0,
    "kwh": 3412.14,
    "mj": 947.817,
    "therms": 100000.0,
    "gallons_oil": 138500.0,       # No. 2 heating oil approx
    "cubic_feet_gas": 1037.0,      # Natural gas approx
}


def btu_conversion_calculator(
    amount: float,
    from_unit: str,
    to_unit: str,
) -> dict[str, Any]:
    """Convert between energy units."""
    try:
        from_unit = from_unit.lower().strip()
        to_unit = to_unit.lower().strip()

        if from_unit not in _TO_BTU:
            return {
                "status": "error",
                "data": {"error": f"Invalid from_unit '{from_unit}'. Supported: {list(_TO_BTU.keys())}"},
                "timestamp": datetime.now(timezone.utc).isoformat(),
            }
        if to_unit not in _TO_BTU:
            return {
                "status": "error",
                "data": {"error": f"Invalid to_unit '{to_unit}'. Supported: {list(_TO_BTU.keys())}"},
                "timestamp": datetime.now(timezone.utc).isoformat(),
            }

        # Convert to BTU first, then to target
        btu_amount = amount * _TO_BTU[from_unit]
        converted = btu_amount / _TO_BTU[to_unit]
        conversion_factor = _TO_BTU[from_unit] / _TO_BTU[to_unit]

        return {
            "status": "ok",
            "data": {
                "original_amount": amount,
                "from_unit": from_unit,
                "to_unit": to_unit,
                "converted_amount": round(converted, 6),
                "conversion_factor": round(conversion_factor, 6),
                "btu_equivalent": round(btu_amount, 2),
            },
            "timestamp": datetime.now(timezone.utc).isoformat(),
        }
    except Exception as exc:
        return {
            "status": "error",
            "data": {"error": str(exc)},
            "timestamp": datetime.now(timezone.utc).isoformat(),
        }
