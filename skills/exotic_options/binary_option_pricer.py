"""
binary_option_pricer — Values digital options of cash-or-nothing or asset-or-nothing type; European payoff via Black-Scholes, American via binomial tree

PREMIUM SKILL — full implementation available to subscribers.
Subscribe: https://snowdrop.ai (launching soon)

AUTO-GENERATED STUB — do not edit manually.
Source of truth: snowdrop-core/skills/premium/exotic_options/binary_option_pricer.py
Regenerate: python scripts/build_public_stubs.py
"""
from __future__ import annotations  # defers annotation evaluation (PEP 563)
from typing import Any, Optional, Union  # FastMCP resolves annotations via get_type_hints()

from skills._paywall import paywall_response

TOOL_META = {
    "name": "binary_option_pricer",
    "tier": "premium",
    "description": "Values digital options of cash-or-nothing or asset-or-nothing type; European payoff via Black-Scholes, American via binomial tree. (Premium — subscribe at https://snowdrop.ai)",
}


def binary_option_pricer() -> dict[str, Any]:
    """Premium skill — subscribe to access full implementation."""
    return paywall_response("binary_option_pricer")
