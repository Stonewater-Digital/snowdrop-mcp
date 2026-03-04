"""Environmental liability exposure model.
Quantifies cleanup and third-party liability costs for pollution events.
"""
from __future__ import annotations

import logging
from datetime import datetime, timezone
from typing import Any

logger = logging.getLogger("snowdrop.skills")

TOOL_META: dict[str, Any] = {
    "name": "environmental_liability_exposure_model",
    "description": "Estimates environmental liability exposure using scenario severities.",
    "inputSchema": {
        "type": "object",
        "properties": {
            "cleanup_cost": {"type": "number"},
            "third_party_liability": {"type": "number"},
            "regulatory_fines": {"type": "number"},
            "probability_pct": {"type": "number"},
        },
        "required": ["cleanup_cost", "third_party_liability", "regulatory_fines", "probability_pct"],
    },
    "outputSchema": {
        "type": "object",
        "properties": {"status": {"type": "string"}, "data": {"type": "object"}, "timestamp": {"type": "string"}},
    },
}


def environmental_liability_exposure_model(
    cleanup_cost: float,
    third_party_liability: float,
    regulatory_fines: float,
    probability_pct: float,
    **_: Any,
) -> dict[str, Any]:
    """Return expected loss and coverage recommendation."""
    try:
        severity = cleanup_cost + third_party_liability + regulatory_fines
        expected_loss = severity * probability_pct / 100
        adequacy = "adequate" if severity <= 50_000_000 else "needs_review"
        data = {
            "modeled_severity": round(severity, 2),
            "expected_loss": round(expected_loss, 2),
            "loss_split": {
                "cleanup_pct": round(cleanup_cost / severity * 100 if severity else 0.0, 2),
                "third_party_pct": round(third_party_liability / severity * 100 if severity else 0.0, 2),
                "fines_pct": round(regulatory_fines / severity * 100 if severity else 0.0, 2),
            },
            "coverage_adequacy": adequacy,
        }
        return {"status": "success", "data": data, "timestamp": datetime.now(timezone.utc).isoformat()}
    except Exception as exc:  # noqa: BLE001
        logger.exception("environmental_liability_exposure_model failed")
        return {"status": "error", "error": str(exc), "timestamp": datetime.now(timezone.utc).isoformat()}
