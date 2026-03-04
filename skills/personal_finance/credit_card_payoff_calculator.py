"""
Executive Smary: Models credit card payoff timelines with comparison to minimum payments.
Inputs: balance (float), apr (float), monthly_payment (float|None), target_months (int|None)
Outputs: months_to_payoff (float), total_interest (float), total_paid (float), vs_minimum_payment (dict), interest_cost_of_minimums (float)
MCP Tool Name: credit_card_payoff_calculator
"""
import logging
from datetime import datetime, timezone
from typing import Any, Optional

logger = logging.getLogger("snowdrop.skills")

TOOL_META = {
    "name": "credit_card_payoff_calculator",
    "description": (
        "Simulates credit card amortization for a chosen payment or target timeline and "
        "compares it against paying issuer minimums."
    ),
    "inputSchema": {
        "type": "object",
        "properties": {
            "balance": {
                "type": "number",
                "description": "Current outstanding credit card balance.",
            },
            "apr": {
                "type": "number",
                "description": "Annual percentage rate expressed as decimal.",
            },
            "monthly_payment": {
                "type": "number",
                "description": "Custom monthly payment; either this or target_months is required.",
            },
            "target_months": {
                "type": "number",
                "description": "Desired months to payoff used to solve for payment if monthly_payment omitted.",
            },
        },
        "required": ["balance", "apr"],
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


def credit_card_payoff_calculator(**kwargs: Any) -> dict:
    """Estimate payoff period for a credit card balance and compare to minimum payments."""
    try:
        balance = float(kwargs["balance"])
        apr = float(kwargs["apr"])
        monthly_payment = kwargs.get("monthly_payment")
        target_months = kwargs.get("target_months")

        if balance <= 0:
            raise ValueError("balance must be positive")
        if monthly_payment is None and target_months is None:
            raise ValueError("Provide monthly_payment or target_months")

        monthly_rate = apr / 12
        payment_value: Optional[float] = None
        if monthly_payment is not None:
            payment_value = float(monthly_payment)
        else:
            months = int(target_months)
            if months <= 0:
                raise ValueError("target_months must be positive")
            if monthly_rate == 0:
                payment_value = balance / months
            else:
                factor = (1 + monthly_rate) ** months
                payment_value = balance * monthly_rate * factor / (factor - 1)

        payoff_months, total_interest, total_paid = _simulate_payoff(
            balance, monthly_rate, payment_value
        )
        min_payment = max(balance * 0.02, 25.0)
        min_months, min_interest, _ = _simulate_payoff(balance, monthly_rate, min_payment)
        vs_minimum = {
            "months_saved": min_months - payoff_months,
            "interest_saved": min_interest - total_interest,
            "minimum_payment": min_payment,
        }

        return {
            "status": "success",
            "data": {
                "months_to_payoff": payoff_months,
                "total_interest": total_interest,
                "total_paid": total_paid,
                "vs_minimum_payment": vs_minimum,
                "interest_cost_of_minimums": min_interest,
            },
            "timestamp": datetime.now(timezone.utc).isoformat(),
        }
    except (ValueError, TypeError, ZeroDivisionError) as e:
        logger.error(f"credit_card_payoff_calculator failed: {e}")
        _log_lesson(f"credit_card_payoff_calculator: {e}")
        return {
            "status": "error",
            "error": str(e),
            "timestamp": datetime.now(timezone.utc).isoformat(),
        }


def _simulate_payoff(balance: float, monthly_rate: float, payment: float) -> tuple[float, float, float]:
    if payment <= balance * monthly_rate:
        raise ValueError("Monthly payment must exceed accrued interest to reduce balance")
    months = 0
    total_interest = 0.0
    total_paid = 0.0
    while balance > 0:
        months += 1
        interest = balance * monthly_rate
        principal = payment - interest
        if principal <= 0:
            raise ValueError("Payment not sufficient to cover interest")
        if principal > balance:
            principal = balance
            payment_effective = principal + interest
        else:
            payment_effective = payment
        balance -= principal
        total_interest += interest
        total_paid += payment_effective
        if months > 600:
            break
    return months, total_interest, total_paid


def _log_lesson(message: str) -> None:
    try:
        with open("logs/lessons.md", "a") as f:
            f.write(f"- [{datetime.now(timezone.utc).isoformat()}] {message}\n")
    except OSError:
        pass
