"""
Executive Smary: Quantifies retirement income sources versus desired spending to flag gaps.
Inputs: desired_retirement_income (float), social_security_estimate (float), pension_estimate (float), other_income (float), portfolio_balance (float), withdrawal_rate (float)
Outputs: total_income (float), income_gap (float), additional_savings_needed (float), portfolio_withdrawal (float)
MCP Tool Name: retirement_income_gap_analyzer
"""
import logging
from datetime import datetime, timezone
from typing import Any

logger = logging.getLogger("snowdrop.skills")

TOOL_META = {
    "name": "retirement_income_gap_analyzer",
    "description": (
        "Aggregates guaranteed income sources with planned withdrawals to determine gaps "
        "versus target retirement spending and highlight additional savings required."
    ),
    "inputSchema": {
        "type": "object",
        "properties": {
            "desired_retirement_income": {
                "type": "number",
                "description": "Annual after-tax lifestyle target in dollars.",
            },
            "social_security_estimate": {
                "type": "number",
                "description": "Annual Social Security benefits, can be zero.",
            },
            "pension_estimate": {
                "type": "number",
                "description": "Annual pension income in dollars.",
            },
            "other_income": {
                "type": "number",
                "description": "Other guaranteed income sources such as annuities.",
            },
            "portfolio_balance": {
                "type": "number",
                "description": "Investable assets available for withdrawals.",
            },
            "withdrawal_rate": {
                "type": "number",
                "description": "Planned sustainable withdrawal rate as decimal.",
            },
        },
        "required": [
            "desired_retirement_income",
            "social_security_estimate",
            "pension_estimate",
            "other_income",
            "portfolio_balance",
            "withdrawal_rate",
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


def retirement_income_gap_analyzer(**kwargs: Any) -> dict:
    """Evaluate retirement income sufficiency and required savings."""
    try:
        desired_income = float(kwargs["desired_retirement_income"])
        ss_income = float(kwargs["social_security_estimate"])
        pension = float(kwargs["pension_estimate"])
        other_income = float(kwargs["other_income"])
        portfolio_balance = float(kwargs["portfolio_balance"])
        withdrawal_rate = float(kwargs["withdrawal_rate"])

        if desired_income <= 0:
            raise ValueError("desired_retirement_income must be positive")
        if withdrawal_rate < 0:
            raise ValueError("withdrawal_rate must be non-negative")
        if portfolio_balance < 0:
            raise ValueError("portfolio_balance must be non-negative")

        portfolio_withdrawal = portfolio_balance * withdrawal_rate
        total_income = ss_income + pension + other_income + portfolio_withdrawal
        income_gap = desired_income - total_income
        additional_savings_needed = (
            income_gap / withdrawal_rate if withdrawal_rate > 0 and income_gap > 0 else 0.0
        )

        return {
            "status": "success",
            "data": {
                "total_income": total_income,
                "income_gap": max(income_gap, 0.0),
                "additional_savings_needed": max(additional_savings_needed, 0.0),
                "portfolio_withdrawal": portfolio_withdrawal,
            },
            "timestamp": datetime.now(timezone.utc).isoformat(),
        }
    except (ValueError, TypeError, ZeroDivisionError) as e:
        logger.error(f"retirement_income_gap_analyzer failed: {e}")
        _log_lesson(f"retirement_income_gap_analyzer: {e}")
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
