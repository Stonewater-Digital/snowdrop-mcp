"""
form_1065_k1_allocator — Splits partnership income items by partner percentages consistent with IRC §704(b)

PREMIUM SKILL — full implementation available to subscribers.
Subscribe: https://snowdrop.ai (launching soon)

AUTO-GENERATED STUB — do not edit manually.
Source of truth: snowdrop-core/skills/premium/fund_tax/form_1065_k1_allocator.py
Regenerate: python scripts/build_public_stubs.py
"""
from __future__ import annotations  # defers annotation evaluation (PEP 563)
from typing import Any, Optional, Union  # FastMCP resolves annotations via get_type_hints()

from skills._paywall import paywall_response

TOOL_META = {
    "name": "form_1065_k1_allocator",
    "tier": "premium",
    "description": "Splits partnership income items by partner percentages consistent with IRC §704(b). (Premium — subscribe at https://snowdrop.ai)",
}


def form_1065_k1_allocator() -> dict:
    """Premium skill — subscribe to access full implementation."""
    return paywall_response("form_1065_k1_allocator")
