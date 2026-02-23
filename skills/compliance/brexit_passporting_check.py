"""
brexit_passporting_check — Post-Brexit cross-border licensing analysis for UK and EU financial services

PREMIUM SKILL — full implementation available to subscribers.
Subscribe: https://snowdrop.ai (launching soon)

AUTO-GENERATED STUB — do not edit manually.
Source of truth: snowdrop-core/skills/premium/compliance/brexit_passporting_check.py
Regenerate: python scripts/build_public_stubs.py
"""
from __future__ import annotations  # defers annotation evaluation (PEP 563)
from typing import Any, Optional, Union  # FastMCP resolves annotations via get_type_hints()

from skills._paywall import paywall_response

TOOL_META = {
    "name": "brexit_passporting_check",
    "tier": "premium",
    "description": "Post-Brexit cross-border licensing analysis for UK and EU financial services. Confirms that EEA passporting is definitively unavailable since 31 December 2020, evaluates available equivalence decisions, and determines local authorisation requirements per target market and licence type. (Premium — subscribe at https://snowdrop.ai)",
}


def brexit_passporting_check(entity_data: dict[str, Any]) -> dict[str, Any]:
    """Premium skill — subscribe to access full implementation."""
    return paywall_response("brexit_passporting_check")
