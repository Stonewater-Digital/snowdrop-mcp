"""
calc_waterfall_dist — Calculates LP/GP waterfall distributions across preferred return, catch-up, and carried interest tiers

PREMIUM SKILL — full implementation available to subscribers.
Subscribe: https://snowdrop.ai (launching soon)

AUTO-GENERATED STUB — do not edit manually.
Source of truth: snowdrop-core/skills/premium/fund_accounting/calc_waterfall_dist.py
Regenerate: python scripts/build_public_stubs.py
"""
from __future__ import annotations  # defers annotation evaluation (PEP 563)
from typing import Any, Optional, Union  # FastMCP resolves annotations via get_type_hints()

from skills._paywall import paywall_response

TOOL_META = {
    "name": "calc_waterfall_dist",
    "tier": "premium",
    "description": "Calculates LP/GP waterfall distributions across preferred return, catch-up, and carried interest tiers. (Premium — subscribe at https://snowdrop.ai)",
}


def calc_waterfall_dist(fund_size: float, preferred_return: float, carry_rate: float, gp_commitment: float, distribution_amount: float) -> dict:
    """Premium skill — subscribe to access full implementation."""
    return paywall_response("calc_waterfall_dist")
