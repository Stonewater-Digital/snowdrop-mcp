"""Evaluate franchise operators for Bar-in-a-Box."""
from __future__ import annotations

from datetime import datetime, timezone
from typing import Any

TOOL_META: dict[str, Any] = {
    "name": "franchise_onboarder",
    "description": "Checks franchise safety gates and returns royalty terms.",
    "inputSchema": {
        "type": "object",
        "properties": {
            "operator_id": {"type": "string"},
            "security_audit_score": {"type": "number"},
            "has_bouncer": {"type": "boolean"},
        },
        "required": ["operator_id", "security_audit_score", "has_bouncer"],
    },
    "outputSchema": {
        "type": "object",
        "properties": {
            "status": {"type": "string"},
            "data": {"type": "object"},
            "timestamp": {"type": "string"},
        },
    },
}


def franchise_onboarder(
    operator_id: str,
    security_audit_score: float,
    has_bouncer: bool,
    **_: Any,
) -> dict[str, Any]:
    """Return approval decision plus royalty schedule.

    Args:
        operator_id: Unique operator identifier.
        security_audit_score: Latest audit score (0-100 scale).
        has_bouncer: Whether the operator has on-site security.

    Returns:
        Envelope confirming approval status and associated terms.
    """

    try:
        approved = security_audit_score >= 80 and has_bouncer
        reason = []
        if security_audit_score < 80:
            reason.append("security audit < 80")
        if not has_bouncer:
            reason.append("no on-prem bouncer")
        rationale = ", ".join(reason) if reason else "meets controls"

        data = {
            "operator_id": operator_id,
            "approved": approved,
            "royalty_rate_pct": 10.0 if approved else None,
            "terms": "10% of gross sales remitted weekly" if approved else "remediate and retry",
            "rationale": rationale,
        }

        return {
            "status": "success",
            "data": data,
            "timestamp": datetime.now(timezone.utc).isoformat(),
        }
    except Exception as exc:
        _log_lesson("franchise_onboarder", str(exc))
        return {
            "status": "error",
            "data": {"error": str(exc)},
            "timestamp": datetime.now(timezone.utc).isoformat(),
        }


def _log_lesson(skill_name: str, error: str) -> None:
    with open("logs/lessons.md", "a", encoding="utf-8") as handle:
        handle.write(f"- [{datetime.now(timezone.utc).isoformat()}] {skill_name}: {error}\n")
