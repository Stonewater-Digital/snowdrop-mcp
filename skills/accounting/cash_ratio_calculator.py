"""Calculate the cash ratio, the most conservative liquidity measure.

MCP Tool Name: cash_ratio_calculator
"""
from __future__ import annotations

from datetime import datetime, timezone
from typing import Any

TOOL_META: dict[str, Any] = {
    "name": "cash_ratio_calculator",
    "description": (
        "Calculates the cash ratio using only cash and marketable securities, "
        "the most conservative short-term liquidity measure."
    ),
    "inputSchema": {
        "type": "object",
        "properties": {
            "cash": {
                "type": "number",
                "description": "Cash and cash equivalents.",
            },
            "marketable_securities": {
                "type": "number",
                "description": "Short-term marketable securities.",
            },
            "current_liabilities": {
                "type": "number",
                "description": "Total current liabilities.",
            },
        },
        "required": ["cash", "marketable_securities", "current_liabilities"],
    },
}


def cash_ratio_calculator(
    cash: float, marketable_securities: float, current_liabilities: float
) -> dict[str, Any]:
    """Calculate the cash ratio."""
    try:
        cash = float(cash)
        marketable_securities = float(marketable_securities)
        current_liabilities = float(current_liabilities)

        if current_liabilities == 0:
            raise ValueError("current_liabilities must not be zero.")

        ratio = (cash + marketable_securities) / current_liabilities

        return {
            "status": "ok",
            "data": {
                "cash_ratio": round(ratio, 4),
                "liquid_assets": round(cash + marketable_securities, 2),
            },
            "timestamp": datetime.now(timezone.utc).isoformat(),
        }
    except Exception as exc:
        return {
            "status": "error",
            "data": {"error": str(exc)},
            "timestamp": datetime.now(timezone.utc).isoformat(),
        }
