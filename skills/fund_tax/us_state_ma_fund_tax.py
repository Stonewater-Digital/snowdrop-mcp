"""
us_state_ma_fund_tax — Calculates Massachusetts flat tax, millionaires surtax, and SALT workaround election under Mass

PREMIUM SKILL — full implementation available to subscribers.
Subscribe: https://snowdrop.ai (launching soon)

AUTO-GENERATED STUB — do not edit manually.
Source of truth: snowdrop-core/skills/premium/fund_tax/us_state_ma_fund_tax.py
Regenerate: python scripts/build_public_stubs.py
"""
from __future__ import annotations  # defers annotation evaluation (PEP 563)
from typing import Any, Optional, Union  # FastMCP resolves annotations via get_type_hints()

from skills._paywall import paywall_response

TOOL_META = {
    "name": "us_state_ma_fund_tax",
    "tier": "premium",
    "description": "Calculates Massachusetts flat tax, millionaires surtax, and SALT workaround election under Mass. Gen. Laws ch. 62 and ch. 63D. (Premium — subscribe at https://snowdrop.ai)",
}


def us_state_ma_fund_tax() -> dict:
    """Premium skill — subscribe to access full implementation."""
    return paywall_response("us_state_ma_fund_tax")
