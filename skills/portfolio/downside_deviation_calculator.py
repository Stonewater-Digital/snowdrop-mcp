"""Calculate downside deviation below a minimum acceptable return.

MCP Tool Name: downside_deviation_calculator
"""
from __future__ import annotations

import math
from datetime import datetime, timezone
from typing import Any

TOOL_META: dict[str, Any] = {
    "name": "downside_deviation_calculator",
    "description": (
        "Calculates downside deviation, measuring the volatility of returns "
        "below a minimum acceptable return (MAR) threshold."
    ),
    "inputSchema": {
        "type": "object",
        "properties": {
            "returns": {
                "type": "array",
                "items": {"type": "number"},
                "description": "List of periodic returns as decimals.",
            },
            "mar": {
                "type": "number",
                "description": "Minimum acceptable return threshold (default 0.0).",
            },
        },
        "required": ["returns"],
    },
}


def downside_deviation_calculator(
    returns: list[float], mar: float = 0.0
) -> dict[str, Any]:
    """Calculate downside deviation."""
    try:
        returns = [float(r) for r in returns]
        mar = float(mar)

        if len(returns) == 0:
            raise ValueError("returns must not be empty.")

        downside_diffs = [min(r - mar, 0) ** 2 for r in returns]
        dd = math.sqrt(sum(downside_diffs) / len(downside_diffs))

        return {
            "status": "ok",
            "data": {
                "downside_deviation": round(dd, 6),
                "mar": mar,
                "n_periods": len(returns),
                "n_below_mar": sum(1 for r in returns if r < mar),
            },
            "timestamp": datetime.now(timezone.utc).isoformat(),
        }
    except Exception as exc:
        return {
            "status": "error",
            "data": {"error": str(exc)},
            "timestamp": datetime.now(timezone.utc).isoformat(),
        }
