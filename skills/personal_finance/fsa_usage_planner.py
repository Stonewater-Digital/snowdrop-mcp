"""Plan FSA usage to minimize use-it-or-lose-it risk.

MCP Tool Name: fsa_usage_planner
"""
from __future__ import annotations
from datetime import datetime, timezone
from typing import Any

TOOL_META: dict[str, Any] = {
    "name": "fsa_usage_planner",
    "description": "Plan Flexible Spending Account (FSA) usage by comparing annual contribution against expected expenses. Identifies surplus risk under the use-it-or-lose-it rule.",
    "inputSchema": {
        "type": "object",
        "properties": {
            "annual_contribution": {
                "type": "number",
                "description": "Annual FSA contribution amount.",
            },
            "expected_expenses": {
                "type": "array",
                "items": {
                    "type": "object",
                    "properties": {
                        "category": {"type": "string"},
                        "amount": {"type": "number"},
                    },
                    "required": ["category", "amount"],
                },
                "description": "List of expected medical/dependent care expenses with category and amount.",
            },
        },
        "required": ["annual_contribution", "expected_expenses"],
    },
}

_MAX_HEALTH_FSA_2024 = 3200
_MAX_CARRYOVER_2024 = 640


def fsa_usage_planner(
    annual_contribution: float,
    expected_expenses: list[dict[str, Any]],
) -> dict[str, Any]:
    """Plan FSA usage to minimize use-it-or-lose-it risk."""
    try:
        total_expected = sum(e.get("amount", 0) for e in expected_expenses)
        surplus = annual_contribution - total_expected
        deficit = total_expected - annual_contribution

        expense_breakdown = [
            {"category": e.get("category", "Unknown"), "amount": e.get("amount", 0)}
            for e in expected_expenses
        ]
        expense_breakdown.sort(key=lambda x: x["amount"], reverse=True)

        at_risk = max(0, surplus - _MAX_CARRYOVER_2024)

        if surplus > 0:
            if surplus <= _MAX_CARRYOVER_2024:
                risk_assessment = (
                    f"Low risk: ${surplus:.2f} surplus is within the ${_MAX_CARRYOVER_2024} carryover limit. "
                    "Unused funds should carry over to next year (if employer offers carryover provision)."
                )
            else:
                risk_assessment = (
                    f"HIGH RISK: ${surplus:.2f} surplus exceeds the ${_MAX_CARRYOVER_2024} carryover limit. "
                    f"${at_risk:.2f} at risk of forfeiture. Consider scheduling eligible expenses before year-end."
                )
        elif surplus < 0:
            risk_assessment = (
                f"No forfeiture risk: expenses exceed contribution by ${abs(surplus):.2f}. "
                "You may want to increase your FSA contribution next enrollment period."
            )
        else:
            risk_assessment = "Perfect balance: expected expenses match contribution exactly."

        suggestions = []
        if at_risk > 0:
            suggestions = [
                "Schedule dental cleanings or eye exams before year-end",
                "Purchase new prescription glasses or contact lenses",
                "Stock up on eligible OTC medications and supplies",
                "Schedule any deferred medical procedures",
                "Purchase FSA-eligible items: sunscreen, first aid kits, thermometers",
            ]

        return {
            "status": "ok",
            "data": {
                "annual_contribution": annual_contribution,
                "total_expected_expenses": round(total_expected, 2),
                "surplus_or_deficit": round(surplus, 2),
                "amount_at_risk_of_forfeiture": round(at_risk, 2),
                "max_carryover_2024": _MAX_CARRYOVER_2024,
                "risk_assessment": risk_assessment,
                "expense_breakdown": expense_breakdown,
                "spending_suggestions": suggestions if at_risk > 0 else [],
                "note": f"2024 Health FSA max: ${_MAX_HEALTH_FSA_2024}. Max carryover: ${_MAX_CARRYOVER_2024}. "
                "Employers may offer carryover OR grace period (2.5 months) but not both. Check your plan details.",
            },
            "timestamp": datetime.now(timezone.utc).isoformat(),
        }
    except Exception as exc:
        return {
            "status": "error",
            "data": {"error": str(exc)},
            "timestamp": datetime.now(timezone.utc).isoformat(),
        }
