"""
wash_sale_cross_account — Determines wash-sale disallowances when substantially identical securities are repurchased within ±30 days across related accounts

PREMIUM SKILL — full implementation available to subscribers.
Subscribe: https://snowdrop.ai (launching soon)

AUTO-GENERATED STUB — do not edit manually.
Source of truth: snowdrop-core/skills/premium/fund_tax/wash_sale_cross_account.py
Regenerate: python scripts/build_public_stubs.py
"""
from __future__ import annotations  # defers annotation evaluation (PEP 563)
from typing import Any, Optional, Union  # FastMCP resolves annotations via get_type_hints()

from skills._paywall import paywall_response

TOOL_META = {
    "name": "wash_sale_cross_account",
    "tier": "premium",
    "description": "Determines wash-sale disallowances when substantially identical securities are repurchased within ±30 days across related accounts. (Premium — subscribe at https://snowdrop.ai)",
}


def wash_sale_cross_account() -> dict:
    """Premium skill — subscribe to access full implementation."""
    return paywall_response("wash_sale_cross_account")
