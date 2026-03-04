"""Calculate FX swap points from interest rate differential.

MCP Tool Name: swap_points_calculator
"""
from __future__ import annotations
from datetime import datetime, timezone
from typing import Any

TOOL_META: dict[str, Any] = {
    "name": "swap_points_calculator",
    "description": "Calculate FX swap points (forward points) from spot rate and interest rate differential. Swap points = forward - spot, expressed in pips.",
    "inputSchema": {
        "type": "object",
        "properties": {
            "spot_rate": {
                "type": "number",
                "description": "Current spot exchange rate.",
            },
            "domestic_rate": {
                "type": "number",
                "description": "Domestic (quote currency) annualized interest rate as a decimal.",
            },
            "foreign_rate": {
                "type": "number",
                "description": "Foreign (base currency) annualized interest rate as a decimal.",
            },
            "days": {
                "type": "integer",
                "description": "Swap period in days.",
                "default": 90,
            },
        },
        "required": ["spot_rate", "domestic_rate", "foreign_rate"],
    },
}


def swap_points_calculator(
    spot_rate: float,
    domestic_rate: float,
    foreign_rate: float,
    days: int = 90,
) -> dict[str, Any]:
    """Calculate FX swap points."""
    try:
        if spot_rate <= 0:
            return {
                "status": "error",
                "data": {"error": "spot_rate must be positive."},
                "timestamp": datetime.now(timezone.utc).isoformat(),
            }
        if days <= 0:
            return {
                "status": "error",
                "data": {"error": "days must be positive."},
                "timestamp": datetime.now(timezone.utc).isoformat(),
            }

        denom = 1 + foreign_rate * days / 360
        if denom == 0:
            return {
                "status": "error",
                "data": {"error": "Invalid foreign rate creates zero denominator."},
                "timestamp": datetime.now(timezone.utc).isoformat(),
            }

        forward = spot_rate * (1 + domestic_rate * days / 360) / denom
        swap_points = forward - spot_rate

        # Convert to pips (0.0001 for most, 0.01 for JPY-related)
        # Heuristic: if spot > 10, likely JPY pair
        pip_size = 0.01 if spot_rate > 10 else 0.0001
        swap_pips = swap_points / pip_size

        return {
            "status": "ok",
            "data": {
                "spot_rate": spot_rate,
                "forward_rate": round(forward, 6),
                "swap_points_decimal": round(swap_points, 6),
                "swap_points_pips": round(swap_pips, 2),
                "pip_size_used": pip_size,
                "days": days,
                "rate_differential_pct": round((domestic_rate - foreign_rate) * 100, 4),
                "note": "Positive swap points = forward premium (domestic rate > foreign rate).",
            },
            "timestamp": datetime.now(timezone.utc).isoformat(),
        }
    except Exception as exc:
        return {
            "status": "error",
            "data": {"error": str(exc)},
            "timestamp": datetime.now(timezone.utc).isoformat(),
        }
