"""
clawback_analyzer — Determines whether the GP owes a clawback based on carry received versus carry entitled after preferred return

PREMIUM SKILL — full implementation available to subscribers.
Subscribe: https://snowdrop.ai (launching soon)

AUTO-GENERATED STUB — do not edit manually.
Source of truth: snowdrop-core/skills/premium/fund_accounting/clawback_analyzer.py
Regenerate: python scripts/build_public_stubs.py
"""
from __future__ import annotations  # defers annotation evaluation (PEP 563)
from typing import Any, Optional, Union  # FastMCP resolves annotations via get_type_hints()

from skills._paywall import paywall_response

TOOL_META = {
    "name": "clawback_analyzer",
    "tier": "premium",
    "description": "Determines whether the GP owes a clawback based on carry received versus carry entitled after preferred return. (Premium — subscribe at https://snowdrop.ai)",
}


def clawback_analyzer(total_distributions: float, total_contributions: float, preferred_return: float, carry_received: float, carry_rate: float = 0.2) -> dict:
    """Premium skill — subscribe to access full implementation."""
    return paywall_response("clawback_analyzer")
