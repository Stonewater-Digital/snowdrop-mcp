"""Combined ratio calculator.

Computes the combined ratio, underwriting margin, and operating ratio for
P&C insurers. Supports both trade basis and statutory basis combined ratios.
"""
from __future__ import annotations

from typing import Any

from skills.utils import get_iso_timestamp, log_lesson

TOOL_META: dict[str, Any] = {
    "name": "combined_ratio_calculator",
    "description": (
        "Computes combined ratio, underwriting margin, and operating ratio from "
        "loss, expense, and investment income ratios. Supports trade and statutory basis."
    ),
    "inputSchema": {
        "type": "object",
        "properties": {
            "loss_ratio_pct": {
                "type": "number",
                "description": "Incurred loss ratio as a percentage (e.g., 65.0 = 65%). Must be >= 0.",
                "minimum": 0.0,
            },
            "expense_ratio_pct": {
                "type": "number",
                "description": (
                    "Underwriting expense ratio as a percentage (e.g., 30.0 = 30%). "
                    "On trade basis: expenses / net written premium. Must be >= 0."
                ),
                "minimum": 0.0,
            },
            "policyholder_dividend_ratio_pct": {
                "type": "number",
                "description": "Policyholder dividends / earned premium %. Typically 0 for most commercial lines.",
                "default": 0.0,
                "minimum": 0.0,
            },
            "investment_income_ratio_pct": {
                "type": "number",
                "description": (
                    "Net investment income / earned premium %. Used to compute operating ratio. "
                    "Typical range 2–8%."
                ),
                "default": 0.0,
                "minimum": 0.0,
            },
        },
        "required": ["loss_ratio_pct", "expense_ratio_pct"],
    },
    "outputSchema": {
        "type": "object",
        "properties": {
            "status": {"type": "string", "enum": ["success", "error"]},
            "combined_ratio_pct": {"type": "number", "description": "Loss + expense + dividend ratios."},
            "operating_ratio_pct": {"type": "number", "description": "Combined ratio minus investment income ratio."},
            "underwriting_margin_pct": {"type": "number", "description": "100 minus combined ratio (positive = profit)."},
            "underwriting_result": {"type": "string", "enum": ["profit", "breakeven", "loss"]},
            "timestamp": {"type": "string", "format": "date-time"},
        },
        "required": ["status", "timestamp"],
    },
}


def combined_ratio_calculator(
    loss_ratio_pct: float,
    expense_ratio_pct: float,
    policyholder_dividend_ratio_pct: float = 0.0,
    investment_income_ratio_pct: float = 0.0,
    **_: Any,
) -> dict[str, Any]:
    """Compute combined ratio, operating ratio, and underwriting result.

    Combined ratio = loss_ratio + expense_ratio + policyholder_dividend_ratio
    Operating ratio = combined_ratio - investment_income_ratio
    Underwriting margin = 100 - combined_ratio

    A combined ratio below 100% indicates an underwriting profit; above 100%
    indicates an underwriting loss (which may still be offset by investment income).

    Args:
        loss_ratio_pct: Incurred loss ratio as % of earned premium. Must be >= 0.
        expense_ratio_pct: Underwriting expense ratio as % of premium. Must be >= 0.
        policyholder_dividend_ratio_pct: Dividend ratio %; default 0.0.
        investment_income_ratio_pct: Investment income ratio %; default 0.0.

    Returns:
        dict with status "success" and ratio metrics, or status "error".
    """
    try:
        if loss_ratio_pct < 0:
            raise ValueError(f"loss_ratio_pct must be >= 0, got {loss_ratio_pct}")
        if expense_ratio_pct < 0:
            raise ValueError(f"expense_ratio_pct must be >= 0, got {expense_ratio_pct}")
        if policyholder_dividend_ratio_pct < 0:
            raise ValueError(f"policyholder_dividend_ratio_pct must be >= 0, got {policyholder_dividend_ratio_pct}")
        if investment_income_ratio_pct < 0:
            raise ValueError(f"investment_income_ratio_pct must be >= 0, got {investment_income_ratio_pct}")

        combined = loss_ratio_pct + expense_ratio_pct + policyholder_dividend_ratio_pct
        operating_ratio = combined - investment_income_ratio_pct
        underwriting_margin = 100.0 - combined

        if underwriting_margin > 0:
            uw_result = "profit"
        elif underwriting_margin < 0:
            uw_result = "loss"
        else:
            uw_result = "breakeven"

        return {
            "status": "success",
            "combined_ratio_pct": round(combined, 2),
            "operating_ratio_pct": round(operating_ratio, 2),
            "underwriting_margin_pct": round(underwriting_margin, 2),
            "underwriting_result": uw_result,
            "timestamp": get_iso_timestamp(),
        }
    except (ValueError, TypeError) as exc:
        log_lesson(f"combined_ratio_calculator: {exc}")
        return {"status": "error", "error": str(exc), "timestamp": get_iso_timestamp()}
