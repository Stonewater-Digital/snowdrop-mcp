"""Calculate the operating cash flow ratio.

MCP Tool Name: operating_cash_flow_ratio_calculator
"""
from __future__ import annotations

from datetime import datetime, timezone
from typing import Any

TOOL_META: dict[str, Any] = {
    "name": "operating_cash_flow_ratio_calculator",
    "description": (
        "Calculates the operating cash flow ratio (OCF / current liabilities), "
        "measuring a company's ability to cover short-term obligations with cash from operations."
    ),
    "inputSchema": {
        "type": "object",
        "properties": {
            "operating_cash_flow": {
                "type": "number",
                "description": "Cash flow from operations.",
            },
            "current_liabilities": {
                "type": "number",
                "description": "Total current liabilities.",
            },
        },
        "required": ["operating_cash_flow", "current_liabilities"],
    },
}


def operating_cash_flow_ratio_calculator(
    operating_cash_flow: float, current_liabilities: float
) -> dict[str, Any]:
    """Calculate the operating cash flow ratio."""
    try:
        operating_cash_flow = float(operating_cash_flow)
        current_liabilities = float(current_liabilities)

        if current_liabilities == 0:
            raise ValueError("current_liabilities must not be zero.")

        ratio = operating_cash_flow / current_liabilities

        return {
            "status": "ok",
            "data": {
                "operating_cash_flow_ratio": round(ratio, 4),
            },
            "timestamp": datetime.now(timezone.utc).isoformat(),
        }
    except Exception as exc:
        return {
            "status": "error",
            "data": {"error": str(exc)},
            "timestamp": datetime.now(timezone.utc).isoformat(),
        }
