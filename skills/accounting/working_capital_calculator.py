"""Calculate working capital and current ratio from balance sheet items.

MCP Tool Name: working_capital_calculator
"""
from __future__ import annotations

from datetime import datetime, timezone
from typing import Any

TOOL_META: dict[str, Any] = {
    "name": "working_capital_calculator",
    "description": (
        "Calculates net working capital and the current ratio to assess "
        "short-term liquidity."
    ),
    "inputSchema": {
        "type": "object",
        "properties": {
            "current_assets": {
                "type": "number",
                "description": "Total current assets.",
            },
            "current_liabilities": {
                "type": "number",
                "description": "Total current liabilities.",
            },
        },
        "required": ["current_assets", "current_liabilities"],
    },
}


def working_capital_calculator(
    current_assets: float, current_liabilities: float
) -> dict[str, Any]:
    """Calculate working capital and current ratio."""
    try:
        current_assets = float(current_assets)
        current_liabilities = float(current_liabilities)

        working_capital = current_assets - current_liabilities

        if current_liabilities == 0:
            ratio = float("inf") if current_assets > 0 else 0.0
        else:
            ratio = current_assets / current_liabilities

        return {
            "status": "ok",
            "data": {
                "working_capital": round(working_capital, 2),
                "current_ratio": round(ratio, 4),
            },
            "timestamp": datetime.now(timezone.utc).isoformat(),
        }
    except Exception as exc:
        return {
            "status": "error",
            "data": {"error": str(exc)},
            "timestamp": datetime.now(timezone.utc).isoformat(),
        }
