"""Key person insurance valuation tool.
Values economic exposure tied to critical personnel.
"""
from __future__ import annotations

import logging
from datetime import datetime, timezone
from typing import Any

logger = logging.getLogger("snowdrop.skills")

TOOL_META: dict[str, Any] = {
    "name": "key_person_insurance_valuation",
    "description": "Calculates key person insurance amount using salary, pipeline, and replacement time.",
    "inputSchema": {
        "type": "object",
        "properties": {
            "annual_compensation": {"type": "number"},
            "revenue_contribution": {"type": "number"},
            "replacement_time_months": {"type": "number"},
            "knowledge_transfer_factor_pct": {"type": "number", "default": 50.0},
        },
        "required": ["annual_compensation", "revenue_contribution", "replacement_time_months"],
    },
    "outputSchema": {
        "type": "object",
        "properties": {"status": {"type": "string"}, "data": {"type": "object"}, "timestamp": {"type": "string"}},
    },
}


def key_person_insurance_valuation(
    annual_compensation: float,
    revenue_contribution: float,
    replacement_time_months: float,
    knowledge_transfer_factor_pct: float = 50.0,
    **_: Any,
) -> dict[str, Any]:
    """Return suggested limit and gap vs current coverage."""
    try:
        payroll_cost = annual_compensation * (replacement_time_months / 12)
        pipeline_cost = revenue_contribution * (knowledge_transfer_factor_pct / 100)
        suggested_limit = payroll_cost + pipeline_cost
        opportunity_loss_pct = (pipeline_cost / revenue_contribution * 100) if revenue_contribution else 0.0
        data = {
            "suggested_limit": round(suggested_limit, 2),
            "payroll_cost": round(payroll_cost, 2),
            "pipeline_cost": round(pipeline_cost, 2),
            "opportunity_loss_pct": round(opportunity_loss_pct, 2),
        }
        return {"status": "success", "data": data, "timestamp": datetime.now(timezone.utc).isoformat()}
    except Exception as exc:  # noqa: BLE001
        logger.exception("key_person_insurance_valuation failed")
        return {"status": "error", "error": str(exc), "timestamp": datetime.now(timezone.utc).isoformat()}
