"""Model MLP distribution growth."""
from __future__ import annotations

from datetime import datetime, timezone
from typing import Any

TOOL_META: dict[str, Any] = {
    "name": "mlp_dpu_growth_modeler",
    "description": "Projects DPU growth considering EBITDA growth, IDRs, and dropdowns.",
    "inputSchema": {
        "type": "object",
        "properties": {
            "current_dpu_annual": {"type": "number"},
            "ebitda": {"type": "number"},
            "ebitda_growth_rate": {"type": "number"},
            "maintenance_capex_pct": {"type": "number"},
            "leverage_target": {"type": "number"},
            "gp_idr_tier": {"type": "string"},
            "organic_growth_capex": {"type": "number"},
            "dropdown_pipeline": {"type": "array", "items": {"type": "object"}},
        },
        "required": ["current_dpu_annual", "ebitda", "ebitda_growth_rate", "maintenance_capex_pct", "leverage_target", "gp_idr_tier", "organic_growth_capex", "dropdown_pipeline"],
    },
    "outputSchema": {
        "type": "object", "properties": {"status": {"type": "string"}, "data": {"type": "object"}, "timestamp": {"type": "string"}}},
}

IDR_DRAG = {"low": 0.05, "mid": 0.15, "high": 0.3}


def mlp_dpu_growth_modeler(
    current_dpu_annual: float,
    ebitda: float,
    ebitda_growth_rate: float,
    maintenance_capex_pct: float,
    leverage_target: float,
    gp_idr_tier: str,
    organic_growth_capex: float,
    dropdown_pipeline: list[dict[str, Any]],
    **_: Any,
) -> dict[str, Any]:
    """Return DPU projection and IDR drag."""
    try:
        projected = []
        dpu = current_dpu_annual
        idr_drag = IDR_DRAG.get(gp_idr_tier, 0.1)
        dropdown_bonus = sum(item.get("ebitda_contribution", 0.0) for item in dropdown_pipeline)
        for year in range(1, 6):
            ebitda *= (1 + ebitda_growth_rate)
            dropdown_add = dropdown_bonus if any(item.get("expected_date") == year for item in dropdown_pipeline) else 0.0
            dcf = ebitda * (1 - maintenance_capex_pct / 100) + dropdown_add - organic_growth_capex
            dpu_growth = max(0.0, dcf / leverage_target) * (1 - idr_drag)
            dpu = dpu + dpu_growth
            projected.append({"year": year, "dpu": round(dpu, 3)})
        cagr = (dpu / current_dpu_annual) ** (1 / 5) - 1 if current_dpu_annual else 0.0
        data = {
            "projected_dpu": projected,
            "dpu_cagr_5yr": round(cagr, 4),
            "idr_drag_pct": idr_drag * 100,
            "dropdown_impact": {"incremental_ebitda": dropdown_bonus},
            "sustainable_growth_rate": round(ebitda_growth_rate * (1 - idr_drag), 4),
            "simplification_benefit": round(idr_drag * current_dpu_annual, 3),
        }
        return {"status": "success", "data": data, "timestamp": datetime.now(timezone.utc).isoformat()}
    except Exception as exc:
        _log_lesson("mlp_dpu_growth_modeler", str(exc))
        return {"status": "error", "data": {"error": str(exc)}, "timestamp": datetime.now(timezone.utc).isoformat()}


def _log_lesson(skill_name: str, error: str) -> None:
    with open("logs/lessons.md", "a", encoding="utf-8") as handle:
        handle.write(f"- [{datetime.now(timezone.utc).isoformat()}] {skill_name}: {error}\n")
