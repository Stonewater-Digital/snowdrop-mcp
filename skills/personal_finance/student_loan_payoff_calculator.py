"""Calculate student loan payoff timeline and total interest.

MCP Tool Name: student_loan_payoff_calculator
"""
from __future__ import annotations
from datetime import datetime, timezone
from typing import Any
import math

TOOL_META: dict[str, Any] = {
    "name": "student_loan_payoff_calculator",
    "description": "Calculate student loan payoff timeline, total interest paid, and show accelerated payment scenarios.",
    "inputSchema": {
        "type": "object",
        "properties": {
            "balance": {
                "type": "number",
                "description": "Current loan balance.",
            },
            "interest_rate": {
                "type": "number",
                "description": "Annual interest rate as percentage (e.g., 5.5 for 5.5%).",
            },
            "monthly_payment": {
                "type": "number",
                "description": "Monthly payment amount.",
            },
        },
        "required": ["balance", "interest_rate", "monthly_payment"],
    },
}


def _calculate_payoff(balance: float, annual_rate: float, monthly_payment: float) -> dict[str, Any]:
    """Calculate payoff details for a given payment amount."""
    monthly_rate = annual_rate / 100 / 12
    if monthly_payment <= balance * monthly_rate:
        return {"months": None, "total_interest": None, "payable": False}

    remaining = balance
    total_interest = 0.0
    months = 0
    max_months = 600  # 50 years safety cap

    while remaining > 0 and months < max_months:
        interest = remaining * monthly_rate
        total_interest += interest
        principal = min(monthly_payment - interest, remaining)
        remaining -= principal
        months += 1

    return {
        "months": months,
        "years": months / 12,
        "total_interest": round(total_interest, 2),
        "total_paid": round(balance + total_interest, 2),
        "payable": True,
    }


def student_loan_payoff_calculator(
    balance: float,
    interest_rate: float,
    monthly_payment: float,
) -> dict[str, Any]:
    """Calculate student loan payoff timeline and interest."""
    try:
        if balance <= 0:
            return {
                "status": "error",
                "data": {"error": "Balance must be positive."},
                "timestamp": datetime.now(timezone.utc).isoformat(),
            }

        monthly_rate = interest_rate / 100 / 12
        min_payment = balance * monthly_rate

        if monthly_payment <= min_payment:
            return {
                "status": "error",
                "data": {
                    "error": f"Monthly payment ${monthly_payment:.2f} does not cover monthly interest "
                    f"${min_payment:.2f}. Loan will never be paid off. Minimum payment needed: ${min_payment + 1:.2f}."
                },
                "timestamp": datetime.now(timezone.utc).isoformat(),
            }

        base = _calculate_payoff(balance, interest_rate, monthly_payment)

        # Accelerated scenarios
        scenarios = []
        for extra_label, extra in [("$50 extra", 50), ("$100 extra", 100), ("$200 extra", 200), ("Double payment", monthly_payment)]:
            accel = _calculate_payoff(balance, interest_rate, monthly_payment + extra)
            if accel["payable"] and base["payable"]:
                months_saved = base["months"] - accel["months"]
                interest_saved = base["total_interest"] - accel["total_interest"]
                scenarios.append({
                    "scenario": extra_label,
                    "monthly_payment": round(monthly_payment + extra, 2),
                    "months_to_payoff": accel["months"],
                    "years_to_payoff": round(accel["years"], 1),
                    "total_interest": accel["total_interest"],
                    "months_saved": months_saved,
                    "interest_saved": round(interest_saved, 2),
                })

        return {
            "status": "ok",
            "data": {
                "balance": balance,
                "interest_rate_pct": interest_rate,
                "monthly_payment": monthly_payment,
                "months_to_payoff": base["months"],
                "years_to_payoff": round(base["years"], 1),
                "total_interest": base["total_interest"],
                "total_paid": base["total_paid"],
                "accelerated_scenarios": scenarios,
                "note": "Assumes fixed interest rate and consistent payments. "
                "Extra payments toward principal can significantly reduce total interest. "
                "Consider refinancing if your credit score has improved since origination.",
            },
            "timestamp": datetime.now(timezone.utc).isoformat(),
        }
    except Exception as exc:
        return {
            "status": "error",
            "data": {"error": str(exc)},
            "timestamp": datetime.now(timezone.utc).isoformat(),
        }
