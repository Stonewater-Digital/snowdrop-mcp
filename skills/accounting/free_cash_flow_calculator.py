"""Calculate free cash flow from operating cash flow and capital expenditures.

MCP Tool Name: free_cash_flow_calculator
"""
from __future__ import annotations

from datetime import datetime, timezone
from typing import Any

TOOL_META: dict[str, Any] = {
    "name": "free_cash_flow_calculator",
    "description": (
        "Calculates free cash flow (FCF = operating cash flow - capital expenditures), "
        "measuring cash available for distribution to investors."
    ),
    "inputSchema": {
        "type": "object",
        "properties": {
            "operating_cash_flow": {
                "type": "number",
                "description": "Cash flow from operations.",
            },
            "capital_expenditures": {
                "type": "number",
                "description": "Capital expenditures (positive number).",
            },
        },
        "required": ["operating_cash_flow", "capital_expenditures"],
    },
}


def free_cash_flow_calculator(
    operating_cash_flow: float, capital_expenditures: float
) -> dict[str, Any]:
    """Calculate free cash flow."""
    try:
        operating_cash_flow = float(operating_cash_flow)
        capital_expenditures = float(capital_expenditures)

        fcf = operating_cash_flow - capital_expenditures

        return {
            "status": "ok",
            "data": {
                "free_cash_flow": round(fcf, 2),
            },
            "timestamp": datetime.now(timezone.utc).isoformat(),
        }
    except Exception as exc:
        return {
            "status": "error",
            "data": {"error": str(exc)},
            "timestamp": datetime.now(timezone.utc).isoformat(),
        }
