"""Evaluate potential vendors against Snowdrop requirements."""
from __future__ import annotations

from datetime import datetime, timezone
from typing import Any

TOOL_META: dict[str, Any] = {
    "name": "vendor_due_diligence",
    "description": "Scores vendor fit based on uptime, pricing, certifications, and experience.",
    "inputSchema": {
        "type": "object",
        "properties": {
            "vendor": {"type": "object"},
            "requirements": {"type": "object"},
        },
        "required": ["vendor", "requirements"],
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


def vendor_due_diligence(
    vendor: dict[str, Any],
    requirements: dict[str, Any],
    **_: Any,
) -> dict[str, Any]:
    """Return vendor diligence score and recommendation."""
    try:
        uptime = float(vendor.get("uptime_sla_pct", 0.0))
        min_uptime = float(requirements.get("min_uptime", 99.0))
        pricing = vendor.get("pricing", {}) or {}
        max_cost = float(requirements.get("max_cost_monthly", 0.0))
        monthly_cost = float(pricing.get("monthly", pricing.get("base", 0.0)))
        certs = set(vendor.get("security_certifications", []))
        required_certs = set(requirements.get("required_certs", []))
        cert_gaps = sorted(required_certs - certs)
        strengths = []
        score = 0.0

        if uptime >= min_uptime:
            score += 30
            strengths.append("Meets uptime")
        else:
            cert_gaps.append("uptime")

        if max_cost and monthly_cost <= max_cost:
            score += 25
            strengths.append("Within budget")
        elif not max_cost:
            score += 10

        if not cert_gaps:
            score += 25
            strengths.append("All certifications present")

        years = int(vendor.get("years_in_operation", 0))
        score += min(years * 2, 20)
        meets_requirements = score >= 70 and not cert_gaps
        recommendation = "Proceed to sandbox" if meets_requirements else "Collect mitigations"
        data = {
            "score": round(score, 1),
            "meets_requirements": meets_requirements,
            "gaps": cert_gaps,
            "strengths": strengths,
            "recommendation": recommendation,
        }
        return {
            "status": "success",
            "data": data,
            "timestamp": datetime.now(timezone.utc).isoformat(),
        }
    except Exception as exc:  # noqa: BLE001
        _log_lesson("vendor_due_diligence", str(exc))
        return {
            "status": "error",
            "data": {"error": str(exc)},
            "timestamp": datetime.now(timezone.utc).isoformat(),
        }


def _log_lesson(skill_name: str, error: str) -> None:
    with open("logs/lessons.md", "a", encoding="utf-8") as handle:
        handle.write(f"- [{datetime.now(timezone.utc).isoformat()}] {skill_name}: {error}\n")
