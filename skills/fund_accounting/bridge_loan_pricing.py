"""
Executive Summary: Prices a bridge loan by computing monthly payment, total interest, effective APR, and a partial amortization schedule using standard annuity math.

Inputs: principal (float), term_months (int), base_rate (float), spread (float)
Outputs: dict with total_interest (float), monthly_payment (float), effective_apr (float), amortization_schedule (list of selected months)
MCP Tool Name: bridge_loan_pricing
"""
import os
import math
import logging
from typing import Any
from datetime import datetime, timezone

logger = logging.getLogger("snowdrop.skills")

TOOL_META = {
    "name": "bridge_loan_pricing",
    "description": (
        "Prices a fixed-rate amortizing bridge loan. Computes the monthly payment using "
        "the standard annuity formula, total interest cost, effective APR (nominal, monthly "
        "compounding), and a partial amortization schedule showing the first 3 months and "
        "final month. Rates are expressed as annual decimals (e.g. 0.05 = 5%)."
    ),
    "inputSchema": {
        "type": "object",
        "properties": {
            "principal": {
                "type": "number",
                "description": "Loan principal in dollars"
            },
            "term_months": {
                "type": "integer",
                "description": "Loan term in months (e.g. 12 for a 1-year bridge)"
            },
            "base_rate": {
                "type": "number",
                "description": "Base interest rate as annual decimal (e.g. 0.055 for SOFR+55bps base)"
            },
            "spread": {
                "type": "number",
                "description": "Lender spread as annual decimal (e.g. 0.025 for 250bps spread)"
            }
        },
        "required": ["principal", "term_months", "base_rate", "spread"]
    },
    "outputSchema": {
        "type": "object",
        "properties": {
            "total_rate_annual": {"type": "number"},
            "monthly_rate": {"type": "number"},
            "monthly_payment": {"type": "number"},
            "total_payments": {"type": "number"},
            "total_interest": {"type": "number"},
            "effective_apr": {"type": "number"},
            "amortization_schedule": {"type": "array"},
            "status": {"type": "string"},
            "timestamp": {"type": "string"}
        },
        "required": [
            "total_rate_annual", "monthly_rate", "monthly_payment",
            "total_interest", "effective_apr", "amortization_schedule",
            "status", "timestamp"
        ]
    }
}


def _monthly_payment(principal: float, monthly_rate: float, n_months: int) -> float:
    """Compute fixed monthly payment for a fully amortizing loan.

    Uses the standard annuity (present value of annuity) formula:
        PMT = P * r / (1 - (1 + r)^-n)

    For zero interest rate, payment = principal / n_months.

    Args:
        principal: Loan amount in dollars.
        monthly_rate: Monthly interest rate as decimal (annual_rate / 12).
        n_months: Total number of monthly payments.

    Returns:
        Fixed monthly payment in dollars.

    Raises:
        ValueError: If n_months is zero or principal is non-positive.
    """
    if n_months <= 0:
        raise ValueError(f"n_months must be positive, got {n_months}")
    if principal <= 0:
        raise ValueError(f"principal must be positive, got {principal}")

    if monthly_rate == 0:
        return round(principal / n_months, 6)

    payment = principal * monthly_rate / (1 - (1 + monthly_rate) ** -n_months)
    return round(payment, 6)


def _build_amortization_schedule(
    principal: float,
    monthly_rate: float,
    n_months: int,
    payment: float,
) -> list[dict]:
    """Build a full amortization schedule for the loan.

    Args:
        principal: Initial loan balance.
        monthly_rate: Monthly rate as decimal.
        n_months: Term in months.
        payment: Fixed monthly payment.

    Returns:
        List of dicts, one per month, with:
            month (int), opening_balance, interest_charge, principal_repaid,
            closing_balance, cumulative_interest.
    """
    schedule: list[dict] = []
    balance = principal
    cumulative_interest = 0.0

    for month in range(1, n_months + 1):
        interest_charge = round(balance * monthly_rate, 6)
        # Final month: pay exact remaining balance to avoid floating point drift
        if month == n_months:
            principal_repaid = round(balance, 6)
            actual_payment = round(principal_repaid + interest_charge, 6)
        else:
            principal_repaid = round(payment - interest_charge, 6)
            actual_payment = payment

        closing_balance = round(balance - principal_repaid, 6)
        # Clamp tiny floating point negatives to zero
        closing_balance = max(0.0, closing_balance)
        cumulative_interest += interest_charge

        schedule.append({
            "month": month,
            "opening_balance": round(balance, 2),
            "interest_charge": round(interest_charge, 2),
            "principal_repaid": round(principal_repaid, 2),
            "payment": round(actual_payment, 2),
            "closing_balance": round(closing_balance, 2),
            "cumulative_interest": round(cumulative_interest, 2),
        })

        balance = closing_balance

    return schedule


