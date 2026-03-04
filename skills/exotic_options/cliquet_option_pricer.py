"""
cliquet_option_pricer — Monte Carlo pricing of locally capped/floored cliquet options with global collar following risk-neutral dynamics

PREMIUM SKILL — full implementation available to subscribers.
Subscribe: https://snowdrop.ai (launching soon)

AUTO-GENERATED STUB — do not edit manually.
Source of truth: snowdrop-core/skills/premium/exotic_options/cliquet_option_pricer.py
Regenerate: python scripts/build_public_stubs.py
"""
from __future__ import annotations  # defers annotation evaluation (PEP 563)
from typing import Any, Optional, Union  # FastMCP resolves annotations via get_type_hints()

from skills._paywall import paywall_response

TOOL_META = {
    "name": "cliquet_option_pricer",
    "tier": "premium",
    "description": "Monte Carlo pricing of locally capped/floored cliquet options with global collar following risk-neutral dynamics. (Premium — subscribe at https://snowdrop.ai)",
}


def cliquet_option_pricer() -> dict[str, Any]:
    """Premium skill — subscribe to access full implementation."""
    return paywall_response("cliquet_option_pricer")
