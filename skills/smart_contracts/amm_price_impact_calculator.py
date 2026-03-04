"""Estimate price impact for constant product AMM swaps.
Quantifies execution slippage versus mid-market for proposed trade sizes."""
from __future__ import annotations

from datetime import datetime, timezone
from typing import Any
import logging

from skills.utils import log_lesson

logger = logging.getLogger("snowdrop.skills")

TOOL_META: dict[str, Any] = {
    "name": "amm_price_impact_calculator",
    "description": "Applies constant product math to measure price impact of swapping base for quote reserves.",
    "inputSchema": {
        "type": "object",
        "properties": {
            "reserve_base": {"type": "number", "description": "Current base asset reserve"},
            "reserve_quote": {"type": "number", "description": "Current quote asset reserve"},
            "trade_size_base": {"type": "number", "description": "Amount of base asset to sell into pool"},
        },
        "required": ["reserve_base", "reserve_quote", "trade_size_base"],
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


def amm_price_impact_calculator(
    reserve_base: float,
    reserve_quote: float,
    trade_size_base: float,
    **_: Any,
) -> dict[str, Any]:
    """Calculate pre/post swap price metrics.

    Args:
        reserve_base: Amount of base asset currently stored in the AMM.
        reserve_quote: Amount of quote asset currently stored.
        trade_size_base: Quantity of base asset sent into the pool.

    Returns:
        Dict with execution price, quote received, and price impact percentage.
    """
    try:
        if trade_size_base <= 0:
            raise ValueError("trade_size_base must be positive")
        invariant = reserve_base * reserve_quote
        new_reserve_base = reserve_base + trade_size_base
        if new_reserve_base <= 0:
            raise ValueError("Resulting reserve must be positive")
        new_reserve_quote = invariant / new_reserve_base
        quote_out = reserve_quote - new_reserve_quote
        if quote_out <= 0:
            raise ValueError("Trade size too large given reserves")
        mid_price = reserve_quote / reserve_base if reserve_base else 0.0
        execution_price = quote_out / trade_size_base
        price_impact_pct = ((execution_price - mid_price) / mid_price * 100) if mid_price else 0.0
        data = {
            "quote_received": round(quote_out, 6),
            "execution_price": round(execution_price, 8),
            "mid_price": round(mid_price, 8),
            "price_impact_pct": round(price_impact_pct, 4),
        }
        return {"status": "success", "data": data, "timestamp": datetime.now(timezone.utc).isoformat()}
    except Exception as exc:  # noqa: BLE001
        logger.exception("amm_price_impact_calculator failure: %s", exc)
        log_lesson(f"amm_price_impact_calculator: {exc}")
        return {"status": "error", "error": str(exc), "timestamp": datetime.now(timezone.utc).isoformat()}
