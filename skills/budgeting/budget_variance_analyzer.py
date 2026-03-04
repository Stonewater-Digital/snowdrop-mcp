"""Analyze budget vs. actual variances."""
from __future__ import annotations

from datetime import datetime, timezone
from typing import Any

TOOL_META: dict[str, Any] = {
    "name": "budget_variance_analyzer",
    "description": "Compares actuals to budget with variance labeling and assessments.",
    "inputSchema": {
        "type": "object",
        "properties": {
            "budget": {"type": "array", "items": {"type": "object"}},
            "actuals": {"type": "array", "items": {"type": "object"}},
            "period": {"type": "string"},
        },
        "required": ["budget", "actuals", "period"],
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


def budget_variance_analyzer(
    budget: list[dict[str, Any]],
    actuals: list[dict[str, Any]],
    period: str,
    **_: Any,
) -> dict[str, Any]:
    """Calculate budget variances and overall assessment."""
    try:
        budget_map = {item.get("category", "misc"): float(item.get("budgeted_amount", 0.0)) for item in budget}
        variances = []
        total_variance = 0.0
        material_variances: list[dict[str, Any]] = []

        for actual in actuals:
            category = actual.get("category", "misc")
            actual_amount = float(actual.get("actual_amount", 0.0))
            budgeted = budget_map.pop(category, 0.0)
            variance = actual_amount - budgeted
            variance_pct = (variance / budgeted) if budgeted else 0.0
            classification = "favorable" if variance <= 0 else "unfavorable"
            material = abs(variance_pct) >= 0.10
            entry = {
                "category": category,
                "budgeted": round(budgeted, 2),
                "actual": round(actual_amount, 2),
                "variance": round(variance, 2),
                "variance_pct": round(variance_pct, 4),
                "classification": classification,
                "material": material,
            }
            variances.append(entry)
            total_variance += variance
            if material:
                material_variances.append(entry)

        for category, remaining in budget_map.items():
            entry = {
                "category": category,
                "budgeted": round(remaining, 2),
                "actual": 0.0,
                "variance": round(-remaining, 2),
                "variance_pct": -1.0,
                "classification": "favorable",
                "material": True,
            }
            variances.append(entry)
            total_variance -= remaining
            material_variances.append(entry)

        assessment = _overall_assessment(total_variance, material_variances)
        data = {
            "period": period,
            "variances": variances,
            "total_variance": round(total_variance, 2),
            "material_variances": material_variances,
            "overall_assessment": assessment,
        }
        return {
            "status": "success",
            "data": data,
            "timestamp": datetime.now(timezone.utc).isoformat(),
        }
    except Exception as exc:  # noqa: BLE001
        _log_lesson("budget_variance_analyzer", str(exc))
        return {
            "status": "error",
            "data": {"error": str(exc)},
            "timestamp": datetime.now(timezone.utc).isoformat(),
        }


def _overall_assessment(total: float, materials: list[dict[str, Any]]) -> str:
    if abs(total) < 1 and not materials:
        return "on_budget"
    if total <= 0 and len(materials) <= 2:
        return "slightly_favorable"
    if total > 0 and len(materials) > 3:
        return "material_overspend"
    if total > 0:
        return "unfavorable"
    return "favorable"


def _log_lesson(skill_name: str, error: str) -> None:
    with open("logs/lessons.md", "a", encoding="utf-8") as handle:
        handle.write(f"- [{datetime.now(timezone.utc).isoformat()}] {skill_name}: {error}\n")
