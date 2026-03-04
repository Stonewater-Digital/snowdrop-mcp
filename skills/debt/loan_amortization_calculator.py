"""Generate loan amortization schedules."""
from __future__ import annotations

from datetime import datetime, timedelta, timezone
from typing import Any

TOOL_META: dict[str, Any] = {
    "name": "loan_amortization_calculator",
    "description": "Computes monthly payment, amortization schedule, and payoff projections.",
    "inputSchema": {
        "type": "object",
        "properties": {
            "principal": {"type": "number"},
            "annual_rate": {"type": "number"},
            "term_months": {"type": "integer"},
            "extra_monthly_payment": {"type": "number", "default": 0.0},
            "start_date": {"type": "string", "default": datetime.now(timezone.utc).date().isoformat()},
        },
        "required": ["principal", "annual_rate", "term_months"],
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


def loan_amortization_calculator(
    principal: float,
    annual_rate: float,
    term_months: int,
    extra_monthly_payment: float = 0.0,
    start_date: str | None = None,
    **_: Any,
) -> dict[str, Any]:
    """Return amortization schedule with totals."""
    try:
        if principal <= 0 or annual_rate <= 0 or term_months <= 0:
            raise ValueError("principal, rate, and term must be positive")
        monthly_rate = annual_rate / 12
        payment = principal * (monthly_rate * (1 + monthly_rate) ** term_months) / (
            (1 + monthly_rate) ** term_months - 1
        )
        payment += extra_monthly_payment
        balance = principal
        schedule: list[dict[str, Any]] = []
        total_interest = 0.0
        current_date = datetime.fromisoformat(start_date).date() if start_date else datetime.now(timezone.utc).date()
        for month in range(1, term_months + 1):
            interest = balance * monthly_rate
            principal_paid = min(payment - interest, balance)
            balance -= principal_paid
            total_interest += interest
            schedule.append(
                {
                    "month": month,
                    "date": current_date.isoformat(),
                    "payment": round(payment, 2),
                    "principal": round(principal_paid, 2),
                    "interest": round(interest, 2),
                    "remaining_balance": round(max(balance, 0.0), 2),
                }
            )
            current_date += timedelta(days=30)
            if balance <= 0:
                break
        payoff_date = schedule[-1]["date"] if schedule else None
        data = {
            "monthly_payment": round(payment, 2),
            "schedule": schedule,
            "total_interest_paid": round(total_interest, 2),
            "payoff_date": payoff_date,
        }
        return {
            "status": "success",
            "data": data,
            "timestamp": datetime.now(timezone.utc).isoformat(),
        }
    except Exception as exc:
        _log_lesson("loan_amortization_calculator", str(exc))
        return {
            "status": "error",
            "data": {"error": str(exc)},
            "timestamp": datetime.now(timezone.utc).isoformat(),
        }


def _log_lesson(skill_name: str, error: str) -> None:
    with open("logs/lessons.md", "a", encoding="utf-8") as handle:
        handle.write(f"- [{datetime.now(timezone.utc).isoformat()}] {skill_name}: {error}\n")
