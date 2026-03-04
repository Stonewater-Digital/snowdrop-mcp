"""Calculate the debt-to-equity ratio measuring financial leverage.

MCP Tool Name: debt_to_equity_calculator
"""
from __future__ import annotations

from datetime import datetime, timezone
from typing import Any

TOOL_META: dict[str, Any] = {
    "name": "debt_to_equity_calculator",
    "description": (
        "Calculates the debt-to-equity ratio, measuring how much debt a company "
        "uses relative to shareholder equity."
    ),
    "inputSchema": {
        "type": "object",
        "properties": {
            "total_debt": {
                "type": "number",
                "description": "Total debt (short-term + long-term).",
            },
            "total_equity": {
                "type": "number",
                "description": "Total shareholders equity.",
            },
        },
        "required": ["total_debt", "total_equity"],
    },
}


def debt_to_equity_calculator(
    total_debt: float, total_equity: float
) -> dict[str, Any]:
    """Calculate the debt-to-equity ratio."""
    try:
        total_debt = float(total_debt)
        total_equity = float(total_equity)

        if total_equity == 0:
            raise ValueError("total_equity must not be zero.")

        ratio = total_debt / total_equity

        return {
            "status": "ok",
            "data": {
                "debt_to_equity_ratio": round(ratio, 4),
            },
            "timestamp": datetime.now(timezone.utc).isoformat(),
        }
    except Exception as exc:
        return {
            "status": "error",
            "data": {"error": str(exc)},
            "timestamp": datetime.now(timezone.utc).isoformat(),
        }
