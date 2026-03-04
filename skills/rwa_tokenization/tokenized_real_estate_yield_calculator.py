"""Estimate yield for tokenized real estate positions.
Combines NOI, leverage cost, and token price to derive income returns."""
from __future__ import annotations

from datetime import datetime, timezone
from typing import Any
import logging

from skills.utils import log_lesson

logger = logging.getLogger("snowdrop.skills")

TOOL_META: dict[str, Any] = {
    "name": "tokenized_real_estate_yield_calculator",
    "description": "Computes NOI yield for tokenized real estate including leverage cost adjustments.",
    "inputSchema": {
        "type": "object",
        "properties": {
            "gross_rent": {"type": "number", "description": "Annualized rental income"},
            "operating_expenses": {"type": "number", "description": "Annual operating expenses"},
            "interest_expense": {"type": "number", "description": "Annual debt service", "default": 0},
            "token_market_value": {"type": "number", "description": "Current market cap of tokens"},
        },
        "required": ["gross_rent", "operating_expenses", "token_market_value"],
    },
    "outputSchema": {
        "type": "object",
        "properties": {
            "status": {"type": "string"},
            "timestamp": {"type": "string"},
            "data": {"type": "object"},
            "error": {"type": "string"},
        },
    },
}


def tokenized_real_estate_yield_calculator(
    gross_rent: float,
    operating_expenses: float,
    token_market_value: float,
    interest_expense: float = 0.0,
    **_: Any,
) -> dict[str, Any]:
    """Calculate NOI yield for property tokens.

    Args:
        gross_rent: Total rental income.
        operating_expenses: Cost to operate the properties.
        token_market_value: Market value of outstanding tokens.
        interest_expense: Debt service cost.

    Returns:
        Dict summarizing NOI, cash yield, and levered yield.
    """
    try:
        if token_market_value <= 0:
            raise ValueError("token_market_value must be positive")
        noi = gross_rent - operating_expenses
        cash_yield_pct = noi / token_market_value * 100
        levered_cash_flow = noi - interest_expense
        levered_yield_pct = levered_cash_flow / token_market_value * 100
        data = {
            "noi": round(noi, 2),
            "cash_yield_pct": round(cash_yield_pct, 2),
            "levered_cash_flow": round(levered_cash_flow, 2),
            "levered_yield_pct": round(levered_yield_pct, 2),
        }
        return {"status": "success", "data": data, "timestamp": datetime.now(timezone.utc).isoformat()}
    except Exception as exc:  # noqa: BLE001
        logger.exception("tokenized_real_estate_yield_calculator failure: %s", exc)
        log_lesson(f"tokenized_real_estate_yield_calculator: {exc}")
        return {"status": "error", "error": str(exc), "timestamp": datetime.now(timezone.utc).isoformat()}
