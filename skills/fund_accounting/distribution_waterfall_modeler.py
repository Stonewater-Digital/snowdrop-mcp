"""
distribution_waterfall_modeler — Calculates LP/GP outcomes for American and European waterfalls with tier detail

PREMIUM SKILL — full implementation available to subscribers.
Subscribe: https://snowdrop.ai (launching soon)

AUTO-GENERATED STUB — do not edit manually.
Source of truth: snowdrop-core/skills/premium/fund_accounting/distribution_waterfall_modeler.py
Regenerate: python scripts/build_public_stubs.py
"""
from __future__ import annotations  # defers annotation evaluation (PEP 563)
from typing import Any, Optional, Union  # FastMCP resolves annotations via get_type_hints()

from skills._paywall import paywall_response

TOOL_META = {
    "name": "distribution_waterfall_modeler",
    "tier": "premium",
    "description": "Calculates LP/GP outcomes for American and European waterfalls with tier detail. (Premium — subscribe at https://snowdrop.ai)",
}


def distribution_waterfall_modeler(style: str, total_commitments: float, contributions: list[dict[str, Any]], distributions: list[dict[str, Any]], preferred_return_pct: float = 8.0, gp_carry_pct: float = 20.0, catch_up_pct: float = 100.0, gp_commitment_pct: float = 2.0, tiers: list[dict[str, Any]] | None = None) -> dict[str, Any]:
    """Premium skill — subscribe to access full implementation."""
    return paywall_response("distribution_waterfall_modeler")
