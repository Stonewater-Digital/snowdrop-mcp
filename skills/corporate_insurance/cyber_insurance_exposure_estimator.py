"""Cyber insurance exposure estimator.
Scores cyber posture and required limit based on financial impact.
"""
from __future__ import annotations

import logging
from datetime import datetime, timezone
from typing import Any

logger = logging.getLogger("snowdrop.skills")

TOOL_META: dict[str, Any] = {
    "name": "cyber_insurance_exposure_estimator",
    "description": "Estimates cyber limit need from revenue, records, and controls maturity.",
    "inputSchema": {
        "type": "object",
        "properties": {
            "annual_revenue": {"type": "number"},
            "records_at_risk_millions": {"type": "number"},
            "control_score_pct": {"type": "number"},
            "event_probability_pct": {"type": "number"},
        },
        "required": ["annual_revenue", "records_at_risk_millions", "control_score_pct", "event_probability_pct"],
    },
    "outputSchema": {
        "type": "object",
        "properties": {"status": {"type": "string"}, "data": {"type": "object"}, "timestamp": {"type": "string"}},
    },
}


def cyber_insurance_exposure_estimator(
    annual_revenue: float,
    records_at_risk_millions: float,
    control_score_pct: float,
    event_probability_pct: float,
    **_: Any,
) -> dict[str, Any]:
    """Return estimated cyber loss and suggested limit."""
    try:
        severity = annual_revenue * 0.08 + records_at_risk_millions * 250_000
        probability = event_probability_pct / 100 * (1 - control_score_pct / 100)
        expected_loss = severity * probability
        suggested_limit = expected_loss * 1.5
        security_rating = "strong" if control_score_pct > 80 else "weak" if control_score_pct < 50 else "average"
        data = {
            "expected_loss": round(expected_loss, 2),
            "suggested_limit": round(suggested_limit, 2),
            "security_rating": security_rating,
            "modeled_probability_pct": round(probability * 100, 2),
        }
        return {"status": "success", "data": data, "timestamp": datetime.now(timezone.utc).isoformat()}
    except Exception as exc:  # noqa: BLE001
        logger.exception("cyber_insurance_exposure_estimator failed")
        return {"status": "error", "error": str(exc), "timestamp": datetime.now(timezone.utc).isoformat()}
