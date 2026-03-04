"""Estimate cost segregation study benefits."""
from __future__ import annotations

from datetime import datetime, timezone
from typing import Any

PROPERTY_BUCKETS = {
    "office": 0.2,
    "retail": 0.22,
    "multifamily": 0.3,
    "industrial": 0.18,
    "hotel": 0.28,
    "restaurant": 0.25,
}

TOOL_META: dict[str, Any] = {
    "name": "cost_segregation_estimator",
    "description": "Approximates accelerated depreciation benefits from cost seg studies.",
    "inputSchema": {
        "type": "object",
        "properties": {
            "building_cost": {"type": "number"},
            "property_type": {"type": "string"},
            "building_age_years": {"type": "integer"},
            "tax_rate": {"type": "number", "default": 0.37},
        },
        "required": ["building_cost", "property_type", "building_age_years"],
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


def cost_segregation_estimator(
    building_cost: float,
    property_type: str,
    building_age_years: int,
    tax_rate: float = 0.37,
    **_: Any,
) -> dict[str, Any]:
    """Return accelerated depreciation impact estimates."""
    try:
        reclass_pct = PROPERTY_BUCKETS.get(property_type, 0.2)
        reclassified_amount = building_cost * reclass_pct
        straight_line = building_cost / 39
        accelerated_year1 = reclassified_amount * 0.2 + (building_cost - reclassified_amount) / 39
        tax_savings = (accelerated_year1 - straight_line) * tax_rate
        npv = tax_savings * 0.9  # simple proxy
        study_cost = building_cost * 0.01
        payback = study_cost / max(tax_savings, 1)
        data = {
            "reclassified_amount": round(reclassified_amount, 2),
            "reclassified_pct": round(reclass_pct * 100, 2),
            "year1_deduction_accelerated": round(accelerated_year1, 2),
            "year1_deduction_straight_line": round(straight_line, 2),
            "npv_tax_savings": round(npv, 2),
            "payback_period_years": round(payback, 2),
            "study_cost_estimate": round(study_cost, 2),
        }
        return {
            "status": "success",
            "data": data,
            "timestamp": datetime.now(timezone.utc).isoformat(),
        }
    except Exception as exc:  # noqa: BLE001
        _log_lesson("cost_segregation_estimator", str(exc))
        return {
            "status": "error",
            "data": {"error": str(exc)},
            "timestamp": datetime.now(timezone.utc).isoformat(),
        }


def _log_lesson(skill_name: str, error: str) -> None:
    with open("logs/lessons.md", "a", encoding="utf-8") as handle:
        handle.write(f"- [{datetime.now(timezone.utc).isoformat()}] {skill_name}: {error}\n")
