"""
anti_treaty_shopping_lob — Evaluates LOB tests (ownership/base erosion, publicly traded, active trade or business, derivative benefits)

PREMIUM SKILL — full implementation available to subscribers.
Subscribe: https://snowdrop.ai (launching soon)

AUTO-GENERATED STUB — do not edit manually.
Source of truth: snowdrop-core/skills/premium/fund_tax/anti_treaty_shopping_lob.py
Regenerate: python scripts/build_public_stubs.py
"""
from __future__ import annotations  # defers annotation evaluation (PEP 563)
from typing import Any, Optional, Union  # FastMCP resolves annotations via get_type_hints()

from skills._paywall import paywall_response

TOOL_META = {
    "name": "anti_treaty_shopping_lob",
    "tier": "premium",
    "description": "Evaluates LOB tests (ownership/base erosion, publicly traded, active trade or business, derivative benefits). (Premium — subscribe at https://snowdrop.ai)",
}


def anti_treaty_shopping_lob() -> dict:
    """Premium skill — subscribe to access full implementation."""
    return paywall_response("anti_treaty_shopping_lob")
