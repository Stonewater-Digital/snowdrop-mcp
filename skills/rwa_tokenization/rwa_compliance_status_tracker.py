"""Track compliance checks for RWA issuers.
Aggregates pass/fail items and severity gaps."""
from __future__ import annotations

from datetime import datetime, timezone
from typing import Any, Sequence
import logging

from skills.utils import log_lesson

logger = logging.getLogger("snowdrop.skills")

TOOL_META: dict[str, Any] = {
    "name": "rwa_compliance_status_tracker",
    "description": "Rolls up AML, KYC, and filing checks into a single compliance status report.",
    "inputSchema": {
        "type": "object",
        "properties": {
            "checks": {
                "type": "array",
                "items": {
                    "type": "object",
                    "properties": {
                        "name": {"type": "string"},
                        "passed": {"type": "boolean"},
                        "severity": {"type": "string", "enum": ["low", "medium", "high"]},
                    },
                    "required": ["name", "passed", "severity"],
                },
                "description": "Compliance checklist items",
            }
        },
        "required": ["checks"],
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


def rwa_compliance_status_tracker(
    checks: Sequence[dict[str, Any]],
    **_: Any,
) -> dict[str, Any]:
    """Summarize compliance checks.

    Args:
        checks: Sequence of compliance check statuses.

    Returns:
        Dict indicating pass rates and outstanding deficiencies.
    """
    try:
        total = len(checks)
        passed = sum(1 for check in checks if check.get("passed"))
        failed_checks = [check for check in checks if not check.get("passed")]
        high_severity_open = any(check.get("severity") == "high" for check in failed_checks)
        data = {
            "pass_rate_pct": round((passed / total * 100) if total else 0.0, 2),
            "open_items": failed_checks,
            "overall_status": "green" if not failed_checks else "yellow" if not high_severity_open else "red",
        }
        return {"status": "success", "data": data, "timestamp": datetime.now(timezone.utc).isoformat()}
    except Exception as exc:  # noqa: BLE001
        logger.exception("rwa_compliance_status_tracker failure: %s", exc)
        log_lesson(f"rwa_compliance_status_tracker: {exc}")
        return {"status": "error", "error": str(exc), "timestamp": datetime.now(timezone.utc).isoformat()}
