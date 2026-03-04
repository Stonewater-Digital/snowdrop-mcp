"""Calculate weighted portfolio return from asset weights and returns.

MCP Tool Name: portfolio_return_calculator
"""
from __future__ import annotations

from datetime import datetime, timezone
from typing import Any

TOOL_META: dict[str, Any] = {
    "name": "portfolio_return_calculator",
    "description": (
        "Calculates the weighted portfolio return as the sum of weight * return "
        "for each asset."
    ),
    "inputSchema": {
        "type": "object",
        "properties": {
            "weights": {
                "type": "array",
                "items": {"type": "number"},
                "description": "List of asset weights (should sum to 1).",
            },
            "returns": {
                "type": "array",
                "items": {"type": "number"},
                "description": "List of asset returns (same length as weights).",
            },
        },
        "required": ["weights", "returns"],
    },
}


def portfolio_return_calculator(
    weights: list[float], returns: list[float]
) -> dict[str, Any]:
    """Calculate weighted portfolio return."""
    try:
        weights = [float(w) for w in weights]
        returns = [float(r) for r in returns]

        if len(weights) != len(returns):
            raise ValueError("weights and returns must have the same length.")
        if len(weights) == 0:
            raise ValueError("Must have at least one asset.")

        portfolio_return = sum(w * r for w, r in zip(weights, returns))

        return {
            "status": "ok",
            "data": {
                "portfolio_return": round(portfolio_return, 8),
                "portfolio_return_pct": round(portfolio_return * 100, 4),
                "weight_sum": round(sum(weights), 6),
            },
            "timestamp": datetime.now(timezone.utc).isoformat(),
        }
    except Exception as exc:
        return {
            "status": "error",
            "data": {"error": str(exc)},
            "timestamp": datetime.now(timezone.utc).isoformat(),
        }
