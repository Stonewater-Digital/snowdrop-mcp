"""
us_state_in_fund_tax — Handles Indiana composite withholding and SALT workaround calculations under Ind

PREMIUM SKILL — full implementation available to subscribers.
Subscribe: https://snowdrop.ai (launching soon)

AUTO-GENERATED STUB — do not edit manually.
Source of truth: snowdrop-core/skills/premium/fund_tax/us_state_in_fund_tax.py
Regenerate: python scripts/build_public_stubs.py
"""
from __future__ import annotations  # defers annotation evaluation (PEP 563)
from typing import Any, Optional, Union  # FastMCP resolves annotations via get_type_hints()

from skills._paywall import paywall_response

TOOL_META = {
    "name": "us_state_in_fund_tax",
    "tier": "premium",
    "description": "Handles Indiana composite withholding and SALT workaround calculations under Ind. Code §§6-3-2-1 and 6-3-4-12. (Premium — subscribe at https://snowdrop.ai)",
}


def us_state_in_fund_tax() -> dict:
    """Premium skill — subscribe to access full implementation."""
    return paywall_response("us_state_in_fund_tax")
