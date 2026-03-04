"""
intl_fr_fund_tax — Determines French withholding outcomes and 25% corporation tax impact when a French permanent establishment exists

PREMIUM SKILL — full implementation available to subscribers.
Subscribe: https://snowdrop.ai (launching soon)

AUTO-GENERATED STUB — do not edit manually.
Source of truth: snowdrop-core/skills/premium/fund_tax/intl_fr_fund_tax.py
Regenerate: python scripts/build_public_stubs.py
"""
from __future__ import annotations  # defers annotation evaluation (PEP 563)
from typing import Any, Optional, Union  # FastMCP resolves annotations via get_type_hints()

from skills._paywall import paywall_response

TOOL_META = {
    "name": "intl_fr_fund_tax",
    "tier": "premium",
    "description": "Determines French withholding outcomes and 25% corporation tax impact when a French permanent establishment exists. (Premium — subscribe at https://snowdrop.ai)",
}


def intl_fr_fund_tax() -> dict:
    """Premium skill — subscribe to access full implementation."""
    return paywall_response("intl_fr_fund_tax")
