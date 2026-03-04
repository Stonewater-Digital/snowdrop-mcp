"""
foreign_tax_credit_calculator — Applies the FTC limitation formula for passive and general baskets

PREMIUM SKILL — full implementation available to subscribers.
Subscribe: https://snowdrop.ai (launching soon)

AUTO-GENERATED STUB — do not edit manually.
Source of truth: snowdrop-core/skills/premium/fund_tax/foreign_tax_credit_calculator.py
Regenerate: python scripts/build_public_stubs.py
"""
from __future__ import annotations  # defers annotation evaluation (PEP 563)
from typing import Any, Optional, Union  # FastMCP resolves annotations via get_type_hints()

from skills._paywall import paywall_response

TOOL_META = {
    "name": "foreign_tax_credit_calculator",
    "tier": "premium",
    "description": "Applies the FTC limitation formula for passive and general baskets. (Premium — subscribe at https://snowdrop.ai)",
}


def foreign_tax_credit_calculator() -> dict:
    """Premium skill — subscribe to access full implementation."""
    return paywall_response("foreign_tax_credit_calculator")
