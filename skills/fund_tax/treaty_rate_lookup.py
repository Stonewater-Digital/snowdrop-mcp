"""
treaty_rate_lookup — Returns statutory vs treaty withholding rates and article citations for major US treaties

PREMIUM SKILL — full implementation available to subscribers.
Subscribe: https://snowdrop.ai (launching soon)

AUTO-GENERATED STUB — do not edit manually.
Source of truth: snowdrop-core/skills/premium/fund_tax/treaty_rate_lookup.py
Regenerate: python scripts/build_public_stubs.py
"""
from __future__ import annotations  # defers annotation evaluation (PEP 563)
from typing import Any, Optional, Union  # FastMCP resolves annotations via get_type_hints()

from skills._paywall import paywall_response

TOOL_META = {
    "name": "treaty_rate_lookup",
    "tier": "premium",
    "description": "Returns statutory vs treaty withholding rates and article citations for major US treaties. (Premium — subscribe at https://snowdrop.ai)",
}


def treaty_rate_lookup() -> dict:
    """Premium skill — subscribe to access full implementation."""
    return paywall_response("treaty_rate_lookup")
