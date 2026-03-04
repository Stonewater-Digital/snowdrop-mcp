"""
longevity_swap_pricer — Transforms mortality qx inputs into a survival curve, discounts the floating and fixed legs, and reports PV and longevity risk premium

PREMIUM SKILL — full implementation available to subscribers.
Subscribe: https://snowdrop.ai (launching soon)

AUTO-GENERATED STUB — do not edit manually.
Source of truth: snowdrop-core/skills/premium/structured_products/longevity_swap_pricer.py
Regenerate: python scripts/build_public_stubs.py
"""
from __future__ import annotations  # defers annotation evaluation (PEP 563)
from typing import Any, Optional, Union  # FastMCP resolves annotations via get_type_hints()

from skills._paywall import paywall_response

TOOL_META = {
    "name": "longevity_swap_pricer",
    "tier": "premium",
    "description": "Transforms mortality qx inputs into a survival curve, discounts the floating and fixed legs, and reports PV and longevity risk premium. (Premium — subscribe at https://snowdrop.ai)",
}


def longevity_swap_pricer(notional: float, mortality_curve: List[Dict[str, float]], fixed_leg_payments: List[float], discount_rate: float) -> dict[str, Any]:
    """Premium skill — subscribe to access full implementation."""
    return paywall_response("longevity_swap_pricer")
