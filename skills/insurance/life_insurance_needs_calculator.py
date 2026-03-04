"""Calculate life insurance coverage needs based on income replacement and obligations.

MCP Tool Name: life_insurance_needs_calculator
"""
from __future__ import annotations
from datetime import datetime, timezone
from typing import Any

TOOL_META: dict[str, Any] = {
    "name": "life_insurance_needs_calculator",
    "description": "Calculate life insurance needs: income replacement + outstanding debts + funeral costs - existing coverage.",
    "inputSchema": {
        "type": "object",
        "properties": {
            "annual_income": {"type": "number", "description": "Annual income to replace."},
            "years_of_income": {"type": "integer", "description": "Years of income to cover (default 10).", "default": 10},
            "outstanding_debts": {"type": "number", "description": "Total outstanding debts (default 0).", "default": 0},
            "funeral_costs": {"type": "number", "description": "Estimated funeral/burial costs (default 15000).", "default": 15000},
            "existing_coverage": {"type": "number", "description": "Existing life insurance coverage (default 0).", "default": 0},
        },
        "required": ["annual_income"],
    },
}


def life_insurance_needs_calculator(
    annual_income: float,
    years_of_income: int = 10,
    outstanding_debts: float = 0,
    funeral_costs: float = 15000,
    existing_coverage: float = 0,
) -> dict[str, Any]:
    """Calculate life insurance coverage needs."""
    try:
        income_replacement = annual_income * years_of_income
        total_need = income_replacement + outstanding_debts + funeral_costs
        gap = total_need - existing_coverage
        coverage_needed = max(gap, 0)

        return {
            "status": "ok",
            "data": {
                "annual_income": annual_income,
                "years_of_income": years_of_income,
                "income_replacement": round(income_replacement, 2),
                "outstanding_debts": outstanding_debts,
                "funeral_costs": funeral_costs,
                "total_need": round(total_need, 2),
                "existing_coverage": existing_coverage,
                "additional_coverage_needed": round(coverage_needed, 2),
            },
            "timestamp": datetime.now(timezone.utc).isoformat(),
        }
    except Exception as exc:
        return {
            "status": "error",
            "data": {"error": str(exc)},
            "timestamp": datetime.now(timezone.utc).isoformat(),
        }
