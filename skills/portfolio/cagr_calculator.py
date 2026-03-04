"""Calculate compound annual growth rate (CAGR) from beginning and ending values.

MCP Tool Name: cagr_calculator
"""
from __future__ import annotations

from datetime import datetime, timezone
from typing import Any

TOOL_META: dict[str, Any] = {
    "name": "cagr_calculator",
    "description": (
        "Calculates the compound annual growth rate (CAGR), the geometric average "
        "annual return between a beginning and ending value."
    ),
    "inputSchema": {
        "type": "object",
        "properties": {
            "begin_value": {
                "type": "number",
                "description": "Beginning value of the investment.",
            },
            "end_value": {
                "type": "number",
                "description": "Ending value of the investment.",
            },
            "years": {
                "type": "number",
                "description": "Number of years over which growth occurred.",
            },
        },
        "required": ["begin_value", "end_value", "years"],
    },
}


def cagr_calculator(
    begin_value: float, end_value: float, years: float
) -> dict[str, Any]:
    """Calculate CAGR."""
    try:
        begin_value = float(begin_value)
        end_value = float(end_value)
        years = float(years)

        if begin_value <= 0:
            raise ValueError("begin_value must be greater than zero.")
        if end_value < 0:
            raise ValueError("end_value must not be negative.")
        if years <= 0:
            raise ValueError("years must be greater than zero.")

        cagr = (end_value / begin_value) ** (1 / years) - 1

        return {
            "status": "ok",
            "data": {
                "cagr_decimal": round(cagr, 6),
                "cagr_pct": round(cagr * 100, 4),
            },
            "timestamp": datetime.now(timezone.utc).isoformat(),
        }
    except Exception as exc:
        return {
            "status": "error",
            "data": {"error": str(exc)},
            "timestamp": datetime.now(timezone.utc).isoformat(),
        }
