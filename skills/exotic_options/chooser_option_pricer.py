"""
chooser_option_pricer — Rubinstein chooser pricing via combination of Black-Scholes call and adjusted put legs, supporting standard and complex choosers

PREMIUM SKILL — full implementation available to subscribers.
Subscribe: https://snowdrop.ai (launching soon)

AUTO-GENERATED STUB — do not edit manually.
Source of truth: snowdrop-core/skills/premium/exotic_options/chooser_option_pricer.py
Regenerate: python scripts/build_public_stubs.py
"""
from __future__ import annotations  # defers annotation evaluation (PEP 563)
from typing import Any, Optional, Union  # FastMCP resolves annotations via get_type_hints()

from skills._paywall import paywall_response

TOOL_META = {
    "name": "chooser_option_pricer",
    "tier": "premium",
    "description": "Rubinstein chooser pricing via combination of Black-Scholes call and adjusted put legs, supporting standard and complex choosers. (Premium — subscribe at https://snowdrop.ai)",
}


def chooser_option_pricer() -> dict[str, Any]:
    """Premium skill — subscribe to access full implementation."""
    return paywall_response("chooser_option_pricer")
