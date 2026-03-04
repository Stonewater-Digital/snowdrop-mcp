"""
Executive Smary: Builds a full mortgage amortization schedule with optional extra payments.
Inputs: principal (float), annual_rate (float), term_years (int), extra_payment (float)
Outputs: monthly_payment (float), total_interest (float), total_paid (float), payoff_date (str), amortization_schedule (list), interest_saved_from_extra (float)
MCP Tool Name: mortgage_amortization
"""
import calendar
import logging
from datetime import datetime, timedelta, timezone
from typing import Any

logger = logging.getLogger("snowdrop.skills")

TOOL_META = {
    "name": "mortgage_amortization",
    "description": (
        "Generates a month-by-month mortgage payoff schedule with support for extra "
        "principal payments and reports payoff timing and interest savings."
    ),
    "inputSchema": {
        "type": "object",
        "properties": {
            "principal": {
                "type": "number",
                "description": "Loan amount financed in dollars.",
            },
            "annual_rate": {
                "type": "number",
                "description": "Annual percentage rate as decimal.",
            },
            "term_years": {
                "type": "number",
                "description": "Original loan term in years.",
            },
            "extra_payment": {
                "type": "number",
                "description": "Optional extra monthly principal payment, defaults to 0.",
            },
        },
        "required": ["principal", "annual_rate", "term_years"],
    },
    "outputSchema": {
        "type": "object",
        "properties": {
            "status": {"type": "string"},
            "timestamp": {"type": "string"},
            "data": {"type": "object"},
        },
        "required": ["status", "timestamp"],
    },
}


def mortgage_amortization(**kwargs: Any) -> dict:
    """Build amortization schedule and quantify payoff acceleration from extra payments."""
    try:
        principal = float(kwargs["principal"])
        annual_rate = float(kwargs["annual_rate"])
        term_years = int(kwargs["term_years"])
        extra_payment = float(kwargs.get("extra_payment", 0))

        if principal <= 0 or term_years <= 0:
            raise ValueError("principal and term_years must be positive")
        if extra_payment < 0:
            raise ValueError("extra_payment must be non-negative")

        term_months = term_years * 12
        monthly_rate = annual_rate / 12
        if monthly_rate == 0:
            base_payment = principal / term_months
        else:
            factor = (1 + monthly_rate) ** term_months
            base_payment = principal * monthly_rate * factor / (factor - 1)
        payment = base_payment + extra_payment

        schedule = []
        balance = principal
        total_interest = 0.0
        month = 0
        while balance > 0 and month < term_months + 120:
            month += 1
            interest = balance * monthly_rate
            principal_payment = min(payment - interest, balance) if payment > interest else balance
            if principal_payment <= 0:
                raise ValueError("Payment does not cover interest; loan will negative amortize")
            balance -= principal_payment
            total_interest += interest
            schedule.append(
                {
                    "month": month,
                    "interest": interest,
                    "principal": principal_payment,
                    "remaining_balance": max(balance, 0.0),
                }
            )

        baseline_total_interest = (
            base_payment * term_months - principal if monthly_rate > 0 else 0.0
        )
        interest_saved = max(baseline_total_interest - total_interest, 0.0)
        payoff_date = _add_months(datetime.now(timezone.utc), month)

        return {
            "status": "success",
            "data": {
                "monthly_payment": payment,
                "total_interest": total_interest,
                "total_paid": payment * month,
                "payoff_date": payoff_date.isoformat(),
                "amortization_schedule": schedule,
                "interest_saved_from_extra": interest_saved,
            },
            "timestamp": datetime.now(timezone.utc).isoformat(),
        }
    except (ValueError, TypeError, ZeroDivisionError) as e:
        logger.error(f"mortgage_amortization failed: {e}")
        _log_lesson(f"mortgage_amortization: {e}")
        return {
            "status": "error",
            "error": str(e),
            "timestamp": datetime.now(timezone.utc).isoformat(),
        }


def _add_months(dt: datetime, months: int) -> datetime:
    year = dt.year + (dt.month - 1 + months) // 12
    month = (dt.month - 1 + months) % 12 + 1
    day = min(dt.day, calendar.monthrange(year, month)[1])
    return datetime(year, month, day, dt.hour, dt.minute, dt.second, tzinfo=timezone.utc)


def _log_lesson(message: str) -> None:
    try:
        with open("logs/lessons.md", "a") as f:
            f.write(f"- [{datetime.now(timezone.utc).isoformat()}] {message}\n")
    except OSError:
        pass
