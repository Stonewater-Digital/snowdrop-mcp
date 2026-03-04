"""Calculate quarterly estimated tax payments with safe harbor rules.

MCP Tool Name: estimated_tax_payment_calculator
"""
from __future__ import annotations
from datetime import datetime, timezone
from typing import Any

TOOL_META: dict[str, Any] = {
    "name": "estimated_tax_payment_calculator",
    "description": "Calculate quarterly estimated tax payments including safe harbor rules (100%/110% of prior year tax) to avoid underpayment penalties.",
    "inputSchema": {
        "type": "object",
        "properties": {
            "expected_annual_income": {
                "type": "number",
                "description": "Expected total annual income in USD.",
            },
            "expected_withholding": {
                "type": "number",
                "description": "Total expected tax withholding for the year (from W-2 jobs, etc.) in USD.",
            },
            "prior_year_tax": {
                "type": "number",
                "description": "Total tax liability from the prior year in USD.",
            },
        },
        "required": ["expected_annual_income", "expected_withholding", "prior_year_tax"],
    },
}

# Simplified effective federal rate by income range (2024 single filer approximation)
_EFFECTIVE_RATES = [
    (11600, 0.10),
    (47150, 0.12),
    (100525, 0.18),
    (191950, 0.22),
    (243725, 0.26),
    (609350, 0.30),
    (float("inf"), 0.33),
]


def _estimate_federal_tax(income: float) -> float:
    """Rough federal tax estimate using blended effective rates."""
    for threshold, rate in _EFFECTIVE_RATES:
        if income <= threshold:
            return income * rate
    return income * 0.33


def estimated_tax_payment_calculator(
    expected_annual_income: float,
    expected_withholding: float,
    prior_year_tax: float,
) -> dict[str, Any]:
    """Calculate quarterly estimated tax payments with safe harbor rules."""
    try:
        if expected_annual_income < 0 or expected_withholding < 0 or prior_year_tax < 0:
            return {
                "status": "error",
                "data": {"error": "All amounts must be non-negative."},
                "timestamp": datetime.now(timezone.utc).isoformat(),
            }

        estimated_tax = _estimate_federal_tax(expected_annual_income)
        se_tax = 0.0  # Could be extended for self-employment
        total_expected_tax = estimated_tax + se_tax

        shortfall = max(total_expected_tax - expected_withholding, 0)

        # Safe harbor: pay at least 100% of prior year tax (110% if AGI > $150k)
        safe_harbor_100 = prior_year_tax
        safe_harbor_110 = prior_year_tax * 1.10
        is_high_income = expected_annual_income > 150000
        safe_harbor = safe_harbor_110 if is_high_income else safe_harbor_100
        safe_harbor_shortfall = max(safe_harbor - expected_withholding, 0)

        # Required estimated payments = higher of current-year or safe-harbor method
        required_annual = max(shortfall, safe_harbor_shortfall)
        quarterly_amount = required_annual / 4

        # Due dates for 2024
        due_dates = [
            "April 15, 2024 (Q1)",
            "June 17, 2024 (Q2)",
            "September 16, 2024 (Q3)",
            "January 15, 2025 (Q4)",
        ]

        return {
            "status": "ok",
            "data": {
                "expected_annual_income": round(expected_annual_income, 2),
                "estimated_federal_tax": round(estimated_tax, 2),
                "expected_withholding": round(expected_withholding, 2),
                "current_year_shortfall": round(shortfall, 2),
                "prior_year_tax": round(prior_year_tax, 2),
                "safe_harbor_method": "110% prior year" if is_high_income else "100% prior year",
                "safe_harbor_amount": round(safe_harbor, 2),
                "safe_harbor_shortfall": round(safe_harbor_shortfall, 2),
                "required_annual_estimated": round(required_annual, 2),
                "quarterly_payment": round(quarterly_amount, 2),
                "due_dates": due_dates,
                "note": "Pay the higher of current-year method or safe-harbor method to avoid underpayment penalty.",
            },
            "timestamp": datetime.now(timezone.utc).isoformat(),
        }
    except Exception as exc:
        return {
            "status": "error",
            "data": {"error": str(exc)},
            "timestamp": datetime.now(timezone.utc).isoformat(),
        }
