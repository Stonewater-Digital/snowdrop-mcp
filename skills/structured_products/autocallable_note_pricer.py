"""
autocallable_note_pricer — Simulates geometric Brownian paths to estimate autocall probabilities, expected life, and fair price for a Phoenix/autocallable note

PREMIUM SKILL — full implementation available to subscribers.
Subscribe: https://snowdrop.ai (launching soon)

AUTO-GENERATED STUB — do not edit manually.
Source of truth: snowdrop-core/skills/premium/structured_products/autocallable_note_pricer.py
Regenerate: python scripts/build_public_stubs.py
"""
from __future__ import annotations  # defers annotation evaluation (PEP 563)
from typing import Any, Optional, Union  # FastMCP resolves annotations via get_type_hints()

from skills._paywall import paywall_response

TOOL_META = {
    "name": "autocallable_note_pricer",
    "tier": "premium",
    "description": "Simulates geometric Brownian paths to estimate autocall probabilities, expected life, and fair price for a Phoenix/autocallable note. (Premium — subscribe at https://snowdrop.ai)",
}


def autocallable_note_pricer(spot_price: float, volatility: float, risk_free_rate: float, coupon_rate: float, knock_in_barrier: float, autocall_barriers: List[float], observation_times: List[float], num_paths: int = 2000) -> dict[str, Any]:
    """Premium skill — subscribe to access full implementation."""
    return paywall_response("autocallable_note_pricer")
