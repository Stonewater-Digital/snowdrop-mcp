"""Calculate years to Lean FIRE (financial independence at reduced expenses).

MCP Tool Name: lean_fire_calculator
"""
from __future__ import annotations
from datetime import datetime, timezone
from typing import Any

TOOL_META: dict[str, Any] = {
    "name": "lean_fire_calculator",
    "description": "Calculates Lean FIRE target (25x of 60% of normal expenses) and years to achieve it.",
    "inputSchema": {
        "type": "object",
        "properties": {
            "annual_expenses": {
                "type": "number",
                "description": "Current annual living expenses in dollars.",
            },
            "current_savings": {
                "type": "number",
                "description": "Current total invested savings in dollars.",
            },
            "annual_savings": {
                "type": "number",
                "description": "Amount saved and invested per year in dollars.",
            },
            "expected_return": {
                "type": "number",
                "description": "Expected annual real investment return as a decimal (default: 0.07).",
            },
        },
        "required": ["annual_expenses", "current_savings", "annual_savings"],
    },
}


def lean_fire_calculator(
    annual_expenses: float,
    current_savings: float,
    annual_savings: float,
    expected_return: float = 0.07,
) -> dict[str, Any]:
    """Calculates years to Lean FIRE."""
    try:
        if annual_expenses <= 0:
            return {
                "status": "error",
                "data": {"error": "Annual expenses must be a positive number."},
                "timestamp": datetime.now(timezone.utc).isoformat(),
            }
        if annual_savings <= 0:
            return {
                "status": "error",
                "data": {"error": "Annual savings must be a positive number."},
                "timestamp": datetime.now(timezone.utc).isoformat(),
            }

        lean_expenses = round(annual_expenses * 0.60, 2)
        lean_fire_number = round(lean_expenses * 25, 2)
        regular_fire_number = round(annual_expenses * 25, 2)

        if current_savings >= lean_fire_number:
            return {
                "status": "ok",
                "data": {
                    "lean_expenses": lean_expenses,
                    "lean_fire_number": lean_fire_number,
                    "regular_fire_number": regular_fire_number,
                    "current_savings": current_savings,
                    "status": "ALREADY LEAN FIRE",
                    "safe_withdrawal_annual": round(current_savings * 0.04, 2),
                    "safe_withdrawal_monthly": round(current_savings * 0.04 / 12, 2),
                },
                "timestamp": datetime.now(timezone.utc).isoformat(),
            }

        balance = current_savings
        years = 0
        max_years = 100

        while balance < lean_fire_number and years < max_years:
            balance = balance * (1 + expected_return) + annual_savings
            years += 1

        # Also calculate regular FIRE for comparison
        balance_reg = current_savings
        years_reg = 0
        while balance_reg < regular_fire_number and years_reg < max_years:
            balance_reg = balance_reg * (1 + expected_return) + annual_savings
            years_reg += 1

        savings_saved = years_reg - years

        return {
            "status": "ok",
            "data": {
                "annual_expenses": annual_expenses,
                "lean_expenses_60pct": lean_expenses,
                "lean_fire_number": lean_fire_number,
                "regular_fire_number": regular_fire_number,
                "savings_difference": round(regular_fire_number - lean_fire_number, 2),
                "current_savings": current_savings,
                "gap_to_lean_fire": round(lean_fire_number - current_savings, 2),
                "progress_pct": round((current_savings / lean_fire_number) * 100, 2),
                "annual_savings": annual_savings,
                "expected_return_pct": round(expected_return * 100, 2),
                "years_to_lean_fire": years if years < max_years else "100+",
                "years_to_regular_fire": years_reg if years_reg < max_years else "100+",
                "years_saved_vs_regular": savings_saved if years < max_years and years_reg < max_years else "N/A",
                "monthly_lean_budget": round(lean_expenses / 12, 2),
                "note": "Lean FIRE uses 60% of current expenses as the target lifestyle cost. Requires significant frugality but achieves independence faster.",
            },
            "timestamp": datetime.now(timezone.utc).isoformat(),
        }
    except Exception as exc:
        return {
            "status": "error",
            "data": {"error": str(exc)},
            "timestamp": datetime.now(timezone.utc).isoformat(),
        }
