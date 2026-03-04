"""
inflation_linker_pricer — Discounts inflation-linked coupons on the real yield curve and reports price and duration versus inflation assumptions

PREMIUM SKILL — full implementation available to subscribers.
Subscribe: https://snowdrop.ai (launching soon)

AUTO-GENERATED STUB — do not edit manually.
Source of truth: snowdrop-core/skills/premium/structured_products/inflation_linker_pricer.py
Regenerate: python scripts/build_public_stubs.py
"""
from __future__ import annotations  # defers annotation evaluation (PEP 563)
from typing import Any, Optional, Union  # FastMCP resolves annotations via get_type_hints()

from skills._paywall import paywall_response

TOOL_META = {
    "name": "inflation_linker_pricer",
    "tier": "premium",
    "description": "Discounts inflation-linked coupons on the real yield curve and reports price and duration versus inflation assumptions. (Premium — subscribe at https://snowdrop.ai)",
}


def inflation_linker_pricer(coupon_rate: float, maturity_years: int, real_yield_curve: List[float], breakeven_inflation: float, index_ratio: float) -> dict[str, Any]:
    """Premium skill — subscribe to access full implementation."""
    return paywall_response("inflation_linker_pricer")
