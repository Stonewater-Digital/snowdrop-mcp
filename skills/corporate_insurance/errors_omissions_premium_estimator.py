"""Errors & omissions premium estimator.
Applies exposure-based rating with credits and surcharges.
"""
from __future__ import annotations

import logging
from datetime import datetime, timezone
from typing import Any

logger = logging.getLogger("snowdrop.skills")

TOOL_META: dict[str, Any] = {
    "name": "errors_omissions_premium_estimator",
    "description": "Calculates E&O premium using rate per revenue and modifiers.",
    "inputSchema": {
        "type": "object",
        "properties": {
            "annual_revenue": {"type": "number"},
            "base_rate_per_million": {"type": "number"},
            "risk_modifier_pct": {"type": "number", "default": 0.0},
            "claims_history_credit_pct": {"type": "number", "default": 0.0},
        },
        "required": ["annual_revenue", "base_rate_per_million"],
    },
    "outputSchema": {
        "type": "object",
        "properties": {"status": {"type": "string"}, "data": {"type": "object"}, "timestamp": {"type": "string"}},
    },
}


def errors_omissions_premium_estimator(
    annual_revenue: float,
    base_rate_per_million: float,
    risk_modifier_pct: float = 0.0,
    claims_history_credit_pct: float = 0.0,
    **_: Any,
) -> dict[str, Any]:
    """Return indicated premium and modifier details."""
    try:
        exposure_units = annual_revenue / 1_000_000
        base_premium = exposure_units * base_rate_per_million
        modifier = 1 + risk_modifier_pct / 100 - claims_history_credit_pct / 100
        premium = base_premium * modifier
        data = {
            "exposure_units_million": round(exposure_units, 4),
            "base_premium": round(base_premium, 2),
            "final_premium": round(premium, 2),
            "composite_modifier": round(modifier, 4),
        }
        return {"status": "success", "data": data, "timestamp": datetime.now(timezone.utc).isoformat()}
    except Exception as exc:  # noqa: BLE001
        logger.exception("errors_omissions_premium_estimator failed")
        return {"status": "error", "error": str(exc), "timestamp": datetime.now(timezone.utc).isoformat()}
