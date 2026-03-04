"""
investor_letter_drafter — Builds executive-ready investor letter sections

PREMIUM SKILL — full implementation available to subscribers.
Subscribe: https://snowdrop.ai (launching soon)

AUTO-GENERATED STUB — do not edit manually.
Source of truth: snowdrop-core/skills/premium/investor_relations/investor_letter_drafter.py
Regenerate: python scripts/build_public_stubs.py
"""
from __future__ import annotations  # defers annotation evaluation (PEP 563)
from typing import Any, Optional, Union  # FastMCP resolves annotations via get_type_hints()

from skills._paywall import paywall_response

TOOL_META = {
    "name": "investor_letter_drafter",
    "tier": "premium",
    "description": "Builds executive-ready investor letter sections. (Premium — subscribe at https://snowdrop.ai)",
}


def investor_letter_drafter(period: str, fund_performance: dict[str, Any], market_commentary: str, outlook: str, key_decisions: list[str]) -> dict[str, Any]:
    """Premium skill — subscribe to access full implementation."""
    return paywall_response("investor_letter_drafter")
