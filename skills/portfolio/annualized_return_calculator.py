"""Calculate annualized return from a total return over a given period.

MCP Tool Name: annualized_return_calculator
"""
from __future__ import annotations

from datetime import datetime, timezone
from typing import Any

TOOL_META: dict[str, Any] = {
    "name": "annualized_return_calculator",
    "description": (
        "Converts a cumulative total return percentage into an annualized return "
        "using geometric compounding."
    ),
    "inputSchema": {
        "type": "object",
        "properties": {
            "total_return_pct": {
                "type": "number",
                "description": "Total return as a percentage (e.g. 50 for 50%).",
            },
            "years": {
                "type": "number",
                "description": "Number of years over which the return was earned.",
            },
        },
        "required": ["total_return_pct", "years"],
    },
}


def annualized_return_calculator(
    total_return_pct: float, years: float
) -> dict[str, Any]:
    """Calculate annualized return."""
    try:
        total_return_pct = float(total_return_pct)
        years = float(years)

        if years <= 0:
            raise ValueError("years must be greater than zero.")

        growth_factor = 1 + total_return_pct / 100
        if growth_factor < 0:
            raise ValueError("Total return implies negative growth factor; cannot annualize.")

        annualized = growth_factor ** (1 / years) - 1

        return {
            "status": "ok",
            "data": {
                "annualized_return_decimal": round(annualized, 6),
                "annualized_return_pct": round(annualized * 100, 4),
            },
            "timestamp": datetime.now(timezone.utc).isoformat(),
        }
    except Exception as exc:
        return {
            "status": "error",
            "data": {"error": str(exc)},
            "timestamp": datetime.now(timezone.utc).isoformat(),
        }
