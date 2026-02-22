"""Estimate maximum debt capacity."""
from __future__ import annotations

from datetime import datetime, timezone
from typing import Any

TOOL_META: dict[str, Any] = {
    "name": "debt_capacity_calculator",
    "description": "Computes leverage and cash-flow-based debt capacity estimates.",
    "inputSchema": {
        "type": "object",
        "properties": {
            "ebitda": {"type": "number"},
            "max_leverage_ratio": {"type": "number", "default": 4.0},
            "interest_rate": {"type": "number"},
            "min_dscr": {"type": "number", "default": 1.25},
            "capex": {"type": "number"},
            "working_capital_change": {"type": "number"},
            "tax_rate": {"type": "number"},
        },
        "required": ["ebitda", "interest_rate", "capex", "working_capital_change", "tax_rate"],
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


def debt_capacity_calculator(
    ebitda: float,
    interest_rate: float,
    capex: float,
    working_capital_change: float,
    tax_rate: float,
    max_leverage_ratio: float = 4.0,
    min_dscr: float = 1.25,
    **_: Any,
) -> dict[str, Any]:
    """Return leverage and cash flow debt capacity estimates."""
    try:
        leverage_capacity = ebitda * max_leverage_ratio
        free_cash_flow = ebitda * (1 - tax_rate) - capex - working_capital_change
        annual_debt_service = free_cash_flow / min_dscr if min_dscr else 0.0
        cashflow_capacity = annual_debt_service / interest_rate if interest_rate else leverage_capacity
        binding = "cash_flow" if cashflow_capacity < leverage_capacity else "leverage"
        recommended = min(leverage_capacity, cashflow_capacity)
        implied_dscr = free_cash_flow / (recommended * interest_rate) if interest_rate and recommended else 0.0
        data = {
            "leverage_based_capacity": round(leverage_capacity, 2),
            "cashflow_based_capacity": round(cashflow_capacity, 2),
            "binding_constraint": binding,
            "recommended_debt": round(recommended, 2),
            "implied_dscr": round(implied_dscr, 2),
            "annual_debt_service": round(annual_debt_service, 2),
        }
        return {
            "status": "success",
            "data": data,
            "timestamp": datetime.now(timezone.utc).isoformat(),
        }
    except Exception as exc:  # noqa: BLE001
        _log_lesson("debt_capacity_calculator", str(exc))
        return {
            "status": "error",
            "data": {"error": str(exc)},
            "timestamp": datetime.now(timezone.utc).isoformat(),
        }


def _log_lesson(skill_name: str, error: str) -> None:
    with open("logs/lessons.md", "a", encoding="utf-8") as handle:
        handle.write(f"- [{datetime.now(timezone.utc).isoformat()}] {skill_name}: {error}\n")
