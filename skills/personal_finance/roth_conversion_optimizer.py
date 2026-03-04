"""
Executive Smary: Estimates tax trade-offs of converting traditional IRA assets to Roth.
Inputs: traditional_ira_balance (float), current_tax_bracket (float), expected_retirement_bracket (float), conversion_amount (float), years_to_retirement (int)
Outputs: tax_cost_now (float), future_tax_saved (float), net_benefit (float), breakeven_years (float), optimal_conversion_amount (float)
MCP Tool Name: roth_conversion_optimizer
"""
import logging
from datetime import datetime, timezone
from typing import Any

logger = logging.getLogger("snowdrop.skills")

GROWTH_ASSUMPTION = 0.05

TOOL_META = {
    "name": "roth_conversion_optimizer",
    "description": (
        "Quantifies the up-front tax bill, future tax savings, and breakeven timing for a "
        "Roth conversion using bracket differentials and an assumed 5% growth rate."
    ),
    "inputSchema": {
        "type": "object",
        "properties": {
            "traditional_ira_balance": {
                "type": "number",
                "description": "Total balance in pre-tax IRA dollars.",
            },
            "current_tax_bracket": {
                "type": "number",
                "description": "Marginal federal tax rate today as decimal (e.g., 0.22).",
            },
            "expected_retirement_bracket": {
                "type": "number",
                "description": "Anticipated marginal rate in retirement as decimal.",
            },
            "conversion_amount": {
                "type": "number",
                "description": "Dollar amount you plan to convert to Roth now.",
            },
            "years_to_retirement": {
                "type": "number",
                "description": "Years until retirement when withdrawals begin.",
            },
        },
        "required": [
            "traditional_ira_balance",
            "current_tax_bracket",
            "expected_retirement_bracket",
            "conversion_amount",
            "years_to_retirement",
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


def roth_conversion_optimizer(**kwargs: Any) -> dict:
    """Evaluate Roth conversion costs, savings, and breakeven timing."""
    try:
        traditional_balance = float(kwargs["traditional_ira_balance"])
        current_bracket = float(kwargs["current_tax_bracket"])
        retirement_bracket = float(kwargs["expected_retirement_bracket"])
        conversion_amount = float(kwargs["conversion_amount"])
        years_to_retirement = int(kwargs["years_to_retirement"])

        if traditional_balance < 0 or conversion_amount < 0:
            raise ValueError("balances must be non-negative")
        if conversion_amount > traditional_balance:
            raise ValueError("conversion_amount cannot exceed traditional_ira_balance")
        if current_bracket < 0 or retirement_bracket < 0:
            raise ValueError("tax brackets must be non-negative")
        if years_to_retirement < 0:
            raise ValueError("years_to_retirement must be non-negative")

        tax_cost_now = conversion_amount * current_bracket
        future_value = conversion_amount * (1 + GROWTH_ASSUMPTION) ** years_to_retirement
        future_tax_if_no_conversion = future_value * retirement_bracket
        future_tax_saved = future_tax_if_no_conversion
        net_benefit = future_tax_saved - tax_cost_now
        breakeven_years = (
            0
            if retirement_bracket <= current_bracket
            else tax_cost_now
            / (future_value * (retirement_bracket - current_bracket) + 1e-9)
        )

        optimal_conversion_amount = conversion_amount if net_benefit >= 0 else 0.0

        return {
            "status": "success",
            "data": {
                "tax_cost_now": tax_cost_now,
                "future_tax_saved": future_tax_saved,
                "net_benefit": net_benefit,
                "breakeven_years": breakeven_years,
                "optimal_conversion_amount": optimal_conversion_amount,
            },
            "timestamp": datetime.now(timezone.utc).isoformat(),
        }
    except (ValueError, TypeError, ZeroDivisionError) as e:
        logger.error(f"roth_conversion_optimizer failed: {e}")
        _log_lesson(f"roth_conversion_optimizer: {e}")
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
