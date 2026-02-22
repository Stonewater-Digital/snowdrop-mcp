"""Compare current vs proposed loan scenarios."""
from __future__ import annotations

import math
from datetime import datetime, timezone
from typing import Any

TOOL_META: dict[str, Any] = {
    "name": "refinancing_analyzer",
    "description": "Evaluates refinance savings, break-even, and NPV for proposed loan terms.",
    "inputSchema": {
        "type": "object",
        "properties": {
            "current_loan": {"type": "object"},
            "proposed_loan": {"type": "object"},
            "discount_rate": {"type": "number", "default": 0.05},
        },
        "required": ["current_loan", "proposed_loan"],
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


def refinancing_analyzer(
    current_loan: dict[str, Any],
    proposed_loan: dict[str, Any],
    discount_rate: float = 0.05,
    **_: Any,
) -> dict[str, Any]:
    """Return refinance recommendation metrics."""
    try:
        remaining_balance = float(current_loan.get("remaining_balance", 0.0))
        current_rate = float(current_loan.get("rate", 0.0))
        remaining_months = int(current_loan.get("remaining_months", 0))
        current_payment = float(current_loan.get("monthly_payment", 0.0))
        proposed_rate = float(proposed_loan.get("rate", 0.0))
        proposed_term = int(proposed_loan.get("term_months", remaining_months))
        closing_costs = float(proposed_loan.get("closing_costs", 0.0))

        if remaining_months <= 0 or proposed_term <= 0:
            raise ValueError("Loan terms must be positive")

        proposed_payment = _monthly_payment(remaining_balance, proposed_rate, proposed_term)
        monthly_savings = current_payment - proposed_payment
        break_even_months = math.ceil(closing_costs / monthly_savings) if monthly_savings > 0 else math.inf
        total_interest_current = current_payment * remaining_months - remaining_balance
        total_interest_proposed = proposed_payment * proposed_term - remaining_balance + closing_costs
        total_interest_savings = total_interest_current - total_interest_proposed
        npv_savings = _npv(monthly_savings, discount_rate / 12, min(remaining_months, proposed_term)) - closing_costs
        refinance_recommended = monthly_savings > 0 and npv_savings > 0
        data = {
            "refinance_recommended": refinance_recommended,
            "monthly_savings": round(monthly_savings, 2),
            "break_even_months": break_even_months if break_even_months != math.inf else None,
            "total_interest_savings": round(total_interest_savings, 2),
            "npv_savings": round(npv_savings, 2),
        }
        return {
            "status": "success",
            "data": data,
            "timestamp": datetime.now(timezone.utc).isoformat(),
        }
    except Exception as exc:
        _log_lesson("refinancing_analyzer", str(exc))
        return {
            "status": "error",
            "data": {"error": str(exc)},
            "timestamp": datetime.now(timezone.utc).isoformat(),
        }


def _monthly_payment(principal: float, rate: float, months: int) -> float:
    monthly_rate = rate / 12
    if monthly_rate == 0:
        return principal / months
    return principal * (monthly_rate * (1 + monthly_rate) ** months) / ((1 + monthly_rate) ** months - 1)


def _npv(cash_flow: float, rate: float, periods: int) -> float:
    if rate == 0:
        return cash_flow * periods
    return cash_flow * (1 - (1 + rate) ** -periods) / rate


def _log_lesson(skill_name: str, error: str) -> None:
    with open("logs/lessons.md", "a", encoding="utf-8") as handle:
        handle.write(f"- [{datetime.now(timezone.utc).isoformat()}] {skill_name}: {error}\n")
