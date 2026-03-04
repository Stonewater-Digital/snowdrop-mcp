"""Track insurance coverage posture and renewals."""
from __future__ import annotations

from datetime import datetime, timezone
from typing import Any

TOOL_META: dict[str, Any] = {
    "name": "insurance_coverage_tracker",
    "description": "Summarizes insurance coverages, gaps, and renewal windows.",
    "inputSchema": {
        "type": "object",
        "properties": {
            "policies": {
                "type": "array",
                "items": {"type": "object"},
            },
            "current_date": {"type": "string"},
        },
        "required": ["policies", "current_date"],
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

_RECOMMENDED = {"E&O", "cyber", "general_liability", "D&O"}


def insurance_coverage_tracker(
    policies: list[dict[str, Any]],
    current_date: str,
    **_: Any,
) -> dict[str, Any]:
    """Aggregate insurance coverage stats."""
    try:
        if not isinstance(policies, list):
            raise ValueError("policies must be a list")
        ref_date = _parse_date(current_date, "current_date")

        total_premium = 0.0
        coverage_summary: dict[str, Any] = {}
        renewals: list[dict[str, Any]] = []

        for policy in policies:
            if not isinstance(policy, dict):
                raise ValueError("each policy must be a dict")
            policy_type = str(policy.get("type", "unknown"))
            total_premium += float(policy.get("premium_annual", 0.0))
            coverage_summary[policy_type] = {
                "carrier": policy.get("carrier"),
                "coverage_limit": policy.get("coverage_limit"),
                "deductible": policy.get("deductible"),
                "expiry_date": policy.get("expiry_date"),
            }
            expiry = _parse_date(policy.get("expiry_date"), "expiry_date") if policy.get("expiry_date") else None
            if expiry and 0 <= (expiry - ref_date).days <= 90:
                renewals.append({"type": policy_type, "expiry_date": expiry.isoformat(), "carrier": policy.get("carrier")})

        active_types = set(coverage_summary.keys())
        gaps = sorted(_RECOMMENDED - active_types)

        data = {
            "total_premium": round(total_premium, 2),
            "gaps": gaps,
            "renewals_within_90d": renewals,
            "coverage_summary": coverage_summary,
        }
        return {
            "status": "success",
            "data": data,
            "timestamp": datetime.now(timezone.utc).isoformat(),
        }
    except Exception as exc:  # noqa: BLE001
        _log_lesson("insurance_coverage_tracker", str(exc))
        return {
            "status": "error",
            "data": {"error": str(exc)},
            "timestamp": datetime.now(timezone.utc).isoformat(),
        }


def _parse_date(value: Any, field_name: str) -> datetime.date:
    if value is None:
        raise ValueError(f"{field_name} is required")
    if not isinstance(value, str):
        raise ValueError(f"{field_name} must be an ISO date string")
    try:
        return datetime.fromisoformat(value).date()
    except ValueError as exc:  # noqa: B904
        raise ValueError(f"Invalid {field_name}: {value}") from exc


def _log_lesson(skill_name: str, error: str) -> None:
    with open("logs/lessons.md", "a", encoding="utf-8") as handle:
        handle.write(f"- [{datetime.now(timezone.utc).isoformat()}] {skill_name}: {error}\n")
