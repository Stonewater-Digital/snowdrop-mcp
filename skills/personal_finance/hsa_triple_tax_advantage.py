"""
Executive Smary: Quantifies the triple tax benefit of maxing an HSA for retirement healthcare.
Inputs: annual_contribution (float), years_to_retirement (int), investment_return (float), tax_bracket (float), medical_expenses_in_retirement (float)
Outputs: tax_savings_contributions (float), tax_free_growth (float), balance_at_retirement (float), total_tax_advantage (float)
MCP Tool Name: hsa_triple_tax_advantage
"""
import logging
from datetime import datetime, timezone
from typing import Any

logger = logging.getLogger("snowdrop.skills")

TOOL_META = {
    "name": "hsa_triple_tax_advantage",
    "description": (
        "Projects HSA balances using constant contributions and growth to highlight tax "
        "savings from deductions, tax-free compounding, and qualified medical withdrawals."
    ),
    "inputSchema": {
        "type": "object",
        "properties": {
            "annual_contribution": {
                "type": "number",
                "description": "Dollars contributed to HSA each year, typically IRS maximum.",
            },
            "years_to_retirement": {
                "type": "number",
                "description": "Years remaining until retirement when HSA funds are tapped.",
            },
            "investment_return": {
                "type": "number",
                "description": "Expected annual investment return on HSA assets as decimal.",
            },
            "tax_bracket": {
                "type": "number",
                "description": "Marginal tax rate applicable today and in retirement.",
            },
            "medical_expenses_in_retirement": {
                "type": "number",
                "description": "Estimated qualified medical spend that can be reimbursed tax-free.",
            },
        },
        "required": [
            "annual_contribution",
            "years_to_retirement",
            "investment_return",
            "tax_bracket",
            "medical_expenses_in_retirement",
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


def hsa_triple_tax_advantage(**kwargs: Any) -> dict:
    """Evaluate HSA tax savings from deductions, compounding, and qualified withdrawals."""
    try:
        contribution = float(kwargs["annual_contribution"])
        years = int(kwargs["years_to_retirement"])
        investment_return = float(kwargs["investment_return"])
        tax_bracket = float(kwargs["tax_bracket"])
        medical_expenses = float(kwargs["medical_expenses_in_retirement"])

        if contribution < 0 or years < 0 or medical_expenses < 0:
            raise ValueError("contribution, years, and medical expenses must be non-negative")

        if years == 0:
            balance = contribution
        elif investment_return == 0:
            balance = contribution * years
        else:
            balance = contribution * ((1 + investment_return) ** years - 1) / investment_return

        tax_savings_contributions = contribution * years * tax_bracket
        growth = balance - contribution * years
        tax_free_growth = growth * tax_bracket
        medical_tax_savings = min(balance, medical_expenses) * tax_bracket
        total_tax_advantage = (
            tax_savings_contributions + tax_free_growth + medical_tax_savings
        )

        return {
            "status": "success",
            "data": {
                "tax_savings_contributions": tax_savings_contributions,
                "tax_free_growth": tax_free_growth,
                "balance_at_retirement": balance,
                "total_tax_advantage": total_tax_advantage,
            },
            "timestamp": datetime.now(timezone.utc).isoformat(),
        }
    except (ValueError, TypeError, ZeroDivisionError) as e:
        logger.error(f"hsa_triple_tax_advantage failed: {e}")
        _log_lesson(f"hsa_triple_tax_advantage: {e}")
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
