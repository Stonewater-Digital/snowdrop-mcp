"""Calculate net operating income (NOI) for a property.

MCP Tool Name: net_operating_income_calculator
"""
from __future__ import annotations
from datetime import datetime, timezone
from typing import Any

TOOL_META: dict[str, Any] = {
    "name": "net_operating_income_calculator",
    "description": "Calculate net operating income (NOI) from gross income, vacancy rate, and operating expenses. NOI = Effective Gross Income - Operating Expenses.",
    "inputSchema": {
        "type": "object",
        "properties": {
            "gross_income": {
                "type": "number",
                "description": "Potential gross annual rental income in USD.",
            },
            "vacancy_rate": {
                "type": "number",
                "description": "Expected vacancy rate as a decimal (e.g. 0.05 for 5%).",
                "default": 0.05,
            },
            "operating_expenses": {
                "type": "number",
                "description": "Total annual operating expenses (property tax, insurance, maintenance, management, etc.) in USD.",
                "default": 0,
            },
        },
        "required": ["gross_income"],
    },
}


def net_operating_income_calculator(
    gross_income: float,
    vacancy_rate: float = 0.05,
    operating_expenses: float = 0,
) -> dict[str, Any]:
    """Calculate net operating income."""
    try:
        if gross_income < 0:
            return {
                "status": "error",
                "data": {"error": "gross_income must be non-negative."},
                "timestamp": datetime.now(timezone.utc).isoformat(),
            }
        if not 0 <= vacancy_rate <= 1:
            return {
                "status": "error",
                "data": {"error": "vacancy_rate must be between 0 and 1."},
                "timestamp": datetime.now(timezone.utc).isoformat(),
            }

        vacancy_loss = gross_income * vacancy_rate
        effective_gross_income = gross_income - vacancy_loss
        noi = effective_gross_income - operating_expenses
        expense_ratio = (operating_expenses / effective_gross_income * 100) if effective_gross_income > 0 else 0.0

        return {
            "status": "ok",
            "data": {
                "potential_gross_income": round(gross_income, 2),
                "vacancy_rate_pct": round(vacancy_rate * 100, 2),
                "vacancy_loss": round(vacancy_loss, 2),
                "effective_gross_income": round(effective_gross_income, 2),
                "operating_expenses": round(operating_expenses, 2),
                "expense_ratio_pct": round(expense_ratio, 2),
                "net_operating_income": round(noi, 2),
                "monthly_noi": round(noi / 12, 2),
            },
            "timestamp": datetime.now(timezone.utc).isoformat(),
        }
    except Exception as exc:
        return {
            "status": "error",
            "data": {"error": str(exc)},
            "timestamp": datetime.now(timezone.utc).isoformat(),
        }
