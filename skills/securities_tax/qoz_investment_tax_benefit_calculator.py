"""Qualified Opportunity Zone benefit calculator.
Estimates deferral, discount, and exclusion values for QOZ investments.
"""
from __future__ import annotations

import logging
from datetime import datetime, timezone
from typing import Any

logger = logging.getLogger("snowdrop.skills")

TOOL_META: dict[str, Any] = {
    "name": "qoz_investment_tax_benefit_calculator",
    "description": "Quantifies tax deferral and exclusion benefits for QOZ capital gains.",
    "inputSchema": {
        "type": "object",
        "properties": {
            "original_gain": {"type": "number"},
            "investment_amount": {"type": "number"},
            "holding_period_years": {"type": "number"},
            "capital_gains_rate_pct": {"type": "number", "default": 20.0},
        },
        "required": ["original_gain", "investment_amount", "holding_period_years"],
    },
    "outputSchema": {
        "type": "object",
        "properties": {"status": {"type": "string"}, "data": {"type": "object"}, "timestamp": {"type": "string"}},
    },
}


def qoz_investment_tax_benefit_calculator(
    original_gain: float,
    investment_amount: float,
    holding_period_years: float,
    capital_gains_rate_pct: float = 20.0,
    **_: Any,
) -> dict[str, Any]:
    """Return deferral amount and exclusion after 10 years."""
    try:
        deferral_value = original_gain * capital_gains_rate_pct / 100
        discount = 0.1 if holding_period_years >= 5 else 0.0
        exclusion = investment_amount * 0.15 if holding_period_years >= 10 else 0.0
        total_benefit = deferral_value * discount + exclusion
        data = {
            "deferral_value": round(deferral_value, 2),
            "basis_step_up_pct": discount * 100,
            "future_exclusion": round(exclusion, 2),
            "aggregate_benefit": round(total_benefit, 2),
        }
        return {"status": "success", "data": data, "timestamp": datetime.now(timezone.utc).isoformat()}
    except Exception as exc:  # noqa: BLE001
        logger.exception("qoz_investment_tax_benefit_calculator failed")
        return {"status": "error", "error": str(exc), "timestamp": datetime.now(timezone.utc).isoformat()}
