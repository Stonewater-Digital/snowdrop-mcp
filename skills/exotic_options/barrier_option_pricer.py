"""
barrier_option_pricer — Monte Carlo pricer for continuously monitored barriers using Brownian-bridge correction (Broadie-Glasserman, 1997) for up/down and in/out configurations

PREMIUM SKILL — full implementation available to subscribers.
Subscribe: https://snowdrop.ai (launching soon)

AUTO-GENERATED STUB — do not edit manually.
Source of truth: snowdrop-core/skills/premium/exotic_options/barrier_option_pricer.py
Regenerate: python scripts/build_public_stubs.py
"""
from __future__ import annotations  # defers annotation evaluation (PEP 563)
from typing import Any, Optional, Union  # FastMCP resolves annotations via get_type_hints()

from skills._paywall import paywall_response

TOOL_META = {
    "name": "barrier_option_pricer",
    "tier": "premium",
    "description": "Monte Carlo pricer for continuously monitored barriers using Brownian-bridge correction (Broadie-Glasserman, 1997) for up/down and in/out configurations. (Premium — subscribe at https://snowdrop.ai)",
}


def barrier_option_pricer() -> dict[str, Any]:
    """Premium skill — subscribe to access full implementation."""
    return paywall_response("barrier_option_pricer")
