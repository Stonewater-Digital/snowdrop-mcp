"""
variance_swap_fair_strike — Applies the continuous variance swap replication integral approximated by discrete strikes (Carr & Madan 2001)

PREMIUM SKILL — full implementation available to subscribers.
Subscribe: https://snowdrop.ai (launching soon)

AUTO-GENERATED STUB — do not edit manually.
Source of truth: snowdrop-core/skills/premium/structured_products/variance_swap_fair_strike.py
Regenerate: python scripts/build_public_stubs.py
"""
from __future__ import annotations  # defers annotation evaluation (PEP 563)
from typing import Any, Optional, Union  # FastMCP resolves annotations via get_type_hints()

from skills._paywall import paywall_response

TOOL_META = {
    "name": "variance_swap_fair_strike",
    "tier": "premium",
    "description": "Applies the continuous variance swap replication integral approximated by discrete strikes (Carr & Madan 2001). (Premium — subscribe at https://snowdrop.ai)",
}


def variance_swap_fair_strike(forward_price: float, time_to_expiry_years: float, option_chain: List[Dict[str, float]]) -> dict[str, Any]:
    """Premium skill — subscribe to access full implementation."""
    return paywall_response("variance_swap_fair_strike")
