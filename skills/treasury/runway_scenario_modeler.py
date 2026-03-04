"""Model bull/base/bear treasury runway scenarios."""
from __future__ import annotations

from datetime import datetime, timezone
from typing import Any

TOOL_META: dict[str, Any] = {
    "name": "runway_scenario_modeler",
    "description": "Projects runway months under bull/base/bear net burn assumptions.",
    "inputSchema": {
        "type": "object",
        "properties": {
            "current_cash": {"type": "number"},
            "base_monthly_burn": {"type": "number"},
            "base_monthly_revenue": {"type": "number"},
        },
        "required": ["current_cash", "base_monthly_burn", "base_monthly_revenue"],
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

_SCENARIOS = {
    "bull": {"revenue_multiplier": 1.3, "burn_multiplier": 1.0},
    "base": {"revenue_multiplier": 1.0, "burn_multiplier": 1.0},
    "bear": {"revenue_multiplier": 0.7, "burn_multiplier": 1.1},
}


def runway_scenario_modeler(
    current_cash: float,
    base_monthly_burn: float,
    base_monthly_revenue: float,
    **_: Any,
) -> dict[str, Any]:
    """Return runway months and survival odds for each macro regime."""
    try:
        if current_cash < 0:
            raise ValueError("current_cash cannot be negative")
        if base_monthly_burn < 0 or base_monthly_revenue < 0:
            raise ValueError("monthly values cannot be negative")

        scenario_data: dict[str, Any] = {}
        for name, modifiers in _SCENARIOS.items():
            scenario_rev = base_monthly_revenue * modifiers["revenue_multiplier"]
            scenario_burn = base_monthly_burn * modifiers["burn_multiplier"]
            net = scenario_burn - scenario_rev
            if net <= 0:
                runway_months = float("inf")
                survival_probability = 0.95
            else:
                runway_months = round(current_cash / net, 1) if net else float("inf")
                survival_probability = max(0.05, min(0.95, current_cash / (net * 18)))
            scenario_data[name] = {
                "revenue": round(scenario_rev, 2),
                "burn": round(scenario_burn, 2),
                "net_burn": round(net, 2),
                "runway_months": runway_months,
                "survival_probability": round(survival_probability, 3),
            }

        return {
            "status": "success",
            "data": scenario_data,
            "timestamp": datetime.now(timezone.utc).isoformat(),
        }
    except Exception as exc:
        _log_lesson("runway_scenario_modeler", str(exc))
        return {
            "status": "error",
            "data": {"error": str(exc)},
            "timestamp": datetime.now(timezone.utc).isoformat(),
        }


def _log_lesson(skill_name: str, error: str) -> None:
    with open("logs/lessons.md", "a", encoding="utf-8") as handle:
        handle.write(f"- [{datetime.now(timezone.utc).isoformat()}] {skill_name}: {error}\n")
