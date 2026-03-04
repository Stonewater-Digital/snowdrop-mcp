"""
Executive Summary: Interest-only venture loan schedules — builds full IO + amortizing payment schedule with optional warrant valuation.
Inputs: principal (float), annual_rate (float), term_months (int), io_period_months (int),
        warrant_coverage_pct (float, optional)
Outputs: schedule (list of dicts), total_interest (float), warrant_value (float or null)
MCP Tool Name: venture_debt_amortization
"""
import os
import logging
from typing import Any
from datetime import datetime, timezone

logger = logging.getLogger("snowdrop.skills")

TOOL_META = {
    "name": "venture_debt_amortization",
    "description": (
        "Generates a complete monthly payment schedule for a venture debt instrument "
        "with an interest-only (IO) period followed by a fully-amortizing repayment "
        "period. Optionally calculates the warrant coverage value granted to the lender "
        "as a percentage of principal."
    ),
    "inputSchema": {
        "type": "object",
        "properties": {
            "principal":            {"type": "number", "description": "Loan principal in USD."},
            "annual_rate":          {"type": "number", "description": "Annual interest rate as a decimal (e.g. 0.12 for 12%)."},
            "term_months":          {"type": "integer", "description": "Total loan term in months."},
            "io_period_months":     {"type": "integer", "description": "Number of months for interest-only period."},
            "warrant_coverage_pct": {
                "type": "number",
                "description": "Warrant coverage as a percentage of principal (e.g. 20 for 20%). Optional.",
            },
        },
        "required": ["principal", "annual_rate", "term_months", "io_period_months"],
    },
    "outputSchema": {
        "type": "object",
        "properties": {
            "schedule":       {"type": "array"},
            "total_interest": {"type": "number"},
            "warrant_value":  {"type": ["number", "null"]},
            "status":         {"type": "string"},
            "timestamp":      {"type": "string"},
        },
        "required": ["schedule", "total_interest", "warrant_value", "status", "timestamp"],
    },
}


def venture_debt_amortization(
    principal: float,
    annual_rate: float,
    term_months: int,
    io_period_months: int,
    warrant_coverage_pct: float | None = None,
) -> dict[str, Any]:
    """Build a monthly payment schedule for venture debt with an IO period.

    During the IO period, each payment covers interest only — no principal reduction.
    After the IO period, the outstanding principal amortizes over the remaining months
    using standard equal-payment (annuity) logic.

    Args:
        principal (float): Initial loan amount in USD.
        annual_rate (float): Annual interest rate as a decimal (e.g. 0.12 for 12%).
        term_months (int): Total loan duration in months.
        io_period_months (int): Number of months for the interest-only phase.
            Must be < term_months.
        warrant_coverage_pct (float | None): Optional warrant coverage expressed as
            a percentage of principal (e.g. 20.0 means 20% × principal). If None,
            warrant_value is returned as null.

    Returns:
        dict with keys:
            - status (str): "success" or "error".
            - schedule (list[dict]): Monthly rows with:
                month, phase, payment, principal_payment, interest_payment, balance.
            - total_interest (float): Sum of all interest payments over the life.
            - warrant_value (float | None): USD value of warrants, or None.
            - timestamp (str): ISO 8601 UTC execution timestamp.
    """
    try:
        now_utc: datetime = datetime.now(timezone.utc)

        if io_period_months >= term_months:
            raise ValueError("io_period_months must be less than term_months.")
        if principal <= 0:
            raise ValueError("principal must be positive.")
        if annual_rate < 0:
            raise ValueError("annual_rate cannot be negative.")

        monthly_rate: float = annual_rate / 12.0
        amortizing_months: int = term_months - io_period_months
        balance: float = principal
        total_interest: float = 0.0
        schedule: list[dict[str, Any]] = []

        # --- IO Phase ---
        for month in range(1, io_period_months + 1):
            interest_payment: float = round(balance * monthly_rate, 2)
            schedule.append(
                {
                    "month":             month,
                    "phase":             "interest_only",
                    "payment":           interest_payment,
                    "principal_payment": 0.0,
                    "interest_payment":  interest_payment,
                    "balance":           round(balance, 2),
                }
            )
            total_interest += interest_payment

        # --- Amortizing Phase ---
        # Calculate equal monthly payment using annuity formula:
        # PMT = P * [r(1+r)^n] / [(1+r)^n - 1]
        if amortizing_months > 0 and balance > 0:
            if monthly_rate > 0:
                factor: float = (1.0 + monthly_rate) ** amortizing_months
                monthly_payment: float = balance * (monthly_rate * factor) / (factor - 1.0)
            else:
                # Zero-rate edge case: equal principal payments
                monthly_payment = balance / amortizing_months

            for month in range(io_period_months + 1, term_months + 1):
                interest_payment = round(balance * monthly_rate, 2)
                principal_payment: float = round(monthly_payment - interest_payment, 2)

                # Guard against floating-point overshoot on final payment
                if principal_payment > balance:
                    principal_payment = round(balance, 2)

                balance -= principal_payment
                if balance < 0.0:
                    balance = 0.0

                actual_payment: float = round(principal_payment + interest_payment, 2)
                schedule.append(
                    {
                        "month":             month,
                        "phase":             "amortizing",
                        "payment":           actual_payment,
                        "principal_payment": principal_payment,
                        "interest_payment":  interest_payment,
                        "balance":           round(balance, 2),
                    }
                )
                total_interest += interest_payment

        # --- Warrant Value ---
        warrant_value: float | None = None
        if warrant_coverage_pct is not None:
            warrant_value = round(principal * (warrant_coverage_pct / 100.0), 2)

        return {
            "status":         "success",
            "schedule":       schedule,
            "total_interest": round(total_interest, 2),
            "warrant_value":  warrant_value,
            "timestamp":      now_utc.isoformat(),
        }

    except Exception as e:
        logger.error(f"venture_debt_amortization failed: {e}")
        _log_lesson(f"venture_debt_amortization: {e}")
        return {"status": "error", "error": str(e), "timestamp": datetime.now(timezone.utc).isoformat()}


def _log_lesson(message: str) -> None:
    """Append a failure lesson to the shared lessons log.

    Args:
        message: Human-readable description of the failure.
    """
    with open("logs/lessons.md", "a") as f:
        f.write(f"- [{datetime.now(timezone.utc).isoformat()}] {message}\n")
