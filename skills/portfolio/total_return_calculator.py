"""Calculate total return including price change and dividends.

MCP Tool Name: total_return_calculator
"""
from __future__ import annotations

from datetime import datetime, timezone
from typing import Any

TOOL_META: dict[str, Any] = {
    "name": "total_return_calculator",
    "description": (
        "Calculates total return as a percentage, including both capital "
        "appreciation and dividend income."
    ),
    "inputSchema": {
        "type": "object",
        "properties": {
            "begin_value": {
                "type": "number",
                "description": "Beginning investment value.",
            },
            "end_value": {
                "type": "number",
                "description": "Ending investment value.",
            },
            "dividends": {
                "type": "number",
                "description": "Total dividends received (default 0).",
            },
        },
        "required": ["begin_value", "end_value"],
    },
}


def total_return_calculator(
    begin_value: float, end_value: float, dividends: float = 0.0
) -> dict[str, Any]:
    """Calculate total return."""
    try:
        begin_value = float(begin_value)
        end_value = float(end_value)
        dividends = float(dividends)

        if begin_value == 0:
            raise ValueError("begin_value must not be zero.")

        total_return = ((end_value + dividends - begin_value) / begin_value) * 100

        return {
            "status": "ok",
            "data": {
                "total_return_pct": round(total_return, 4),
                "capital_gain": round(end_value - begin_value, 2),
                "dividends": round(dividends, 2),
            },
            "timestamp": datetime.now(timezone.utc).isoformat(),
        }
    except Exception as exc:
        return {
            "status": "error",
            "data": {"error": str(exc)},
            "timestamp": datetime.now(timezone.utc).isoformat(),
        }
