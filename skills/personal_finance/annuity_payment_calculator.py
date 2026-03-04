"""
Executive Smary: Solves for fixed annuity payments for loans or investments.
Inputs: principal (float), annual_rate (float), years (float), payments_per_year (int), annuity_type (str)
Outputs: payment_amount (float), total_paid (float), total_interest (float), amortization_summary (list)
MCP Tool Name: annuity_payment_calculator
"""
import logging
from datetime import datetime, timezone
from typing import Any

logger = logging.getLogger("snowdrop.skills")

TOOL_META = {
    "name": "annuity_payment_calculator",
    "description": (
        "Determines the periodic payment required to amortize a balance, including "
        "summary stats for total paid, interest, and early amortization snapshots."
    ),
    "inputSchema": {
        "type": "object",
        "properties": {
            "principal": {
                "type": "number",
                "description": "Amount financed or invested at present value.",
            },
            "annual_rate": {
                "type": "number",
                "description": "Nominal annual interest rate as decimal.",
            },
            "years": {
                "type": "number",
                "description": "Amortization term in years.",
            },
            "payments_per_year": {
                "type": "number",
                "description": "Number of payments per year (12 for monthly).",
            },
            "annuity_type": {
                "type": "string",
                "description": "ordinary for end-of-period, due for beginning-of-period payments.",
            },
        },
        "required": ["principal", "annual_rate", "years", "payments_per_year", "annuity_type"],
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


def annuity_payment_calculator(**kwargs: Any) -> dict:
    """Solve annuity payment and create amortization snapshots."""
    try:
        principal = float(kwargs["principal"])
        annual_rate = float(kwargs["annual_rate"])
        years = float(kwargs["years"])
        payments_per_year = int(kwargs["payments_per_year"])
        annuity_type = str(kwargs["annuity_type"]).strip().lower()

        if principal <= 0:
            raise ValueError("principal must be positive")
        if years <= 0:
            raise ValueError("years must be positive")
        if payments_per_year <= 0:
            raise ValueError("payments_per_year must be positive")
        if annuity_type not in {"ordinary", "due"}:
            raise ValueError("annuity_type must be ordinary or due")

        periods = int(years * payments_per_year)
        period_rate = annual_rate / payments_per_year

        if period_rate == 0:
            payment = principal / periods
        else:
            discount = (1 - (1 + period_rate) ** (-periods)) / period_rate
            payment = principal / discount
            if annuity_type == "due":
                payment /= (1 + period_rate)

        total_paid = payment * periods
        total_interest = total_paid - principal

        amortization_summary = []
        balance = principal
        for n in range(1, min(periods, 12) + 1):
            interest = balance * period_rate
            principal_paid = payment - interest
            balance -= principal_paid
            amortization_summary.append(
                {
                    "payment_number": n,
                    "interest": interest,
                    "principal": principal_paid,
                    "remaining_balance": max(balance, 0.0),
                }
            )

        return {
            "status": "success",
            "data": {
                "payment_amount": payment,
                "total_paid": total_paid,
                "total_interest": total_interest,
                "amortization_summary": amortization_summary,
            },
            "timestamp": datetime.now(timezone.utc).isoformat(),
        }
    except (ValueError, TypeError, ZeroDivisionError) as e:
        logger.error(f"annuity_payment_calculator failed: {e}")
        _log_lesson(f"annuity_payment_calculator: {e}")
        return {
            "status": "error",
            "error": str(e),
            "timestamp": datetime.now(timezone.utc).isoformat(),
        }


def _log_lesson(message: str) -> None:
    try:
        with open("logs/lessons.md", "a") as f:
            f.write(f"- [{datetime.now(timezone.utc).isoformat()}] {message}\n")
    except OSError:
        pass
