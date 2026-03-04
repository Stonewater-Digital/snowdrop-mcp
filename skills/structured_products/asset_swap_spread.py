"""
asset_swap_spread — Derives the par asset swap spread and constant Z-spread using swap discount factors and root-finding

PREMIUM SKILL — full implementation available to subscribers.
Subscribe: https://snowdrop.ai (launching soon)

AUTO-GENERATED STUB — do not edit manually.
Source of truth: snowdrop-core/skills/premium/structured_products/asset_swap_spread.py
Regenerate: python scripts/build_public_stubs.py
"""
from __future__ import annotations  # defers annotation evaluation (PEP 563)
from typing import Any, Optional, Union  # FastMCP resolves annotations via get_type_hints()

from skills._paywall import paywall_response

TOOL_META = {
    "name": "asset_swap_spread",
    "tier": "premium",
    "description": "Derives the par asset swap spread and constant Z-spread using swap discount factors and root-finding. (Premium — subscribe at https://snowdrop.ai)",
}


def asset_swap_spread(bond_price: float, coupon_rate: float, maturity_years: int, swap_curve: List[float]) -> dict[str, Any]:
    """Premium skill — subscribe to access full implementation."""
    return paywall_response("asset_swap_spread")
