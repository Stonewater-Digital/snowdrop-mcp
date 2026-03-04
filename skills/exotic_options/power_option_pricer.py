"""
power_option_pricer — Closed-form pricing for type-I power options (payoff (S^n − K)^+) based on moment-adjusted Black-Scholes

PREMIUM SKILL — full implementation available to subscribers.
Subscribe: https://snowdrop.ai (launching soon)

AUTO-GENERATED STUB — do not edit manually.
Source of truth: snowdrop-core/skills/premium/exotic_options/power_option_pricer.py
Regenerate: python scripts/build_public_stubs.py
"""
from __future__ import annotations  # defers annotation evaluation (PEP 563)
from typing import Any, Optional, Union  # FastMCP resolves annotations via get_type_hints()

from skills._paywall import paywall_response

TOOL_META = {
    "name": "power_option_pricer",
    "tier": "premium",
    "description": "Closed-form pricing for type-I power options (payoff (S^n − K)^+) based on moment-adjusted Black-Scholes. (Premium — subscribe at https://snowdrop.ai)",
}


def power_option_pricer() -> dict[str, Any]:
    """Premium skill — subscribe to access full implementation."""
    return paywall_response("power_option_pricer")
