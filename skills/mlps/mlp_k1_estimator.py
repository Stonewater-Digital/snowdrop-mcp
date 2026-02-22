"""Estimate MLP K-1 tax allocations."""
from __future__ import annotations

from datetime import datetime, timezone
from typing import Any

TOOL_META: dict[str, Any] = {
    "name": "mlp_k1_estimator",
    "description": "Estimates income, return of capital, and UBTI exposure for MLP units.",
    "inputSchema": {
        "type": "object",
        "properties": {
            "dpu": {"type": "number"},
            "units_held": {"type": "integer"},
            "acquisition_cost_per_unit": {"type": "number"},
            "depreciation_allocation_pct": {"type": "number"},
            "ubti_pct": {"type": "number"},
            "section_199a_eligible_pct": {"type": "number"},
            "state_income_states": {"type": "array", "items": {"type": "string"}},
        },
        "required": ["dpu", "units_held", "acquisition_cost_per_unit", "depreciation_allocation_pct", "ubti_pct", "section_199a_eligible_pct", "state_income_states"],
    },
    "outputSchema": {
        "type": "object", "properties": {"status": {"type": "string"}, "data": {"type": "object"}, "timestamp": {"type": "string"}}},
}


def mlp_k1_estimator(
    dpu: float,
    units_held: int,
    acquisition_cost_per_unit: float,
    depreciation_allocation_pct: float,
    ubti_pct: float,
    section_199a_eligible_pct: float,
    state_income_states: list[str],
    **_: Any,
) -> dict[str, Any]:
    """Return K-1 tax estimates."""
    try:
        total_distribution = dpu * units_held
        roc = total_distribution * (depreciation_allocation_pct / 100)
        adjusted_basis = acquisition_cost_per_unit * units_held - roc
        ubti = total_distribution * (ubti_pct / 100)
        ira_concern = ubti > 1000
        section_199a = total_distribution * (section_199a_eligible_pct / 100) * 0.2
        data = {
            "k1_estimate": {
                "ordinary_income": round(total_distribution - roc, 2),
                "return_of_capital": round(roc, 2),
                "section_199a_deduction": round(section_199a, 2),
            },
            "return_of_capital": round(roc, 2),
            "adjusted_basis": round(adjusted_basis, 2),
            "ubti_exposure": round(ubti, 2),
            "ira_concern": ira_concern,
            "state_filing_required": state_income_states,
            "phantom_income_risk": "high" if adjusted_basis <= 0 else "low",
        }
        return {"status": "success", "data": data, "timestamp": datetime.now(timezone.utc).isoformat()}
    except Exception as exc:
        _log_lesson("mlp_k1_estimator", str(exc))
        return {"status": "error", "data": {"error": str(exc)}, "timestamp": datetime.now(timezone.utc).isoformat()}


def _log_lesson(skill_name: str, error: str) -> None:
    with open("logs/lessons.md", "a", encoding="utf-8") as handle:
        handle.write(f"- [{datetime.now(timezone.utc).isoformat()}] {skill_name}: {error}\n")
