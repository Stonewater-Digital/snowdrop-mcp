"""Estimate insurance premiums using heuristics."""
from __future__ import annotations

from datetime import datetime, timezone
from typing import Any

TOOL_META: dict[str, Any] = {
    "name": "premium_estimator",
    "description": "Provides heuristic premium estimates based on business profile and coverage type.",
    "inputSchema": {
        "type": "object",
        "properties": {
            "business_profile": {"type": "object"},
            "coverage_type": {"type": "string"},
        },
        "required": ["business_profile", "coverage_type"],
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


_BASE_RATES = {
    "tech": 0.015,
    "fintech": 0.018,
    "defi": 0.02,
    "professional_services": 0.012,
}

_COVERAGE_FACTORS = {
    "E&O": 1.3,
    "cyber": 1.1,
    "general_liability": 0.9,
    "D&O": 1.4,
}


def premium_estimator(
    business_profile: dict[str, Any],
    coverage_type: str,
    **_: Any,
) -> dict[str, Any]:
    """Estimate annual premium within heuristic bounds."""
    try:
        required_fields = ["annual_revenue", "employee_count", "years_in_business", "prior_claims"]
        for field in required_fields:
            if field not in business_profile:
                raise ValueError(f"business_profile missing {field}")

        industry = str(business_profile.get("industry", "tech")).lower()
        revenue = float(business_profile["annual_revenue"])
        employees = int(business_profile["employee_count"])
        years = int(business_profile["years_in_business"])
        prior_claims = int(business_profile["prior_claims"])

        base_rate = _BASE_RATES.get(industry, 0.013)
        coverage_factor = _COVERAGE_FACTORS.get(coverage_type, 1.0)

        exposure = max(revenue, employees * 150_000)
        premium = exposure * base_rate * coverage_factor

        factors = []
        if prior_claims > 0:
            surcharge = 1 + prior_claims * 0.1
            premium *= surcharge
            factors.append({"factor": "claims_surcharge", "multiplier": surcharge})
        if years < 3:
            premium *= 1.2
            factors.append({"factor": "new_business", "multiplier": 1.2})
        if employees > 50:
            premium *= 1.1
            factors.append({"factor": "headcount_scale", "multiplier": 1.1})

        confidence = "high" if prior_claims == 0 and years >= 3 else "medium"
        if employees == 0 or revenue == 0:
            confidence = "low"

        recommendation = "Proceed with broker quotes" if confidence != "high" else "Ready for bind".
        data = {
            "coverage_type": coverage_type,
            "estimated_annual_premium": round(premium, 2),
            "confidence": confidence,
            "factors": factors,
            "recommendation": recommendation,
        }
        return {
            "status": "success",
            "data": data,
            "timestamp": datetime.now(timezone.utc).isoformat(),
        }
    except Exception as exc:  # noqa: BLE001
        _log_lesson("premium_estimator", str(exc))
        return {
            "status": "error",
            "data": {"error": str(exc)},
            "timestamp": datetime.now(timezone.utc).isoformat(),
        }


def _log_lesson(skill_name: str, error: str) -> None:
    with open("logs/lessons.md", "a", encoding="utf-8") as handle:
        handle.write(f"- [{datetime.now(timezone.utc).isoformat()}] {skill_name}: {error}\n")
