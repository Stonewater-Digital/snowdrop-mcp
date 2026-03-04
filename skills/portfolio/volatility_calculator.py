"""Calculate historical volatility from a return series.

MCP Tool Name: volatility_calculator
"""
from __future__ import annotations

import math
from datetime import datetime, timezone
from typing import Any

TOOL_META: dict[str, Any] = {
    "name": "volatility_calculator",
    "description": (
        "Calculates historical volatility (standard deviation of returns), "
        "optionally annualized using sqrt(252) for daily data."
    ),
    "inputSchema": {
        "type": "object",
        "properties": {
            "returns": {
                "type": "array",
                "items": {"type": "number"},
                "description": "List of periodic returns as decimals.",
            },
            "annualize": {
                "type": "boolean",
                "description": "Whether to annualize using sqrt(252) (default true).",
            },
        },
        "required": ["returns"],
    },
}


def volatility_calculator(
    returns: list[float], annualize: bool = True
) -> dict[str, Any]:
    """Calculate historical volatility."""
    try:
        import statistics

        returns = [float(r) for r in returns]

        if len(returns) < 2:
            raise ValueError("returns must contain at least 2 values.")

        std = statistics.stdev(returns)
        factor = math.sqrt(252) if annualize else 1.0
        volatility = std * factor

        return {
            "status": "ok",
            "data": {
                "volatility": round(volatility, 6),
                "periodic_std": round(std, 6),
                "annualized": annualize,
            },
            "timestamp": datetime.now(timezone.utc).isoformat(),
        }
    except Exception as exc:
        return {
            "status": "error",
            "data": {"error": str(exc)},
            "timestamp": datetime.now(timezone.utc).isoformat(),
        }
