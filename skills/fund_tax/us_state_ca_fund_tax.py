"""
us_state_ca_fund_tax — Models California PIT, LLC fee, nonresident withholding, and AB 150 pass-through entity tax under Cal

PREMIUM SKILL — full implementation available to subscribers.
Subscribe: https://snowdrop.ai (launching soon)

AUTO-GENERATED STUB — do not edit manually.
Source of truth: snowdrop-core/skills/premium/fund_tax/us_state_ca_fund_tax.py
Regenerate: python scripts/build_public_stubs.py
"""
from __future__ import annotations  # defers annotation evaluation (PEP 563)
from typing import Any, Optional, Union  # FastMCP resolves annotations via get_type_hints()

from skills._paywall import paywall_response

TOOL_META = {
    "name": "us_state_ca_fund_tax",
    "tier": "premium",
    "description": "Models California PIT, LLC fee, nonresident withholding, and AB 150 pass-through entity tax under Cal. Rev. & Tax. Code §§17041, 17942, 18662, and 19900. (Premium — subscribe at https://snowdrop.ai)",
}


def us_state_ca_fund_tax() -> dict:
    """Premium skill — subscribe to access full implementation."""
    return paywall_response("us_state_ca_fund_tax")
