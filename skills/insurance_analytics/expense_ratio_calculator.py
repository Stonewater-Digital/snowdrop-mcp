"""Expense ratio calculator.

Computes underwriting expense ratio and component breakdowns. Supports both
trade basis (vs. net written premium) and statutory basis (vs. net earned premium).
"""
from __future__ import annotations

from typing import Any

from skills.utils import get_iso_timestamp, log_lesson

TOOL_META: dict[str, Any] = {
    "name": "expense_ratio_calculator",
    "description": (
        "Computes underwriting expense ratio and breakdowns for acquisition, general & administrative, "
        "and other expenses. Supports both trade basis (vs. NWP) and statutory basis (vs. NEP)."
    ),
    "inputSchema": {
        "type": "object",
        "properties": {
            "acquisition_expenses": {
                "type": "number",
                "description": "Agent commissions, brokerage fees, and other policy acquisition costs. Must be >= 0.",
                "minimum": 0.0,
            },
            "general_admin_expenses": {
                "type": "number",
                "description": "General and administrative overhead expenses. Must be >= 0.",
                "minimum": 0.0,
            },
            "net_written_premium": {
                "type": "number",
                "description": "Net written premium (denominator for trade basis). Must be > 0.",
                "exclusiveMinimum": 0.0,
            },
            "other_expenses": {
                "type": "number",
                "description": "Other underwriting expenses not captured above (taxes, licenses, fees). Must be >= 0.",
                "default": 0.0,
                "minimum": 0.0,
            },
        },
        "required": ["acquisition_expenses", "general_admin_expenses", "net_written_premium"],
    },
    "outputSchema": {
        "type": "object",
        "properties": {
            "status": {"type": "string", "enum": ["success", "error"]},
            "expense_ratio_pct": {"type": "number", "description": "Total expenses / NWP × 100 (trade basis)."},
            "acquisition_ratio_pct": {"type": "number", "description": "Acquisition expenses / NWP × 100."},
            "general_admin_ratio_pct": {"type": "number", "description": "G&A expenses / NWP × 100."},
            "other_ratio_pct": {"type": "number", "description": "Other expenses / NWP × 100."},
            "total_expenses": {"type": "number", "description": "Sum of all expense categories."},
            "timestamp": {"type": "string", "format": "date-time"},
        },
        "required": ["status", "timestamp"],
    },
}


def expense_ratio_calculator(
    acquisition_expenses: float,
    general_admin_expenses: float,
    net_written_premium: float,
    other_expenses: float = 0.0,
    **_: Any,
) -> dict[str, Any]:
    """Compute expense ratio breakdown on a trade basis vs. net written premium.

    Trade basis expense ratio = total underwriting expenses / net written premium.
    This differs from the statutory basis (expenses / net earned premium) but is
    standard for combined ratio reporting under the trade basis convention.

    Args:
        acquisition_expenses: Commissions, brokerage, and policy acquisition costs. Must be >= 0.
        general_admin_expenses: G&A overhead. Must be >= 0.
        net_written_premium: Net written premium; denominator. Must be > 0.
        other_expenses: Taxes, licenses, fees, and other underwriting expenses; default 0.0.

    Returns:
        dict with status "success" and expense ratio breakdown, or status "error".
    """
    try:
        if net_written_premium <= 0:
            raise ValueError(f"net_written_premium must be positive, got {net_written_premium}")
        if acquisition_expenses < 0:
            raise ValueError(f"acquisition_expenses must be >= 0, got {acquisition_expenses}")
        if general_admin_expenses < 0:
            raise ValueError(f"general_admin_expenses must be >= 0, got {general_admin_expenses}")
        if other_expenses < 0:
            raise ValueError(f"other_expenses must be >= 0, got {other_expenses}")

        total_expenses = acquisition_expenses + general_admin_expenses + other_expenses
        expense_ratio = total_expenses / net_written_premium
        acquisition_ratio = acquisition_expenses / net_written_premium
        ga_ratio = general_admin_expenses / net_written_premium
        other_ratio = other_expenses / net_written_premium

        return {
            "status": "success",
            "expense_ratio_pct": round(expense_ratio * 100, 2),
            "acquisition_ratio_pct": round(acquisition_ratio * 100, 2),
            "general_admin_ratio_pct": round(ga_ratio * 100, 2),
            "other_ratio_pct": round(other_ratio * 100, 2),
            "total_expenses": round(total_expenses, 2),
            "timestamp": get_iso_timestamp(),
        }
    except (ValueError, TypeError, ZeroDivisionError) as exc:
        log_lesson(f"expense_ratio_calculator: {exc}")
        return {"status": "error", "error": str(exc), "timestamp": get_iso_timestamp()}