def _effective_apr(monthly_rate: float) -> float:
    """Compute effective APR from monthly rate using monthly compounding convention.

    Effective APR = (1 + monthly_rate)^12 - 1

    This matches the Truth-in-Lending Act (TILA) APR disclosure convention for
    monthly-compounding instruments.

    Args:
        monthly_rate: Monthly interest rate as decimal.

    Returns:
        Effective APR as decimal (e.g. 0.0834 = 8.34%).
    """
    return round((1 + monthly_rate) ** 12 - 1, 8)


def bridge_loan_pricing(**kwargs: Any) -> dict:
    """Price a bridge loan and generate amortization analytics.

    Computes total_rate = base_rate + spread, then monthly_rate = total_rate / 12.
    Monthly payment is derived from the standard present-value-of-annuity formula.
    The returned amortization_schedule contains first 3 months + final month only
    (for brevity in API responses); the full schedule is computed internally.

    Args:
        **kwargs: Keyword arguments containing:
            principal (float): Loan amount in dollars.
            term_months (int): Loan term in months.
            base_rate (float): Base rate as annual decimal (e.g. 0.055).
            spread (float): Lender spread as annual decimal (e.g. 0.025).

    Returns:
        dict: Contains:
            - status (str): 'success' or 'error'
            - data (dict):
                - total_rate_annual (float): base_rate + spread
                - monthly_rate (float): total_rate / 12
                - monthly_payment (float): Fixed monthly payment
                - total_payments (float): monthly_payment * term_months (approx)
                - total_interest (float): Total interest paid over life of loan
                - effective_apr (float): (1 + monthly_rate)^12 - 1
                - amortization_schedule (list): First 3 + last month rows
            - timestamp (str): ISO 8601 UTC timestamp
    """
    try:
        principal: float = float(kwargs.get("principal", 0))
        term_months: int = int(kwargs.get("term_months", 0))
        base_rate: float = float(kwargs.get("base_rate", 0))
        spread: float = float(kwargs.get("spread", 0))

        if principal <= 0:
            raise ValueError(f"principal must be positive, got {principal}")
        if term_months <= 0:
            raise ValueError(f"term_months must be positive, got {term_months}")
        if base_rate < 0:
            raise ValueError(f"base_rate cannot be negative, got {base_rate}")
        if spread < 0:
            raise ValueError(f"spread cannot be negative, got {spread}")

        total_rate = round(base_rate + spread, 10)
        monthly_rate = round(total_rate / 12, 10)

        payment = _monthly_payment(principal, monthly_rate, term_months)

        full_schedule = _build_amortization_schedule(principal, monthly_rate, term_months, payment)

        total_interest = sum(row["interest_charge"] for row in full_schedule)
        total_payments_actual = sum(row["payment"] for row in full_schedule)

        # Partial schedule: first 3 months + last month (avoiding duplicates for short loans)
        if term_months <= 4:
            partial_schedule = full_schedule
        else:
            partial_schedule = full_schedule[:3] + [full_schedule[-1]]
            # Mark the gap
            partial_schedule[3] = {**full_schedule[-1], "_note": f"Month {term_months} (final)"}

        apr = _effective_apr(monthly_rate)

        result = {
            "principal": principal,
            "term_months": term_months,
            "base_rate": base_rate,
            "spread": spread,
            "total_rate_annual": total_rate,
            "total_rate_annual_pct": round(total_rate * 100, 6),
            "monthly_rate": monthly_rate,
            "monthly_rate_pct": round(monthly_rate * 100, 6),
            "monthly_payment": round(payment, 2),
            "total_payments": round(total_payments_actual, 2),
            "total_interest": round(total_interest, 2),
            "interest_as_pct_of_principal": round(total_interest / principal * 100, 4),
            "effective_apr": apr,
            "effective_apr_pct": round(apr * 100, 6),
            "amortization_schedule": partial_schedule,
        }

        return {
            "status": "success",
            "data": result,
            "timestamp": datetime.now(timezone.utc).isoformat(),
        }

    except Exception as e:
        logger.error(f"bridge_loan_pricing failed: {e}")
        _log_lesson(f"bridge_loan_pricing: {e}")
        return {
            "status": "error",
            "error": str(e),
            "timestamp": datetime.now(timezone.utc).isoformat(),
        }


def _log_lesson(message: str) -> None:
    """Append an error lesson to the shared lessons log.

    Args:
        message: The lesson or error description to record.
    """
    try:
        with open("logs/lessons.md", "a") as f:
            f.write(f"- [{datetime.now(timezone.utc).isoformat()}] {message}\n")
    except OSError:
        logger.warning("Could not write to logs/lessons.md")
