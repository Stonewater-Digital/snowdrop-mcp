"""Underwriting profit calculator.

Computes underwriting profit/loss, underwriting margin, combined ratio, and
return on premium for a P&C insurance portfolio or line of business.
"""
from __future__ import annotations

from typing import Any

from skills.utils import get_iso_timestamp, log_lesson

TOOL_META: dict[str, Any] = {
    "name": "underwriting_profit_calculator",
    "description": (
        "Computes underwriting profit/loss, underwriting margin, combined ratio, "
        "and return on net earned premium from earned premium, losses, and expenses."
    ),
    "inputSchema": {
        "type": "object",
        "properties": {
            "earned_premium": {
                "type": "number",
                "description": "Net earned premium for the period. Must be > 0.",
                "exclusiveMinimum": 0.0,
            },
            "incurred_losses": {
                "type": "number",
                "description": "Incurred losses including IBNR (paid + reserves). Must be >= 0.",
                "minimum": 0.0,
            },
            "underwriting_expenses": {
                "type": "number",
                "description": "Total underwriting expenses (acquisition + G&A + taxes/fees). Must be >= 0.",
                "minimum": 0.0,
            },
            "policyholder_dividends": {
                "type": "number",
                "description": "Policyholder dividends paid or accrued. Must be >= 0.",
                "default": 0.0,
                "minimum": 0.0,
            },
        },
        "required": ["earned_premium", "incurred_losses", "underwriting_expenses"],
    },
    "outputSchema": {
        "type": "object",
        "properties": {
            "status": {"type": "string", "enum": ["success", "error"]},
            "underwriting_profit": {"type": "number", "description": "EP - losses - expenses - dividends."},
            "underwriting_margin_pct": {"type": "number", "description": "Underwriting profit / EP × 100."},
            "combined_ratio_pct": {"type": "number", "description": "(Losses + expenses + dividends) / EP × 100."},
            "loss_ratio_pct": {"type": "number", "description": "Incurred losses / EP × 100."},
            "expense_ratio_pct": {"type": "number", "description": "Underwriting expenses / EP × 100."},
            "timestamp": {"type": "string", "format": "date-time"},
        },
        "required": ["status", "timestamp"],
    },
}


def underwriting_profit_calculator(
    earned_premium: float,
    incurred_losses: float,
    underwriting_expenses: float,
    policyholder_dividends: float = 0.0,
    **_: Any,
) -> dict[str, Any]:
    """Compute underwriting profit and derived ratios.

    Underwriting profit = earned_premium - incurred_losses - underwriting_expenses - policyholder_dividends
    Combined ratio      = (losses + expenses + dividends) / earned_premium × 100
    Underwriting margin = 100 - combined_ratio  (positive = profit)

    Args:
        earned_premium: Net earned premium. Must be > 0.
        incurred_losses: Incurred losses + IBNR. Must be >= 0.
        underwriting_expenses: Total underwriting expenses. Must be >= 0.
        policyholder_dividends: Dividends to policyholders; default 0.0.

    Returns:
        dict with status "success" and profitability metrics, or status "error".
    """
    try:
        if earned_premium <= 0:
            raise ValueError(f"earned_premium must be positive, got {earned_premium}")
        if incurred_losses < 0:
            raise ValueError(f"incurred_losses must be >= 0, got {incurred_losses}")
        if underwriting_expenses < 0:
            raise ValueError(f"underwriting_expenses must be >= 0, got {underwriting_expenses}")
        if policyholder_dividends < 0:
            raise ValueError(f"policyholder_dividends must be >= 0, got {policyholder_dividends}")

        total_costs = incurred_losses + underwriting_expenses + policyholder_dividends
        underwriting_profit = earned_premium - total_costs
        margin = underwriting_profit / earned_premium
        combined_ratio = total_costs / earned_premium
        loss_ratio = incurred_losses / earned_premium
        expense_ratio = underwriting_expenses / earned_premium

        return {
            "status": "success",
            "underwriting_profit": round(underwriting_profit, 2),
            "underwriting_margin_pct": round(margin * 100, 2),
            "combined_ratio_pct": round(combined_ratio * 100, 2),
            "loss_ratio_pct": round(loss_ratio * 100, 2),
            "expense_ratio_pct": round(expense_ratio * 100, 2),
            "timestamp": get_iso_timestamp(),
        }
    except (ValueError, TypeError, ZeroDivisionError) as exc:
        log_lesson(f"underwriting_profit_calculator: {exc}")
        return {"status": "error", "error": str(exc), "timestamp": get_iso_timestamp()}
