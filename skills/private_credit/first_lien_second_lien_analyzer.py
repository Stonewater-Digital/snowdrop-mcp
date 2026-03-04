"""Model recoveries across first and second lien capital."""
from __future__ import annotations

from datetime import datetime, timezone
from typing import Any

TOOL_META: dict[str, Any] = {
    "name": "first_lien_second_lien_analyzer",
    "description": "Allocates recovery value between first-lien and second-lien creditors.",
    "inputSchema": {
        "type": "object",
        "properties": {
            "enterprise_value": {"type": "number"},
            "senior_debt": {"type": "number"},
            "junior_debt": {"type": "number"},
            "recovery_pct": {"type": "number", "default": 70.0},
        },
        "required": ["enterprise_value", "senior_debt", "junior_debt"],
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


def first_lien_second_lien_analyzer(
    enterprise_value: float,
    senior_debt: float,
    junior_debt: float,
    recovery_pct: float = 70.0,
    **_: Any,
) -> dict[str, Any]:
    """Return recovery waterfall by lien class."""
    try:
        recoverable_value = enterprise_value * (recovery_pct / 100)
        senior_recovery = min(senior_debt, recoverable_value)
        junior_recovery = max(recoverable_value - senior_recovery, 0.0)
        junior_recovery = min(junior_recovery, junior_debt)
        senior_recovery_pct = senior_recovery / senior_debt * 100 if senior_debt else 0.0
        junior_recovery_pct = junior_recovery / junior_debt * 100 if junior_debt else 0.0
        ltv = (senior_debt + junior_debt) / enterprise_value * 100 if enterprise_value else 0.0
        data = {
            "recoverable_value": round(recoverable_value, 2),
            "senior_recovery": round(senior_recovery, 2),
            "junior_recovery": round(junior_recovery, 2),
            "senior_recovery_pct": round(senior_recovery_pct, 2),
            "junior_recovery_pct": round(junior_recovery_pct, 2),
            "blended_ltv_pct": round(ltv, 2),
        }
        return {"status": "success", "data": data, "timestamp": datetime.now(timezone.utc).isoformat()}
    except Exception as exc:
        _log_lesson("first_lien_second_lien_analyzer", str(exc))
        return {
            "status": "error",
            "data": {"error": str(exc)},
            "timestamp": datetime.now(timezone.utc).isoformat(),
        }


def _log_lesson(skill_name: str, error: str) -> None:
    with open("logs/lessons.md", "a", encoding="utf-8") as handle:
        handle.write(f"- [{datetime.now(timezone.utc).isoformat()}] {skill_name}: {error}\n")
