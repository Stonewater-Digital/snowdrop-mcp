"""Analyze venture-style liquidation preferences across exits."""
from __future__ import annotations

from datetime import datetime, timezone
from typing import Any

TOOL_META: dict[str, Any] = {
    "name": "venture_return_analyzer",
    "description": "Computes proceeds for preferred vs common across exit scenarios, including participation caps.",
    "inputSchema": {
        "type": "object",
        "properties": {
            "investment": {"type": "object"},
            "exit_scenarios": {"type": "array", "items": {"type": "number"}},
            "total_shares": {"type": "number"},
            "other_preferences": {"type": ["array", "null"], "default": None},
        },
        "required": ["investment", "exit_scenarios", "total_shares"],
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


def venture_return_analyzer(
    investment: dict[str, Any],
    exit_scenarios: list[float],
    total_shares: int,
    other_preferences: list[dict[str, Any]] | None = None,
    **_: Any,
) -> dict[str, Any]:
    """Return proceeds per scenario along with breakeven and MOIC."""
    try:
        amount = float(investment.get("amount", 0))
        shares = float(investment.get("shares", 0))
        liq_pref = float(investment.get("liquidation_preference", 1.0))
        participating = bool(investment.get("participating", False))
        participation_cap = investment.get("participation_cap")
        seniority = int(investment.get("seniority", 1))
        base_pps = amount / max(shares, 1)
        stack = sorted(other_preferences or [], key=lambda pref: pref.get("seniority", 1))
        scenarios_output = []
        crossover = None
        moic_list = []
        for exit_value in exit_scenarios:
            pref_stack = _preference_alloc(exit_value, amount, liq_pref, stack, seniority)
            pref_take = min(amount * liq_pref, pref_stack)
            participation_value = 0.0
            if participating:
                common_pool = max(exit_value - pref_stack, 0)
                pro_rata = shares / max(total_shares, 1)
                participation_value = common_pool * pro_rata
                if participation_cap:
                    participation_value = min(participation_value, amount * participation_cap - pref_take)
            convert_value = shares / max(total_shares, 1) * exit_value
            preferred_value = pref_take + participation_value
            method = "preferred"
            if convert_value > preferred_value:
                method = "common"
                preferred_value = convert_value
                if crossover is None:
                    crossover = exit_value
            moic = preferred_value / max(amount, 1e-6)
            moic_list.append(round(moic, 4))
            scenarios_output.append(
                {
                    "exit_value": exit_value,
                    "proceeds": round(preferred_value, 2),
                    "moic": round(moic, 4),
                    "method": method,
                }
            )
        data = {
            "scenarios": scenarios_output,
            "breakeven_exit": crossover or min(exit_scenarios),
            "moic_by_scenario": moic_list,
            "participation_value": round(sum(s["proceeds"] for s in scenarios_output) / len(scenarios_output), 2),
            "crossover_point": crossover,
        }
        return {
            "status": "success",
            "data": data,
            "timestamp": datetime.now(timezone.utc).isoformat(),
        }
    except Exception as exc:
        _log_lesson("venture_return_analyzer", str(exc))
        return {
            "status": "error",
            "data": {"error": str(exc)},
            "timestamp": datetime.now(timezone.utc).isoformat(),
        }


def _preference_alloc(exit_value: float, amount: float, liq_pref: float, stack: list[dict[str, Any]], seniority: int) -> float:
    remaining = exit_value
    for pref in stack:
        pref_amount = pref.get("amount", 0) * pref.get("liquidation_preference", 1.0)
        remaining -= min(pref_amount, remaining)
        if remaining <= 0:
            return exit_value
    return exit_value - remaining + min(amount * liq_pref, remaining)


def _log_lesson(skill_name: str, error: str) -> None:
    with open("logs/lessons.md", "a", encoding="utf-8") as handle:
        handle.write(f"- [{datetime.now(timezone.utc).isoformat()}] {skill_name}: {error}\n")
