"""
gp_clawback_calculator — Compares distributed carry versus catch-up waterfall to determine outstanding clawback and recommended escrow percentage

PREMIUM SKILL — full implementation available to subscribers.
Subscribe: https://snowdrop.ai (launching soon)

AUTO-GENERATED STUB — do not edit manually.
Source of truth: snowdrop-core/skills/premium/alternative_investments/gp_clawback_calculator.py
Regenerate: python scripts/build_public_stubs.py
"""
from __future__ import annotations  # defers annotation evaluation (PEP 563)
from typing import Any, Optional, Union  # FastMCP resolves annotations via get_type_hints()

from skills._paywall import paywall_response

TOOL_META = {
    "name": "gp_clawback_calculator",
    "tier": "premium",
    "description": "Compares distributed carry versus catch-up waterfall to determine outstanding clawback and recommended escrow percentage. (Premium — subscribe at https://snowdrop.ai)",
}


def gp_clawback_calculator(carried_interest_received: float, lp_preferred_return: float, total_distributions: float, total_contributions: float, carry_split: float) -> dict[str, Any]:
    """Premium skill — subscribe to access full implementation."""
    return paywall_response("gp_clawback_calculator")
