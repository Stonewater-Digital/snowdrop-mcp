"""Assess vendor concentration risk."""
from __future__ import annotations

from datetime import datetime, timezone
from typing import Any

TOOL_META: dict[str, Any] = {
    "name": "vendor_risk_assessor",
    "description": "Evaluates concentration risk, SPOFs, and diversification across vendors.",
    "inputSchema": {
        "type": "object",
        "properties": {
            "vendors": {"type": "array", "items": {"type": "object"}},
        },
        "required": ["vendors"],
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


def vendor_risk_assessor(vendors: list[dict[str, Any]], **_: Any) -> dict[str, Any]:
    """Compute diversification and highlight single points of failure."""
    try:
        total_spend = sum(float(v.get("monthly_spend", 0.0)) for v in vendors)
        single_points = []
        concentration_risk = "low"
        recommendations: list[str] = []

        for vendor in vendors:
            spend = float(vendor.get("monthly_spend", 0.0))
            share = (spend / total_spend) if total_spend else 0.0
            if share > 0.5:
                concentration_risk = "high"
                recommendations.append(f"Diversify spend away from {vendor.get('name')}")
            if vendor.get("criticality") == "critical" and int(vendor.get("alternatives_count", 0)) == 0:
                single_points.append(vendor.get("name"))
                recommendations.append(f"Identify backup for {vendor.get('name')}")

        diversification_score = len([v for v in vendors if v.get("monthly_spend", 0) > 0])
        data = {
            "concentration_risk": concentration_risk,
            "single_points_of_failure": single_points,
            "diversification_score": diversification_score,
            "recommendations": recommendations,
        }
        return {
            "status": "success",
            "data": data,
            "timestamp": datetime.now(timezone.utc).isoformat(),
        }
    except Exception as exc:  # noqa: BLE001
        _log_lesson("vendor_risk_assessor", str(exc))
        return {
            "status": "error",
            "data": {"error": str(exc)},
            "timestamp": datetime.now(timezone.utc).isoformat(),
        }


def _log_lesson(skill_name: str, error: str) -> None:
    with open("logs/lessons.md", "a", encoding="utf-8") as handle:
        handle.write(f"- [{datetime.now(timezone.utc).isoformat()}] {skill_name}: {error}\n")
