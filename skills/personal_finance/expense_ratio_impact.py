"""
Executive Smary: Shows long-term drag from fund expense ratios.
Inputs: investment_amount (float), annual_return_gross (float), expense_ratio (float), comparison_expense_ratio (float), years (int)
Outputs: balance_high_fee (float), balance_low_fee (float), fee_drag_dollars (float), fee_drag_pct (float), annual_fee_schedule (list)
MCP Tool Name: expense_ratio_impact
"""
import logging
from datetime import datetime, timezone
from typing import Any, List, Dict

logger = logging.getLogger("snowdrop.skills")

TOOL_META = {
    "name": "expense_ratio_impact",
    "description": (
        "Quantifies the difference in ending balance between two funds with different "
        "expense ratios and reports cumulative fee drag."
    ),
    "inputSchema": {
        "type": "object",
        "properties": {
            "investment_amount": {
                "type": "number",
                "description": "Initial investment in dollars.",
            },
            "annual_return_gross": {
                "type": "number",
                "description": "Gross expected annual return before fees.",
            },
            "expense_ratio": {
                "type": "number",
                "description": "Expense ratio (as decimal) of the current fund.",
            },
            "comparison_expense_ratio": {
                "type": "number",
                "description": "Expense ratio of the lower-cost alternative.",
            },
            "years": {
                "type": "number",
                "description": "Investment horizon in years.",
            },
        },
        "required": [
            "investment_amount",
            "annual_return_gross",
            "expense_ratio",
            "comparison_expense_ratio",
            "years",
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


def expense_ratio_impact(**kwargs: Any) -> dict:
    """Compare two expense ratios and quantify fee drag on portfolio growth."""
    try:
        amount = float(kwargs["investment_amount"])
        gross_return = float(kwargs["annual_return_gross"])
        high_fee = float(kwargs["expense_ratio"])
        low_fee = float(kwargs["comparison_expense_ratio"])
        years = int(kwargs["years"])

        if amount <= 0 or years <= 0:
            raise ValueError("investment_amount and years must be positive")

        balance_high = amount * (1 + gross_return - high_fee) ** years
        balance_low = amount * (1 + gross_return - low_fee) ** years
        fee_drag = balance_low - balance_high
        fee_drag_pct = fee_drag / balance_low if balance_low > 0 else 0.0

        annual_fee_schedule: List[Dict[str, float]] = []
        balance = amount
        for year in range(1, years + 1):
            gross_growth = balance * gross_return
            fee_cost = balance * high_fee
            balance = balance + gross_growth - fee_cost
            annual_fee_schedule.append({"year": year, "fees_paid": fee_cost})

        return {
            "status": "success",
            "data": {
                "balance_high_fee": balance_high,
                "balance_low_fee": balance_low,
                "fee_drag_dollars": fee_drag,
                "fee_drag_pct": fee_drag_pct,
                "annual_fee_schedule": annual_fee_schedule,
            },
            "timestamp": datetime.now(timezone.utc).isoformat(),
        }
    except (ValueError, TypeError, ZeroDivisionError) as e:
        logger.error(f"expense_ratio_impact failed: {e}")
        _log_lesson(f"expense_ratio_impact: {e}")
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
