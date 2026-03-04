"""
total_return_swap_pricer — Discounts realized equity leg cashflows against floating leg funding to output PVs, breakeven spread, and sensitivity

PREMIUM SKILL — full implementation available to subscribers.
Subscribe: https://snowdrop.ai (launching soon)

AUTO-GENERATED STUB — do not edit manually.
Source of truth: snowdrop-core/skills/premium/structured_products/total_return_swap_pricer.py
Regenerate: python scripts/build_public_stubs.py
"""
from __future__ import annotations  # defers annotation evaluation (PEP 563)
from typing import Any, Optional, Union  # FastMCP resolves annotations via get_type_hints()

from skills._paywall import paywall_response

TOOL_META = {
    "name": "total_return_swap_pricer",
    "tier": "premium",
    "description": "Discounts realized equity leg cashflows against floating leg funding to output PVs, breakeven spread, and sensitivity. (Premium — subscribe at https://snowdrop.ai)",
}


def total_return_swap_pricer(notional: float, reference_returns: List[float], funding_rate: float, spread_bps: float, tenor_years: float, payments_per_year: int) -> dict[str, Any]:
    """Premium skill — subscribe to access full implementation."""
    return paywall_response("total_return_swap_pricer")
