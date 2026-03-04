"""
us_state_co_fund_tax — Computes Colorado income tax, elective entity-level tax, and nonresident withholding obligations referencing Colo

PREMIUM SKILL — full implementation available to subscribers.
Subscribe: https://snowdrop.ai (launching soon)

AUTO-GENERATED STUB — do not edit manually.
Source of truth: snowdrop-core/skills/premium/fund_tax/us_state_co_fund_tax.py
Regenerate: python scripts/build_public_stubs.py
"""
from __future__ import annotations  # defers annotation evaluation (PEP 563)
from typing import Any, Optional, Union  # FastMCP resolves annotations via get_type_hints()

from skills._paywall import paywall_response

TOOL_META = {
    "name": "us_state_co_fund_tax",
    "tier": "premium",
    "description": "Computes Colorado income tax, elective entity-level tax, and nonresident withholding obligations referencing Colo. Rev. Stat. §§39-22-104 and 39-22-601. (Premium — subscribe at https://snowdrop.ai)",
}


def us_state_co_fund_tax() -> dict:
    """Premium skill — subscribe to access full implementation."""
    return paywall_response("us_state_co_fund_tax")
