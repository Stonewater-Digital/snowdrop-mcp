"""Calculate the Omega ratio comparing gains to losses relative to a threshold.

MCP Tool Name: omega_ratio_calculator
"""
from __future__ import annotations

from datetime import datetime, timezone
from typing import Any

TOOL_META: dict[str, Any] = {
    "name": "omega_ratio_calculator",
    "description": (
        "Calculates the Omega ratio, the ratio of cumulative gains above a "
        "threshold to cumulative losses below it."
    ),
    "inputSchema": {
        "type": "object",
        "properties": {
            "returns": {
                "type": "array",
                "items": {"type": "number"},
                "description": "List of periodic returns as decimals.",
            },
            "threshold": {
                "type": "number",
                "description": "Minimum acceptable return threshold (default 0.0).",
            },
        },
        "required": ["returns"],
    },
}


def omega_ratio_calculator(
    returns: list[float], threshold: float = 0.0
) -> dict[str, Any]:
    """Calculate the Omega ratio."""
    try:
        returns = [float(r) for r in returns]
        threshold = float(threshold)

        if len(returns) == 0:
            raise ValueError("returns must not be empty.")

        gains = sum(max(r - threshold, 0) for r in returns)
        losses = sum(max(threshold - r, 0) for r in returns)

        if losses == 0:
            if gains == 0:
                raise ValueError("No gains or losses relative to threshold.")
            omega = float("inf")
        else:
            omega = gains / losses

        return {
            "status": "ok",
            "data": {
                "omega_ratio": round(omega, 6) if omega != float("inf") else "inf",
                "total_gains": round(gains, 6),
                "total_losses": round(losses, 6),
                "threshold": threshold,
            },
            "timestamp": datetime.now(timezone.utc).isoformat(),
        }
    except Exception as exc:
        return {
            "status": "error",
            "data": {"error": str(exc)},
            "timestamp": datetime.now(timezone.utc).isoformat(),
        }
