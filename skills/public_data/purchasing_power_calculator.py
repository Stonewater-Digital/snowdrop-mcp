"""Calculate future purchasing power erosion due to inflation.

MCP Tool Name: purchasing_power_calculator
"""
from __future__ import annotations
from datetime import datetime, timezone
from typing import Any

TOOL_META: dict[str, Any] = {
    "name": "purchasing_power_calculator",
    "description": "Calculate how inflation erodes purchasing power over time. Shows future value of money in today's dollars.",
    "inputSchema": {
        "type": "object",
        "properties": {
            "amount": {
                "type": "number",
                "description": "Current dollar amount.",
            },
            "annual_inflation": {
                "type": "number",
                "description": "Expected annual inflation rate as decimal (e.g., 0.03 for 3%).",
                "default": 0.03,
            },
            "years": {
                "type": "integer",
                "description": "Number of years into the future.",
                "default": 10,
            },
        },
        "required": ["amount"],
    },
}


def purchasing_power_calculator(
    amount: float,
    annual_inflation: float = 0.03,
    years: int = 10,
) -> dict[str, Any]:
    """Calculate future purchasing power erosion due to inflation."""
    try:
        if annual_inflation <= -1.0:
            return {
                "status": "error",
                "data": {"error": "Annual inflation rate must be greater than -100%."},
                "timestamp": datetime.now(timezone.utc).isoformat(),
            }
        if years < 0:
            return {
                "status": "error",
                "data": {"error": "Years must be non-negative."},
                "timestamp": datetime.now(timezone.utc).isoformat(),
            }

        future_purchasing_power = amount / ((1 + annual_inflation) ** years)
        purchasing_power_lost = amount - future_purchasing_power
        pct_lost = (purchasing_power_lost / amount) * 100 if amount != 0 else 0

        # Year-by-year breakdown
        yearly = []
        for y in range(1, years + 1):
            pp = amount / ((1 + annual_inflation) ** y)
            yearly.append({
                "year": y,
                "purchasing_power": round(pp, 2),
                "cumulative_loss_pct": round((1 - pp / amount) * 100, 2) if amount != 0 else 0,
            })

        return {
            "status": "ok",
            "data": {
                "original_amount": amount,
                "annual_inflation_rate": annual_inflation,
                "annual_inflation_pct": round(annual_inflation * 100, 2),
                "years": years,
                "future_purchasing_power": round(future_purchasing_power, 2),
                "purchasing_power_lost": round(purchasing_power_lost, 2),
                "pct_lost": round(pct_lost, 2),
                "yearly_breakdown": yearly,
                "interpretation": (
                    f"${amount:,.2f} today will have the purchasing power of ${future_purchasing_power:,.2f} "
                    f"in {years} years at {annual_inflation*100:.1f}% annual inflation. "
                    f"That is a loss of ${purchasing_power_lost:,.2f} ({pct_lost:.1f}%) in real value."
                ),
            },
            "timestamp": datetime.now(timezone.utc).isoformat(),
        }
    except Exception as exc:
        return {
            "status": "error",
            "data": {"error": str(exc)},
            "timestamp": datetime.now(timezone.utc).isoformat(),
        }
