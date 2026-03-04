"""Calculate Customer Acquisition Cost (CAC) and optional LTV:CAC ratio.

MCP Tool Name: customer_acquisition_cost_calculator
"""
from __future__ import annotations
from datetime import datetime, timezone
from typing import Any

TOOL_META: dict[str, Any] = {
    "name": "customer_acquisition_cost_calculator",
    "description": "Calculate Customer Acquisition Cost: CAC = total_marketing_spend / new_customers. Optionally compute LTV:CAC ratio.",
    "inputSchema": {
        "type": "object",
        "properties": {
            "total_marketing_spend": {"type": "number", "description": "Total marketing and sales spend."},
            "new_customers": {"type": "integer", "description": "Number of new customers acquired."},
            "ltv": {"type": "number", "description": "Optional Customer Lifetime Value for LTV:CAC ratio."},
        },
        "required": ["total_marketing_spend", "new_customers"],
    },
}


def customer_acquisition_cost_calculator(
    total_marketing_spend: float, new_customers: int, ltv: float = 0
) -> dict[str, Any]:
    """Calculate CAC and optional LTV:CAC ratio."""
    try:
        if new_customers <= 0:
            return {
                "status": "error",
                "data": {"error": "new_customers must be positive."},
                "timestamp": datetime.now(timezone.utc).isoformat(),
            }

        cac = total_marketing_spend / new_customers

        result: dict[str, Any] = {
            "total_marketing_spend": total_marketing_spend,
            "new_customers": new_customers,
            "cac": round(cac, 2),
        }

        if ltv and ltv > 0:
            result["ltv"] = ltv
            result["ltv_to_cac"] = round(ltv / cac, 2)
            if ltv / cac >= 3:
                result["assessment"] = "Healthy (LTV:CAC >= 3:1)"
            elif ltv / cac >= 1:
                result["assessment"] = "Marginal (1:1 <= LTV:CAC < 3:1)"
            else:
                result["assessment"] = "Unsustainable (LTV:CAC < 1:1)"

        return {
            "status": "ok",
            "data": result,
            "timestamp": datetime.now(timezone.utc).isoformat(),
        }
    except Exception as exc:
        return {
            "status": "error",
            "data": {"error": str(exc)},
            "timestamp": datetime.now(timezone.utc).isoformat(),
        }
