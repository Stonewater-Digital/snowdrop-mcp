"""Score asset originators supporting RWA programs.
Evaluates track record, reporting cadence, and loss performance."""
from __future__ import annotations

from datetime import datetime, timezone
from typing import Any
import logging

from skills.utils import log_lesson

logger = logging.getLogger("snowdrop.skills")

TOOL_META: dict[str, Any] = {
    "name": "rwa_originator_quality_scorer",
    "description": "Combines historical loss rates, audits, and reporting cadence into an originator score.",
    "inputSchema": {
        "type": "object",
        "properties": {
            "years_operating": {"type": "number", "description": "Years in operation"},
            "cumulative_loss_rate_pct": {"type": "number", "description": "Historical loss rate"},
            "audit_rating_pct": {"type": "number", "description": "Audit quality percent"},
            "reporting_timeliness_score": {
                "type": "number",
                "description": "Score 0-100 for reporting timeliness",
            },
        },
        "required": ["years_operating", "cumulative_loss_rate_pct", "audit_rating_pct", "reporting_timeliness_score"],
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


def rwa_originator_quality_scorer(
    years_operating: float,
    cumulative_loss_rate_pct: float,
    audit_rating_pct: float,
    reporting_timeliness_score: float,
    **_: Any,
) -> dict[str, Any]:
    """Score originator quality.

    Args:
        years_operating: Track record length.
        cumulative_loss_rate_pct: Historical loss experience.
        audit_rating_pct: Audit quality score.
        reporting_timeliness_score: Timeliness evaluation.

    Returns:
        Dict containing composite score and risk tier.
    """
    try:
        tenure_score = min(years_operating / 10, 1.0)
        loss_score = max(1 - cumulative_loss_rate_pct / 10, 0)
        audit_score = audit_rating_pct / 100
        reporting_score = reporting_timeliness_score / 100
        composite = round((tenure_score * 0.3 + loss_score * 0.3 + audit_score * 0.2 + reporting_score * 0.2), 3)
        data = {
            "originator_score": composite,
            "risk_tier": "strong" if composite > 0.75 else "average" if composite > 0.5 else "weak",
        }
        return {"status": "success", "data": data, "timestamp": datetime.now(timezone.utc).isoformat()}
    except Exception as exc:  # noqa: BLE001
        logger.exception("rwa_originator_quality_scorer failure: %s", exc)
        log_lesson(f"rwa_originator_quality_scorer: {exc}")
        return {"status": "error", "error": str(exc), "timestamp": datetime.now(timezone.utc).isoformat()}
