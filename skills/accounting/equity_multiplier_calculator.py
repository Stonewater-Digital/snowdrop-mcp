"""Calculate the equity multiplier measuring financial leverage.

MCP Tool Name: equity_multiplier_calculator
"""
from __future__ import annotations

from datetime import datetime, timezone
from typing import Any

TOOL_META: dict[str, Any] = {
    "name": "equity_multiplier_calculator",
    "description": (
        "Calculates the equity multiplier (total assets / total equity), a measure "
        "of financial leverage used in DuPont analysis."
    ),
    "inputSchema": {
        "type": "object",
        "properties": {
            "total_assets": {
                "type": "number",
                "description": "Total assets.",
            },
            "total_equity": {
                "type": "number",
                "description": "Total shareholders equity.",
            },
        },
        "required": ["total_assets", "total_equity"],
    },
}


def equity_multiplier_calculator(
    total_assets: float, total_equity: float
) -> dict[str, Any]:
    """Calculate the equity multiplier."""
    try:
        total_assets = float(total_assets)
        total_equity = float(total_equity)

        if total_equity == 0:
            raise ValueError("total_equity must not be zero.")

        multiplier = total_assets / total_equity

        return {
            "status": "ok",
            "data": {
                "equity_multiplier": round(multiplier, 4),
            },
            "timestamp": datetime.now(timezone.utc).isoformat(),
        }
    except Exception as exc:
        return {
            "status": "error",
            "data": {"error": str(exc)},
            "timestamp": datetime.now(timezone.utc).isoformat(),
        }
