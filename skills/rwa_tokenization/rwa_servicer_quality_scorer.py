"""Score servicing partners supporting RWA programs.
Focuses on remittance speed, historical accuracy, and staffing."""
from __future__ import annotations

from datetime import datetime, timezone
from typing import Any
import logging

from skills.utils import log_lesson

logger = logging.getLogger("snowdrop.skills")

TOOL_META: dict[str, Any] = {
    "name": "rwa_servicer_quality_scorer",
    "description": "Generates a composite score for RWA servicers using accuracy, staffing, and remittance metrics.",
    "inputSchema": {
        "type": "object",
        "properties": {
            "error_rate_pct": {"type": "number", "description": "Servicing error rate percent"},
            "remittance_days": {"type": "number", "description": "Average days to remit cash"},
            "staff_tenure_years": {"type": "number", "description": "Average staff tenure"},
            "systems_uptime_pct": {"type": "number", "description": "Servicing platform uptime percent"},
        },
        "required": ["error_rate_pct", "remittance_days", "staff_tenure_years", "systems_uptime_pct"],
    },
    "outputSchema": {
        "type": "object",
        "properties": {
            "status": {"type": "string"},
            "timestamp": {"type": "string"},
            "data": {"type": "object"},
            "error": {"type": "string"},
        },
    },
}


def rwa_servicer_quality_scorer(
    error_rate_pct: float,
    remittance_days: float,
    staff_tenure_years: float,
    systems_uptime_pct: float,
    **_: Any,
) -> dict[str, Any]:
    """Score servicer performance.

    Args:
        error_rate_pct: Servicing accuracy issues.
        remittance_days: Days to remit investor proceeds.
        staff_tenure_years: Average tenure of servicing team.
        systems_uptime_pct: Availability of servicing platform.

    Returns:
        Dict with composite score and qualitative recommendation.
    """
    try:
        accuracy_score = max(1 - error_rate_pct / 5, 0)
        remittance_score = max(1 - remittance_days / 10, 0)
        tenure_score = min(staff_tenure_years / 5, 1)
        uptime_score = systems_uptime_pct / 100
        composite = round(accuracy_score * 0.35 + remittance_score * 0.25 + tenure_score * 0.15 + uptime_score * 0.25, 3)
        data = {
            "servicer_score": composite,
            "recommendation": "preferred" if composite > 0.8 else "watch" if composite > 0.6 else "replace",
        }
        return {"status": "success", "data": data, "timestamp": datetime.now(timezone.utc).isoformat()}
    except Exception as exc:  # noqa: BLE001
        logger.exception("rwa_servicer_quality_scorer failure: %s", exc)
        log_lesson(f"rwa_servicer_quality_scorer: {exc}")
        return {"status": "error", "error": str(exc), "timestamp": datetime.now(timezone.utc).isoformat()}
