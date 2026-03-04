"""
catastrophe_bond_spreads — Applies industry convention (expected loss + risk load + liquidity premium) to decompose cat bond spreads

PREMIUM SKILL — full implementation available to subscribers.
Subscribe: https://snowdrop.ai (launching soon)

AUTO-GENERATED STUB — do not edit manually.
Source of truth: snowdrop-core/skills/premium/structured_products/catastrophe_bond_spreads.py
Regenerate: python scripts/build_public_stubs.py
"""
from __future__ import annotations  # defers annotation evaluation (PEP 563)
from typing import Any, Optional, Union  # FastMCP resolves annotations via get_type_hints()

from skills._paywall import paywall_response

TOOL_META = {
    "name": "catastrophe_bond_spreads",
    "tier": "premium",
    "description": "Applies industry convention (expected loss + risk load + liquidity premium) to decompose cat bond spreads. (Premium — subscribe at https://snowdrop.ai)",
}


def catastrophe_bond_spreads(expected_loss: float, attachment_probability: float, risk_free_rate: float, market_spread: float) -> dict[str, Any]:
    """Premium skill — subscribe to access full implementation."""
    return paywall_response("catastrophe_bond_spreads")
