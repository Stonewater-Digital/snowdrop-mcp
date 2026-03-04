"""
management_fee_vat_calculator — Determines VAT/GST on management fees and whether exemptions/zero-rating apply

PREMIUM SKILL — full implementation available to subscribers.
Subscribe: https://snowdrop.ai (launching soon)

AUTO-GENERATED STUB — do not edit manually.
Source of truth: snowdrop-core/skills/premium/fund_tax/management_fee_vat_calculator.py
Regenerate: python scripts/build_public_stubs.py
"""
from __future__ import annotations  # defers annotation evaluation (PEP 563)
from typing import Any, Optional, Union  # FastMCP resolves annotations via get_type_hints()

from skills._paywall import paywall_response

TOOL_META = {
    "name": "management_fee_vat_calculator",
    "tier": "premium",
    "description": "Determines VAT/GST on management fees and whether exemptions/zero-rating apply. (Premium — subscribe at https://snowdrop.ai)",
}


def management_fee_vat_calculator() -> dict:
    """Premium skill — subscribe to access full implementation."""
    return paywall_response("management_fee_vat_calculator")
