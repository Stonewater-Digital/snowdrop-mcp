"""
merger_arbitrage_spread — Computes dollar and annualized spread along with implied deal probability from price-break analysis

PREMIUM SKILL — full implementation available to subscribers.
Subscribe: https://snowdrop.ai (launching soon)

AUTO-GENERATED STUB — do not edit manually.
Source of truth: snowdrop-core/skills/premium/alternative_investments/merger_arbitrage_spread.py
Regenerate: python scripts/build_public_stubs.py
"""
from __future__ import annotations  # defers annotation evaluation (PEP 563)
from typing import Any, Optional, Union  # FastMCP resolves annotations via get_type_hints()

from skills._paywall import paywall_response

TOOL_META = {
    "name": "merger_arbitrage_spread",
    "tier": "premium",
    "description": "Computes dollar and annualized spread along with implied deal probability from price-break analysis. (Premium — subscribe at https://snowdrop.ai)",
}


def merger_arbitrage_spread(target_price: float, offer_price: float, expected_close_days: int, risk_free_rate: float, break_price: float | None = None) -> dict[str, Any]:
    """Premium skill — subscribe to access full implementation."""
    return paywall_response("merger_arbitrage_spread")
