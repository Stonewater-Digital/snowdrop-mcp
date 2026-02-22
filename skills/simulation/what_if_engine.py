"""Scenario planning for business decisions."""
from __future__ import annotations

from copy import deepcopy
from datetime import datetime, timezone
from typing import Any

TOOL_META: dict[str, Any] = {
    "name": "what_if_engine",
    "description": "Applies scenario overrides to a base business case and projects outcomes.",
    "inputSchema": {
        "type": "object",
        "properties": {
            "base_case": {"type": "object"},
            "scenarios": {
                "type": "array",
                "items": {"type": "object"},
                "description": "List of scenario dicts with name and overrides.",
            },
        },
        "required": ["base_case", "scenarios"],
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


def what_if_engine(
    base_case: dict[str, Any],
    scenarios: list[dict[str, Any]],
    **_: Any,
) -> dict[str, Any]:
    """Run a 12-month projection for each scenario."""
    try:
        if not isinstance(base_case, dict):
            raise ValueError("base_case must be a dict")
        if not isinstance(scenarios, list):
            raise ValueError("scenarios must be a list")

        scenario_outcomes = []
        base_projection = _project_case("base", base_case)
        scenario_outcomes.append(base_projection)

        for scenario in scenarios:
            if not isinstance(scenario, dict):
                raise ValueError("each scenario must be a dict")
            name = str(scenario.get("name", "unnamed"))
            overrides = scenario.get("overrides", {}) or {}
            merged_case = deepcopy(base_case)
            merged_case.update(overrides)
            scenario_outcomes.append(_project_case(name, merged_case))

        comparisons = _relative_to_base(scenario_outcomes)
        result = {
            "scenario_outcomes": scenario_outcomes,
            "relative_to_base": comparisons,
        }
        return {
            "status": "success",
            "data": result,
            "timestamp": datetime.now(timezone.utc).isoformat(),
        }
    except Exception as exc:  # noqa: BLE001
        _log_lesson("what_if_engine", str(exc))
        return {
            "status": "error",
            "data": {"error": str(exc)},
            "timestamp": datetime.now(timezone.utc).isoformat(),
        }


def _project_case(name: str, case: dict[str, Any]) -> dict[str, Any]:
    revenue = float(case.get("revenue", 0.0))
    expenses = float(case.get("expenses", 0.0))
    growth_rate = float(case.get("growth_rate", 0.0))
    expense_growth = float(case.get("expense_growth_rate", 0.0))
    cash_on_hand = float(case.get("cash_on_hand", 0.0))
    other_costs = float(case.get("other_costs", 0.0))

    projection = []
    cash_balance = cash_on_hand
    runway_months = 12

    for month in range(1, 13):
        revenue = revenue * (1 + growth_rate)
        expenses = expenses * (1 + expense_growth)
        profit = revenue - (expenses + other_costs)
        cash_balance += profit
        projection.append(
            {
                "month": month,
                "revenue": round(revenue, 2),
                "expenses": round(expenses + other_costs, 2),
                "profit": round(profit, 2),
                "cash_balance": round(cash_balance, 2),
            }
        )
        if cash_balance < 0 and runway_months == 12:
            runway_months = month

    if cash_balance >= 0 and runway_months == 12:
        runway_months = 12

    return {
        "name": name,
        "assumptions": {
            "growth_rate": growth_rate,
            "expense_growth_rate": expense_growth,
            "cash_on_hand": cash_on_hand,
        },
        "month_12_revenue": projection[-1]["revenue"],
        "month_12_profit": projection[-1]["profit"],
        "runway_months": runway_months,
        "projection": projection,
    }


def _relative_to_base(outcomes: list[dict[str, Any]]) -> dict[str, Any]:
    base = next((scenario for scenario in outcomes if scenario["name"] == "base"), None)
    if not base:
        return {}
    base_revenue = base["month_12_revenue"]
    base_profit = base["month_12_profit"]
    base_runway = base["runway_months"]

    comparisons: dict[str, Any] = {}
    for scenario in outcomes:
        if scenario["name"] == "base":
            continue
        comparisons[scenario["name"]] = {
            "revenue_delta": round(scenario["month_12_revenue"] - base_revenue, 2),
            "profit_delta": round(scenario["month_12_profit"] - base_profit, 2),
            "runway_delta": scenario["runway_months"] - base_runway,
        }
    return comparisons


def _log_lesson(skill_name: str, error: str) -> None:
    with open("logs/lessons.md", "a", encoding="utf-8") as handle:
        handle.write(f"- [{datetime.now(timezone.utc).isoformat()}] {skill_name}: {error}\n")
