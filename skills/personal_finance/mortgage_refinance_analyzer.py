"""
Executive Smary: Evaluates refinancing trade-offs including break-even and lifetime savings.
Inputs: current_balance (float), current_rate (float), current_remaining_months (int), new_rate (float), new_term_months (int), closing_costs (float)
Outputs: monthly_savings (float), breakeven_months (float), total_savings_over_life (float), new_total_interest (float)
MCP Tool Name: mortgage_refinance_analyzer
"""
import logging
from datetime import datetime, timezone
from typing import Any

logger = logging.getLogger("snowdrop.skills")


def _payment(balance: float, rate: float, months: int) -> float:
    if months <= 0:
        raise ValueError("months must be positive")
    monthly_rate = rate / 12
    if monthly_rate == 0:
        return balance / months
    factor = (1 + monthly_rate) ** months
    return balance * monthly_rate * factor / (factor - 1)


TOOL_META = {
    "name": "mortgage_refinance_analyzer",
    "description": (
        "Compares an existing mortgage to a potential refinance by modeling monthly "
        "savings, break-even period, lifetime interest, and payoff horizon."
    ),
    "inputSchema": {
        "type": "object",
        "properties": {
            "current_balance": {
                "type": "number",
                "description": "Outstanding principal on the existing loan.",
            },
            "current_rate": {
                "type": "number",
                "description": "Current loan APR as decimal.",
            },
            "current_remaining_months": {
                "type": "number",
                "description": "Months remaining on the existing mortgage.",
            },
            "new_rate": {
                "type": "number",
                "description": "Proposed refinance APR as decimal.",
            },
            "new_term_months": {
                "type": "number",
                "description": "Term of the new loan in months.",
            },
            "closing_costs": {
                "type": "number",
                "description": "Out-of-pocket closing costs required for refinance.",
            },
        },
        "required": [
            "current_balance",
            "current_rate",
            "current_remaining_months",
            "new_rate",
            "new_term_months",
            "closing_costs",
        ],
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


def mortgage_refinance_analyzer(**kwargs: Any) -> dict:
    """Compare existing mortgage terms against a refinance scenario."""
    try:
        current_balance = float(kwargs["current_balance"])
        current_rate = float(kwargs["current_rate"])
        current_months = int(kwargs["current_remaining_months"])
        new_rate = float(kwargs["new_rate"])
        new_term_months = int(kwargs["new_term_months"])
        closing_costs = float(kwargs["closing_costs"])

        if current_balance <= 0 or current_months <= 0 or new_term_months <= 0:
            raise ValueError("balances and months must be positive")
        if closing_costs < 0:
            raise ValueError("closing_costs must be non-negative")

        current_payment = _payment(current_balance, current_rate, current_months)
        new_payment = _payment(current_balance, new_rate, new_term_months)
        monthly_savings = current_payment - new_payment
        current_total_interest = current_payment * current_months - current_balance
        new_total_interest = new_payment * new_term_months - current_balance
        total_savings_over_life = current_total_interest - (new_total_interest + closing_costs)
        breakeven_months = (
            closing_costs / monthly_savings if monthly_savings > 0 else float("inf")
        )

        return {
            "status": "success",
            "data": {
                "monthly_savings": monthly_savings,
                "breakeven_months": breakeven_months,
                "total_savings_over_life": total_savings_over_life,
                "new_total_interest": new_total_interest,
            },
            "timestamp": datetime.now(timezone.utc).isoformat(),
        }
    except (ValueError, TypeError, ZeroDivisionError) as e:
        logger.error(f"mortgage_refinance_analyzer failed: {e}")
        _log_lesson(f"mortgage_refinance_analyzer: {e}")
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
