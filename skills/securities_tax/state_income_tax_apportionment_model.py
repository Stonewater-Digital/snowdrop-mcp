"""State income tax apportionment model.
Calculates factors and tax due across states using property-payroll-sales formula.
"""
from __future__ import annotations

import logging
from datetime import datetime, timezone
from typing import Any, Sequence

logger = logging.getLogger("snowdrop.skills")

TOOL_META: dict[str, Any] = {
    "name": "state_income_tax_apportionment_model",
    "description": "Apportions taxable income among states via three-factor formula.",
    "inputSchema": {
        "type": "object",
        "properties": {
            "states": {
                "type": "array",
                "items": {
                    "type": "object",
                    "properties": {
                        "state": {"type": "string"},
                        "sales": {"type": "number"},
                        "property": {"type": "number"},
                        "payroll": {"type": "number"},
                        "tax_rate_pct": {"type": "number"},
                    },
                    "required": ["state", "sales", "property", "payroll", "tax_rate_pct"],
                },
            },
            "taxable_income": {"type": "number"},
        },
        "required": ["states", "taxable_income"],
    },
    "outputSchema": {
        "type": "object",
        "properties": {"status": {"type": "string"}, "data": {"type": "object"}, "timestamp": {"type": "string"}},
    },
}


def state_income_tax_apportionment_model(states: Sequence[dict[str, Any]], taxable_income: float, **_: Any) -> dict[str, Any]:
    """Return apportionment percentages and tax per state."""
    try:
        total_sales = sum(item["sales"] for item in states)
        total_property = sum(item["property"] for item in states)
        total_payroll = sum(item["payroll"] for item in states)
        results = []
        total_tax = 0.0
        for item in states:
            sales_factor = item["sales"] / total_sales if total_sales else 0.0
            property_factor = item["property"] / total_property if total_property else 0.0
            payroll_factor = item["payroll"] / total_payroll if total_payroll else 0.0
            apportionment = (sales_factor + property_factor + payroll_factor) / 3
            state_income = taxable_income * apportionment
            tax = state_income * item["tax_rate_pct"] / 100
            total_tax += tax
            results.append(
                {
                    "state": item["state"].upper(),
                    "apportionment_pct": round(apportionment * 100, 3),
                    "taxable_income": round(state_income, 2),
                    "tax": round(tax, 2),
                }
            )
        data = {
            "state_taxes": results,
            "total_state_tax": round(total_tax, 2),
        }
        return {"status": "success", "data": data, "timestamp": datetime.now(timezone.utc).isoformat()}
    except Exception as exc:  # noqa: BLE001
        logger.exception("state_income_tax_apportionment_model failed")
        return {"status": "error", "error": str(exc), "timestamp": datetime.now(timezone.utc).isoformat()}
