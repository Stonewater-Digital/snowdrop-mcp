"""
quanto_option_pricer — Black-Scholes quanto pricer with correlation adjustment between asset and FX volatility (Hull, Ch

PREMIUM SKILL — full implementation available to subscribers.
Subscribe: https://snowdrop.ai (launching soon)

AUTO-GENERATED STUB — do not edit manually.
Source of truth: snowdrop-core/skills/premium/exotic_options/quanto_option_pricer.py
Regenerate: python scripts/build_public_stubs.py
"""
from __future__ import annotations  # defers annotation evaluation (PEP 563)
from typing import Any, Optional, Union  # FastMCP resolves annotations via get_type_hints()

from skills._paywall import paywall_response

TOOL_META = {
    "name": "quanto_option_pricer",
    "tier": "premium",
    "description": "Black-Scholes quanto pricer with correlation adjustment between asset and FX volatility (Hull, Ch. 28). (Premium — subscribe at https://snowdrop.ai)",
}


def quanto_option_pricer() -> dict[str, Any]:
    """Premium skill — subscribe to access full implementation."""
    return paywall_response("quanto_option_pricer")
