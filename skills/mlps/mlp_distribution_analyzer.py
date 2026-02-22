"""Analyze MLP distribution sustainability."""
from __future__ import annotations

from datetime import datetime, timezone
from typing import Any

TOOL_META: dict[str, Any] = {
    "name": "mlp_distribution_analyzer",
    "description": "Calculates DCF coverage, leverage, and GP take for MLP distributions.",
    "inputSchema": {
        "type": "object",
        "properties": {
            "distributable_cash_flow": {"type": "number"},
            "total_distributions": {"type": "number"},
            "gp_idr_distributions": {"type": "number"},
            "lp_distributions": {"type": "number"},
            "maintenance_capex": {"type": "number"},
            "growth_capex": {"type": "number"},
            "total_debt": {"type": "number"},
            "ebitda": {"type": "number"},
            "units_outstanding": {"type": "number"},
        },
        "required": ["distributable_cash_flow", "total_distributions", "gp_idr_distributions", "lp_distributions", "maintenance_capex", "growth_capex", "total_debt", "ebitda", "units_outstanding"],
    },
    "outputSchema": {
        "type": "object", "properties": {"status": {"type": "string"}, "data": {"type": "object"}, "timestamp": {"type": "string"}}},
}


def mlp_distribution_analyzer(
    distributable_cash_flow: float,
    total_distributions: float,
    gp_idr_distributions: float,
    lp_distributions: float,
    maintenance_capex: float,
    growth_capex: float,
    total_debt: float,
    ebitda: float,
    units_outstanding: float,
    **_: Any,
) -> dict[str, Any]:
    """Return distribution coverage metrics."""
    try:
        coverage = distributable_cash_flow / total_distributions if total_distributions else float("inf")
        dpu = lp_distributions / units_outstanding if units_outstanding else 0.0
        dcf_yield = distributable_cash_flow / (units_outstanding * dpu) * 100 if dpu else 0.0
        leverage = total_debt / ebitda if ebitda else 0.0
        gp_take = gp_idr_distributions / total_distributions * 100 if total_distributions else 0.0
        excess_dcf = distributable_cash_flow - total_distributions
        sustainable = coverage >= 1.1 and leverage < 4.5
        risk = "low" if sustainable else "high" if coverage < 1 else "moderate"
        data = {
            "dcf_coverage": round(coverage, 2),
            "dpu": round(dpu, 3),
            "dcf_yield_pct": round(dcf_yield, 2),
            "leverage_ratio": round(leverage, 2),
            "gp_take_pct": round(gp_take, 2),
            "sustainable": sustainable,
            "distribution_cut_risk": risk,
            "excess_dcf": round(excess_dcf, 2),
        }
        return {"status": "success", "data": data, "timestamp": datetime.now(timezone.utc).isoformat()}
    except Exception as exc:
        _log_lesson("mlp_distribution_analyzer", str(exc))
        return {"status": "error", "data": {"error": str(exc)}, "timestamp": datetime.now(timezone.utc).isoformat()}


def _log_lesson(skill_name: str, error: str) -> None:
    with open("logs/lessons.md", "a", encoding="utf-8") as handle:
        handle.write(f"- [{datetime.now(timezone.utc).isoformat()}] {skill_name}: {error}\n")
