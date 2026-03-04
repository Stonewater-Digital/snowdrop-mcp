"""Analyze unit economics: gross margin, LTV/CAC, and payback period.

MCP Tool Name: unit_economics_analyzer
"""
from __future__ import annotations
from datetime import datetime, timezone
from typing import Any

TOOL_META: dict[str, Any] = {
    "name": "unit_economics_analyzer",
    "description": "Analyze unit economics including gross margin, LTV:CAC ratio, and CAC payback period.",
    "inputSchema": {
        "type": "object",
        "properties": {
            "price": {"type": "number", "description": "Revenue per unit/transaction."},
            "cogs": {"type": "number", "description": "Cost of goods sold per unit."},
            "cac": {"type": "number", "description": "Customer Acquisition Cost."},
            "ltv": {"type": "number", "description": "Customer Lifetime Value."},
        },
        "required": ["price", "cogs", "cac", "ltv"],
    },
}


def unit_economics_analyzer(
    price: float, cogs: float, cac: float, ltv: float
) -> dict[str, Any]:
    """Analyze unit economics."""
    try:
        if price <= 0:
            return {
                "status": "error",
                "data": {"error": "price must be positive."},
                "timestamp": datetime.now(timezone.utc).isoformat(),
            }

        gross_profit = price - cogs
        gross_margin = (gross_profit / price) * 100
        ltv_cac = ltv / cac if cac > 0 else float("inf")

        # Payback period: CAC / monthly gross profit
        monthly_gp = gross_profit  # assuming price is monthly revenue
        payback_months = cac / monthly_gp if monthly_gp > 0 else float("inf")

        if ltv_cac >= 3:
            health = "Healthy"
        elif ltv_cac >= 1:
            health = "Marginal"
        else:
            health = "Unsustainable"

        return {
            "status": "ok",
            "data": {
                "price": price,
                "cogs": cogs,
                "gross_profit": round(gross_profit, 2),
                "gross_margin_pct": round(gross_margin, 2),
                "cac": cac,
                "ltv": ltv,
                "ltv_to_cac": round(ltv_cac, 2),
                "payback_months": round(payback_months, 1) if payback_months != float("inf") else None,
                "health": health,
            },
            "timestamp": datetime.now(timezone.utc).isoformat(),
        }
    except Exception as exc:
        return {
            "status": "error",
            "data": {"error": str(exc)},
            "timestamp": datetime.now(timezone.utc).isoformat(),
        }
