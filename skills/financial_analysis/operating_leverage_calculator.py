"""Calculate degree of operating leverage and breakeven sensitivity."""
from __future__ import annotations

from datetime import datetime, timezone
from typing import Any

TOOL_META: dict[str, Any] = {
    "name": "operating_leverage_calculator",
    "description": "Computes contribution margin, DOL, breakeven revenue, and scenario EBIT deltas.",
    "inputSchema": {
        "type": "object",
        "properties": {
            "revenue": {"type": "number"},
            "variable_costs": {"type": "number"},
            "fixed_costs": {"type": "number"},
            "revenue_change_scenarios": {"type": "array", "items": {"type": "number"}},
        },
        "required": ["revenue", "variable_costs", "fixed_costs", "revenue_change_scenarios"],
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


def operating_leverage_calculator(
    revenue: float,
    variable_costs: float,
    fixed_costs: float,
    revenue_change_scenarios: list[float],
    **_: Any,
) -> dict[str, Any]:
    """Return DOL, breakeven, and scenario analysis."""
    try:
        contribution = revenue - variable_costs
        ebit = contribution - fixed_costs
        if contribution <= 0:
            raise ValueError("Contribution margin must be positive")
        dol = contribution / max(ebit, 1e-6)
        breakeven_revenue = fixed_costs / max(1 - variable_costs / max(revenue, 1e-6), 1e-6)
        margin_of_safety = (revenue - breakeven_revenue) / max(revenue, 1e-6) * 100
        contribution_margin_pct = contribution / max(revenue, 1e-6) * 100
        scenarios = []
        for change in revenue_change_scenarios:
            delta_ebit = dol * change * ebit
            scenarios.append(
                {
                    "revenue_change_pct": change * 100,
                    "projected_ebit": round(ebit + delta_ebit, 2),
                }
            )
        risk = "elevated" if dol > 4 else "balanced" if dol > 2 else "low"
        data = {
            "dol": round(dol, 3),
            "breakeven_revenue": round(breakeven_revenue, 2),
            "margin_of_safety_pct": round(margin_of_safety, 2),
            "contribution_margin_pct": round(contribution_margin_pct, 2),
            "scenario_analysis": scenarios,
            "risk_assessment": risk,
        }
        return {
            "status": "success",
            "data": data,
            "timestamp": datetime.now(timezone.utc).isoformat(),
        }
    except Exception as exc:
        _log_lesson("operating_leverage_calculator", str(exc))
        return {
            "status": "error",
            "data": {"error": str(exc)},
            "timestamp": datetime.now(timezone.utc).isoformat(),
        }


def _log_lesson(skill_name: str, error: str) -> None:
    with open("logs/lessons.md", "a", encoding="utf-8") as handle:
        handle.write(f"- [{datetime.now(timezone.utc).isoformat()}] {skill_name}: {error}\n")
