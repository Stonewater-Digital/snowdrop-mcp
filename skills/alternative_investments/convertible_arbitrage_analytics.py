"""
convertible_arbitrage_analytics — Computes share hedge, gamma exposure, and credit/borrow carry for convert arb positions

PREMIUM SKILL — full implementation available to subscribers.
Subscribe: https://snowdrop.ai (launching soon)

AUTO-GENERATED STUB — do not edit manually.
Source of truth: snowdrop-core/skills/premium/alternative_investments/convertible_arbitrage_analytics.py
Regenerate: python scripts/build_public_stubs.py
"""
from __future__ import annotations  # defers annotation evaluation (PEP 563)
from typing import Any, Optional, Union  # FastMCP resolves annotations via get_type_hints()

from skills._paywall import paywall_response

TOOL_META = {
    "name": "convertible_arbitrage_analytics",
    "tier": "premium",
    "description": "Computes share hedge, gamma exposure, and credit/borrow carry for convert arb positions. (Premium — subscribe at https://snowdrop.ai)",
}


def convertible_arbitrage_analytics(cb_price: float, stock_price: float, delta: float, gamma: float, credit_spread: float, borrow_cost: float) -> dict[str, Any]:
    """Premium skill — subscribe to access full implementation."""
    return paywall_response("convertible_arbitrage_analytics")
