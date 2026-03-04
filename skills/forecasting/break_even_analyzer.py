"""Break-even calculator for unit economics."""
from __future__ import annotations

from datetime import datetime, timezone
from typing import Any

TOOL_META: dict[str, Any] = {
    "name": "break_even_analyzer",
    "description": "Computes break-even units, revenue, margin of safety, and estimated time to break even.",
    "inputSchema": {
        "type": "object",
        "properties": {
            "fixed_costs_monthly": {"type": "number"},
            "variable_cost_per_unit": {"type": "number"},
            "price_per_unit": {"type": "number"},
            "current_monthly_units": {"type": "integer"},
        },
        "required": [
            "fixed_costs_monthly",
            "variable_cost_per_unit",
            "price_per_unit",
            "current_monthly_units",
        ],
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


def break_even_analyzer(
    fixed_costs_monthly: float,
    variable_cost_per_unit: float,
    price_per_unit: float,
    current_monthly_units: int,
    **_: Any,
) -> dict[str, Any]:
    """Return break-even metrics for the operating plan."""
    try:
        if price_per_unit <= variable_cost_per_unit:
            raise ValueError("price_per_unit must exceed variable_cost_per_unit")
        contribution_margin = price_per_unit - variable_cost_per_unit
        break_even_units = fixed_costs_monthly / contribution_margin
        break_even_revenue = break_even_units * price_per_unit
        margin_of_safety = (
            (current_monthly_units - break_even_units) / break_even_units if break_even_units else 0
        )
        months_to_break_even = _months_to_break_even(current_monthly_units, break_even_units)

        data = {
            "break_even_units": round(break_even_units, 2),
            "break_even_revenue": round(break_even_revenue, 2),
            "margin_of_safety_pct": round(margin_of_safety * 100, 2),
            "months_to_break_even": months_to_break_even,
        }
        return {
            "status": "success",
            "data": data,
            "timestamp": datetime.now(timezone.utc).isoformat(),
        }
    except Exception as exc:
        _log_lesson("break_even_analyzer", str(exc))
        return {
            "status": "error",
            "data": {"error": str(exc)},
            "timestamp": datetime.now(timezone.utc).isoformat(),
        }


def _months_to_break_even(current_units: int, break_even_units: float) -> float:
    if current_units <= 0:
        return float("inf")
    if current_units >= break_even_units:
        return 0.0
    assumed_growth = max(1, current_units * 0.1)
    months_needed = (break_even_units - current_units) / assumed_growth
    return round(months_needed, 1)


def _log_lesson(skill_name: str, error: str) -> None:
    with open("logs/lessons.md", "a", encoding="utf-8") as handle:
        handle.write(f"- [{datetime.now(timezone.utc).isoformat()}] {skill_name}: {error}\n")
