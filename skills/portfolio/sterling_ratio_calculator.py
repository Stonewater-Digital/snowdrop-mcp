"""Calculate the Sterling ratio (return over average max drawdown).

MCP Tool Name: sterling_ratio_calculator
"""
from __future__ import annotations

from datetime import datetime, timezone
from typing import Any

TOOL_META: dict[str, Any] = {
    "name": "sterling_ratio_calculator",
    "description": (
        "Calculates the Sterling ratio, comparing annualized return to average "
        "maximum drawdown plus a 10% buffer."
    ),
    "inputSchema": {
        "type": "object",
        "properties": {
            "annual_return": {
                "type": "number",
                "description": "Annualized return (decimal, e.g. 0.15 for 15%).",
            },
            "avg_max_drawdown": {
                "type": "number",
                "description": "Average maximum drawdown as a positive decimal.",
            },
        },
        "required": ["annual_return", "avg_max_drawdown"],
    },
}


def sterling_ratio_calculator(
    annual_return: float, avg_max_drawdown: float
) -> dict[str, Any]:
    """Calculate the Sterling ratio."""
    try:
        annual_return = float(annual_return)
        avg_max_drawdown = float(avg_max_drawdown)

        denominator = abs(avg_max_drawdown) + 0.1
        if denominator == 0:
            raise ValueError("Denominator (avg_max_drawdown + 0.1) must not be zero.")

        sterling = annual_return / denominator

        return {
            "status": "ok",
            "data": {
                "sterling_ratio": round(sterling, 6),
            },
            "timestamp": datetime.now(timezone.utc).isoformat(),
        }
    except Exception as exc:
        return {
            "status": "error",
            "data": {"error": str(exc)},
            "timestamp": datetime.now(timezone.utc).isoformat(),
        }
