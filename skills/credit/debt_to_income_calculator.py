"""Calculate debt-to-income (DTI) ratio with classification.

MCP Tool Name: debt_to_income_calculator
"""
from __future__ import annotations
from datetime import datetime, timezone
from typing import Any

TOOL_META: dict[str, Any] = {
    "name": "debt_to_income_calculator",
    "description": "Calculate debt-to-income ratio. Classifies front-end and back-end DTI and provides lender risk assessment.",
    "inputSchema": {
        "type": "object",
        "properties": {
            "monthly_debt_payments": {
                "type": "number",
                "description": "Total monthly debt payments (all obligations).",
            },
            "gross_monthly_income": {
                "type": "number",
                "description": "Gross (pre-tax) monthly income.",
            },
        },
        "required": ["monthly_debt_payments", "gross_monthly_income"],
    },
}


def debt_to_income_calculator(
    monthly_debt_payments: float, gross_monthly_income: float
) -> dict[str, Any]:
    """Calculate debt-to-income ratio."""
    try:
        if gross_monthly_income <= 0:
            return {
                "status": "error",
                "data": {"error": "gross_monthly_income must be positive."},
                "timestamp": datetime.now(timezone.utc).isoformat(),
            }

        dti = (monthly_debt_payments / gross_monthly_income) * 100

        if dti <= 20:
            classification = "Excellent"
        elif dti <= 36:
            classification = "Good"
        elif dti <= 43:
            classification = "Acceptable (max for most mortgages)"
        elif dti <= 50:
            classification = "High risk"
        else:
            classification = "Very high risk"

        return {
            "status": "ok",
            "data": {
                "monthly_debt_payments": monthly_debt_payments,
                "gross_monthly_income": gross_monthly_income,
                "dti_pct": round(dti, 2),
                "classification": classification,
            },
            "timestamp": datetime.now(timezone.utc).isoformat(),
        }
    except Exception as exc:
        return {
            "status": "error",
            "data": {"error": str(exc)},
            "timestamp": datetime.now(timezone.utc).isoformat(),
        }
