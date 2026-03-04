"""Calculate the Calmar ratio (annualized return / max drawdown).

MCP Tool Name: calmar_ratio_calculator
"""
from __future__ import annotations

from datetime import datetime, timezone
from typing import Any

TOOL_META: dict[str, Any] = {
    "name": "calmar_ratio_calculator",
    "description": (
        "Calculates the Calmar ratio, comparing annualized return to maximum "
        "drawdown as a measure of risk-adjusted performance."
    ),
    "inputSchema": {
        "type": "object",
        "properties": {
            "annual_return": {
                "type": "number",
                "description": "Annualized return (decimal, e.g. 0.12 for 12%).",
            },
            "max_drawdown": {
                "type": "number",
                "description": "Maximum drawdown as a positive decimal (e.g. 0.20 for 20%).",
            },
        },
        "required": ["annual_return", "max_drawdown"],
    },
}


def calmar_ratio_calculator(
    annual_return: float, max_drawdown: float
) -> dict[str, Any]:
    """Calculate the Calmar ratio."""
    try:
        annual_return = float(annual_return)
        max_drawdown = float(max_drawdown)

        if abs(max_drawdown) == 0:
            raise ValueError("max_drawdown must not be zero.")

        calmar = annual_return / abs(max_drawdown)

        return {
            "status": "ok",
            "data": {
                "calmar_ratio": round(calmar, 6),
            },
            "timestamp": datetime.now(timezone.utc).isoformat(),
        }
    except Exception as exc:
        return {
            "status": "error",
            "data": {"error": str(exc)},
            "timestamp": datetime.now(timezone.utc).isoformat(),
        }
