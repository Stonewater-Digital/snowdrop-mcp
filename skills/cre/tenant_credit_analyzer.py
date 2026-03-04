"""Assess tenant creditworthiness for CRE underwriting."""
from __future__ import annotations

from datetime import datetime, timezone
from typing import Any

TOOL_META: dict[str, Any] = {
    "name": "tenant_credit_analyzer",
    "description": "Scores tenant credit strength based on financials and lease metrics.",
    "inputSchema": {
        "type": "object",
        "properties": {
            "tenant": {"type": "object"},
            "property_rent_pct_of_revenue": {"type": "number"},
        },
        "required": ["tenant"],
    },
    "outputSchema": {
        "type": "object", "properties": {"status": {"type": "string"}, "data": {"type": "object"}, "timestamp": {"type": "string"}}},
}


def tenant_credit_analyzer(
    tenant: dict[str, Any],
    property_rent_pct_of_revenue: float | None = None,
    **_: Any,
) -> dict[str, Any]:
    """Return credit score and rent coverage for tenant."""
    try:
        revenue = tenant.get("revenue", 0.0)
        ebitda = tenant.get("ebitda", 0.0)
        rent = tenant.get("rent_annual", 0.0)
        leverage = tenant.get("total_debt", 0.0) / ebitda if ebitda else 0.0
        rent_coverage = ebitda / rent if rent else float("inf")
        rent_pct = property_rent_pct_of_revenue or (rent / revenue * 100 if revenue else 0.0)
        years = tenant.get("years_in_business", 0)
        base_score = 80 if tenant.get("credit_rating") else 60
        base_score -= leverage * 5
        base_score += (rent_coverage - 1) * 10
        base_score += min(years, 20)
        score = max(min(base_score, 100), 0)
        if rent_pct > 15:
            score -= 10
        risk_tier = "investment_grade" if score >= 80 else "crossover" if score >= 65 else "high_yield" if score >= 45 else "distressed"
        lease_risk = "secure" if rent_coverage > 3 else "moderate" if rent_coverage > 1.5 else "elevated"
        deposit = 3 if risk_tier in {"investment_grade", "crossover"} else 6
        data = {
            "credit_score": round(score, 1),
            "rent_coverage_ratio": round(rent_coverage, 2),
            "rent_to_revenue_pct": round(rent_pct, 2),
            "risk_tier": risk_tier,
            "lease_risk_assessment": lease_risk,
            "recommended_security_deposit_months": deposit,
        }
        return {"status": "success", "data": data, "timestamp": datetime.now(timezone.utc).isoformat()}
    except Exception as exc:
        _log_lesson("tenant_credit_analyzer", str(exc))
        return {"status": "error", "data": {"error": str(exc)}, "timestamp": datetime.now(timezone.utc).isoformat()}


def _log_lesson(skill_name: str, error: str) -> None:
    with open("logs/lessons.md", "a", encoding="utf-8") as handle:
        handle.write(f"- [{datetime.now(timezone.utc).isoformat()}] {skill_name}: {error}\n")
