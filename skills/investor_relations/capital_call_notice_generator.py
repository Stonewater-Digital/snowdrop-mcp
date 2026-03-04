"""
capital_call_notice_generator — Creates LP-specific capital call instructions awaiting Thunder sign-off

PREMIUM SKILL — full implementation available to subscribers.
Subscribe: https://snowdrop.ai (launching soon)

AUTO-GENERATED STUB — do not edit manually.
Source of truth: snowdrop-core/skills/premium/investor_relations/capital_call_notice_generator.py
Regenerate: python scripts/build_public_stubs.py
"""
from __future__ import annotations  # defers annotation evaluation (PEP 563)
from typing import Any, Optional, Union  # FastMCP resolves annotations via get_type_hints()

from skills._paywall import paywall_response

TOOL_META = {
    "name": "capital_call_notice_generator",
    "tier": "premium",
    "description": "Creates LP-specific capital call instructions awaiting Thunder sign-off. (Premium — subscribe at https://snowdrop.ai)",
}


def capital_call_notice_generator(fund_name: str, call_amount: float, purpose: str, due_date: str, lp_allocations: list[dict[str, Any]]) -> dict[str, Any]:
    """Premium skill — subscribe to access full implementation."""
    return paywall_response("capital_call_notice_generator")
