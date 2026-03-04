"""
fund_restructuring_tax — Evaluates IRC §§351, 368, 367 and EU Merger Directive treatment for fund Merger/Domestication transactions

PREMIUM SKILL — full implementation available to subscribers.
Subscribe: https://snowdrop.ai (launching soon)

AUTO-GENERATED STUB — do not edit manually.
Source of truth: snowdrop-core/skills/premium/fund_tax/fund_restructuring_tax.py
Regenerate: python scripts/build_public_stubs.py
"""
from __future__ import annotations  # defers annotation evaluation (PEP 563)
from typing import Any, Optional, Union  # FastMCP resolves annotations via get_type_hints()

from skills._paywall import paywall_response

TOOL_META = {
    "name": "fund_restructuring_tax",
    "tier": "premium",
    "description": "Evaluates IRC §§351, 368, 367 and EU Merger Directive treatment for fund Merger/Domestication transactions. (Premium — subscribe at https://snowdrop.ai)",
}


def fund_restructuring_tax() -> dict:
    """Premium skill — subscribe to access full implementation."""
    return paywall_response("fund_restructuring_tax")
