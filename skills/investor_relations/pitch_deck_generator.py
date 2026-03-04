"""
pitch_deck_generator — Creates slide-by-slide pitch content for Snowdrop fundraising narratives

PREMIUM SKILL — full implementation available to subscribers.
Subscribe: https://snowdrop.ai (launching soon)

AUTO-GENERATED STUB — do not edit manually.
Source of truth: snowdrop-core/skills/premium/investor_relations/pitch_deck_generator.py
Regenerate: python scripts/build_public_stubs.py
"""
from __future__ import annotations  # defers annotation evaluation (PEP 563)
from typing import Any, Optional, Union  # FastMCP resolves annotations via get_type_hints()

from skills._paywall import paywall_response

TOOL_META = {
    "name": "pitch_deck_generator",
    "tier": "premium",
    "description": "Creates slide-by-slide pitch content for Snowdrop fundraising narratives. (Premium — subscribe at https://snowdrop.ai)",
}


def pitch_deck_generator(company: dict[str, Any], financials: dict[str, Any], market: dict[str, Any], traction: dict[str, Any], ask: dict[str, Any]) -> dict[str, Any]:
    """Premium skill — subscribe to access full implementation."""
    return paywall_response("pitch_deck_generator")
