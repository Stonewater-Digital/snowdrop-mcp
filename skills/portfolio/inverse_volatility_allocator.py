"""Allocate a portfolio using inverse-volatility weighting.

MCP Tool Name: inverse_volatility_allocator
"""
from __future__ import annotations

from datetime import datetime, timezone
from typing import Any

TOOL_META: dict[str, Any] = {
    "name": "inverse_volatility_allocator",
    "description": (
        "Allocates a portfolio using inverse-volatility weighting, giving more "
        "weight to lower-volatility assets."
    ),
    "inputSchema": {
        "type": "object",
        "properties": {
            "volatilities": {
                "type": "array",
                "items": {"type": "number"},
                "description": "List of asset volatilities (must all be > 0).",
            },
            "total_value": {
                "type": "number",
                "description": "Total portfolio value to allocate (default 10000).",
            },
        },
        "required": ["volatilities"],
    },
}


def inverse_volatility_allocator(
    volatilities: list[float], total_value: float = 10000.0
) -> dict[str, Any]:
    """Allocate portfolio using inverse-volatility weighting."""
    try:
        volatilities = [float(v) for v in volatilities]
        total_value = float(total_value)

        if len(volatilities) == 0:
            raise ValueError("volatilities must not be empty.")
        if any(v <= 0 for v in volatilities):
            raise ValueError("All volatilities must be greater than zero.")

        inv_vols = [1.0 / v for v in volatilities]
        total_inv = sum(inv_vols)
        weights = [iv / total_inv for iv in inv_vols]

        allocations = [
            {
                "asset": i + 1,
                "volatility": round(volatilities[i], 6),
                "weight": round(weights[i], 6),
                "value": round(weights[i] * total_value, 2),
            }
            for i in range(len(volatilities))
        ]

        return {
            "status": "ok",
            "data": {
                "total_value": total_value,
                "allocations": allocations,
            },
            "timestamp": datetime.now(timezone.utc).isoformat(),
        }
    except Exception as exc:
        return {
            "status": "error",
            "data": {"error": str(exc)},
            "timestamp": datetime.now(timezone.utc).isoformat(),
        }
