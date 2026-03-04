"""
shout_option_pricer — Monte Carlo shout option valuation treating shout dates as discrete lookback checkpoints where locked intrinsic is preserved per Rubinstein's construction

PREMIUM SKILL — full implementation available to subscribers.
Subscribe: https://snowdrop.ai (launching soon)

AUTO-GENERATED STUB — do not edit manually.
Source of truth: snowdrop-core/skills/premium/exotic_options/shout_option_pricer.py
Regenerate: python scripts/build_public_stubs.py
"""
from __future__ import annotations  # defers annotation evaluation (PEP 563)
from typing import Any, Optional, Union  # FastMCP resolves annotations via get_type_hints()

from skills._paywall import paywall_response

TOOL_META = {
    "name": "shout_option_pricer",
    "tier": "premium",
    "description": "Monte Carlo shout option valuation treating shout dates as discrete lookback checkpoints where locked intrinsic is preserved per Rubinstein's construction. (Premium — subscribe at https://snowdrop.ai)",
}


def shout_option_pricer() -> dict[str, Any]:
    """Premium skill — subscribe to access full implementation."""
    return paywall_response("shout_option_pricer")
