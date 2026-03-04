"""
management_fee_offset — Computes the net management fee after applying a fee offset for transaction fees and advisory income earned by the GP

PREMIUM SKILL — full implementation available to subscribers.
Subscribe: https://snowdrop.ai (launching soon)

AUTO-GENERATED STUB — do not edit manually.
Source of truth: snowdrop-core/skills/premium/fund_accounting/management_fee_offset.py
Regenerate: python scripts/build_public_stubs.py
"""
from __future__ import annotations  # defers annotation evaluation (PEP 563)
from typing import Any, Optional, Union  # FastMCP resolves annotations via get_type_hints()

from skills._paywall import paywall_response

TOOL_META = {
    "name": "management_fee_offset",
    "tier": "premium",
    "description": "Computes the net management fee after applying a fee offset for transaction fees and advisory income earned by the GP. Per ILPA best practices, a configurable percentage (default 80%) of GP-earned fees is credited against the base management fee, benefiting LPs. Net fee is floored at zero (cannot be negative). (Premium — subscribe at https://snowdrop.ai)",
}


def management_fee_offset() -> dict:
    """Premium skill — subscribe to access full implementation."""
    return paywall_response("management_fee_offset")
