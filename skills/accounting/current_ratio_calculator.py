"""Calculate the current ratio with an interpretive assessment.

MCP Tool Name: current_ratio_calculator
"""
from __future__ import annotations

from datetime import datetime, timezone
from typing import Any

TOOL_META: dict[str, Any] = {
    "name": "current_ratio_calculator",
    "description": (
        "Calculates the current ratio (current assets / current liabilities) and "
        "provides an interpretive assessment of liquidity strength."
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


def current_ratio_calculator(
    current_assets: float, current_liabilities: float
) -> dict[str, Any]:
    """Calculate current ratio with interpretation."""
    try:
        current_assets = float(current_assets)
        current_liabilities = float(current_liabilities)

        if current_liabilities == 0:
            raise ValueError("current_liabilities must not be zero.")

        ratio = current_assets / current_liabilities

        if ratio >= 2.0:
            interpretation = "strong"
        elif ratio >= 1.5:
            interpretation = "healthy"
        elif ratio >= 1.0:
            interpretation = "adequate"
        else:
            interpretation = "weak"

        return {
            "status": "ok",
            "data": {
                "current_ratio": round(ratio, 4),
                "interpretation": interpretation,
            },
            "timestamp": datetime.now(timezone.utc).isoformat(),
        }
    except Exception as exc:
        return {
            "status": "error",
            "data": {"error": str(exc)},
            "timestamp": datetime.now(timezone.utc).isoformat(),
        }
