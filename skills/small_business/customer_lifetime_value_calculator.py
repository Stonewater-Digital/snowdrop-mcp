"""Calculate Customer Lifetime Value (CLV).

MCP Tool Name: customer_lifetime_value_calculator
"""
from __future__ import annotations
from datetime import datetime, timezone
from typing import Any

TOOL_META: dict[str, Any] = {
    "name": "customer_lifetime_value_calculator",
    "description": "Calculate Customer Lifetime Value: LTV = avg_purchase * purchase_frequency * customer_lifespan_years.",
    "inputSchema": {
        "type": "object",
        "properties": {
            "avg_purchase": {"type": "number", "description": "Average purchase value."},
            "purchase_frequency": {"type": "number", "description": "Average number of purchases per year."},
            "customer_lifespan_years": {"type": "number", "description": "Average customer lifespan in years."},
        },
        "required": ["avg_purchase", "purchase_frequency", "customer_lifespan_years"],
    },
}


def customer_lifetime_value_calculator(
    avg_purchase: float, purchase_frequency: float, customer_lifespan_years: float
) -> dict[str, Any]:
    """Calculate Customer Lifetime Value."""
    try:
        if avg_purchase < 0 or purchase_frequency < 0 or customer_lifespan_years < 0:
            return {
                "status": "error",
                "data": {"error": "All inputs must be non-negative."},
                "timestamp": datetime.now(timezone.utc).isoformat(),
            }

        annual_value = avg_purchase * purchase_frequency
        ltv = annual_value * customer_lifespan_years

        return {
            "status": "ok",
            "data": {
                "avg_purchase": avg_purchase,
                "purchase_frequency": purchase_frequency,
                "customer_lifespan_years": customer_lifespan_years,
                "annual_customer_value": round(annual_value, 2),
                "lifetime_value": round(ltv, 2),
            },
            "timestamp": datetime.now(timezone.utc).isoformat(),
        }
    except Exception as exc:
        return {
            "status": "error",
            "data": {"error": str(exc)},
            "timestamp": datetime.now(timezone.utc).isoformat(),
        }
