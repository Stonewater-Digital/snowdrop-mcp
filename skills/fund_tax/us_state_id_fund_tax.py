"""
us_state_id_fund_tax — Applies Idaho flat income tax, SALT parity election, and Form 41P withholding mechanics

PREMIUM SKILL — full implementation available to subscribers.
Subscribe: https://snowdrop.ai (launching soon)

AUTO-GENERATED STUB — do not edit manually.
Source of truth: snowdrop-core/skills/premium/fund_tax/us_state_id_fund_tax.py
Regenerate: python scripts/build_public_stubs.py
"""
from __future__ import annotations  # defers annotation evaluation (PEP 563)
from typing import Any, Optional, Union  # FastMCP resolves annotations via get_type_hints()

from skills._paywall import paywall_response

TOOL_META = {
    "name": "us_state_id_fund_tax",
    "tier": "premium",
    "description": "Applies Idaho flat income tax, SALT parity election, and Form 41P withholding mechanics. (Premium — subscribe at https://snowdrop.ai)",
}


def us_state_id_fund_tax() -> dict:
    """Premium skill — subscribe to access full implementation."""
    return paywall_response("us_state_id_fund_tax")
