"""Captive insurance feasibility model.
Evaluates volatility absorption and surplus requirements.
"""
from __future__ import annotations

import logging
from datetime import datetime, timezone
from typing import Any

logger = logging.getLogger("snowdrop.skills")

TOOL_META: dict[str, Any] = {
    "name": "captive_insurance_feasibility_model",
    "description": "Scores captive feasibility based on losses, premium, and surplus needs.",
    "inputSchema": {
        "type": "object",
        "properties": {
            "expected_losses": {"type": "number"},
            "loss_volatility_pct": {"type": "number"},
            "planned_premium": {"type": "number"},
            "target_confidence_pct": {"type": "number", "default": 95.0},
            "operating_expenses": {"type": "number"},
        },
        "required": ["expected_losses", "loss_volatility_pct", "planned_premium", "operating_expenses"],
    },
    "outputSchema": {
        "type": "object",
        "properties": {"status": {"type": "string"}, "data": {"type": "object"}, "timestamp": {"type": "string"}},
    },
}


def captive_insurance_feasibility_model(
    expected_losses: float,
    loss_volatility_pct: float,
    planned_premium: float,
    operating_expenses: float,
    target_confidence_pct: float = 95.0,
    **_: Any,
) -> dict[str, Any]:
    """Return surplus requirement and feasibility score."""
    try:
        z_score = 1.65 if target_confidence_pct >= 95 else 1.28
        volatility = loss_volatility_pct / 100
        surplus_required = expected_losses * volatility * z_score
        combined_ratio = (expected_losses + operating_expenses) / planned_premium if planned_premium else 0.0
        feasibility_score = max(0, 100 - (combined_ratio - 1) * 200)
        data = {
            "surplus_required": round(surplus_required, 2),
            "combined_ratio": round(combined_ratio, 3),
            "feasibility_score": round(feasibility_score, 1),
            "recommendation": "proceed" if feasibility_score >= 70 else "review",
        }
        return {"status": "success", "data": data, "timestamp": datetime.now(timezone.utc).isoformat()}
    except Exception as exc:  # noqa: BLE001
        logger.exception("captive_insurance_feasibility_model failed")
        return {"status": "error", "error": str(exc), "timestamp": datetime.now(timezone.utc).isoformat()}
