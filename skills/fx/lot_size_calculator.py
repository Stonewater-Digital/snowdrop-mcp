"""Convert between forex lot sizes (standard, mini, micro).

MCP Tool Name: lot_size_calculator
"""
from __future__ import annotations
from datetime import datetime, timezone
from typing import Any

TOOL_META: dict[str, Any] = {
    "name": "lot_size_calculator",
    "description": "Convert a unit count into standard lots (100,000), mini lots (10,000), and micro lots (1,000).",
    "inputSchema": {
        "type": "object",
        "properties": {
            "units": {
                "type": "integer",
                "description": "Number of currency units.",
            },
        },
        "required": ["units"],
    },
}


def lot_size_calculator(
    units: int,
) -> dict[str, Any]:
    """Convert units to lot sizes."""
    try:
        if units < 0:
            return {
                "status": "error",
                "data": {"error": "units must be non-negative."},
                "timestamp": datetime.now(timezone.utc).isoformat(),
            }

        standard = units / 100000
        mini = units / 10000
        micro = units / 1000
        nano = units / 100

        return {
            "status": "ok",
            "data": {
                "units": units,
                "standard_lots": round(standard, 4),
                "mini_lots": round(mini, 4),
                "micro_lots": round(micro, 4),
                "nano_lots": round(nano, 4),
                "definitions": {
                    "standard_lot": "100,000 units",
                    "mini_lot": "10,000 units",
                    "micro_lot": "1,000 units",
                    "nano_lot": "100 units",
                },
            },
            "timestamp": datetime.now(timezone.utc).isoformat(),
        }
    except Exception as exc:
        return {
            "status": "error",
            "data": {"error": str(exc)},
            "timestamp": datetime.now(timezone.utc).isoformat(),
        }
