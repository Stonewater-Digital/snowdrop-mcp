"""
convexity_hedger — Determines barbell weights that match the duration of a bullet bond while maximizing convexity per CFA curriculum

PREMIUM SKILL — full implementation available to subscribers.
Subscribe: https://snowdrop.ai (launching soon)

AUTO-GENERATED STUB — do not edit manually.
Source of truth: snowdrop-core/skills/premium/fixed_income_analytics/convexity_hedger.py
Regenerate: python scripts/build_public_stubs.py
"""
from __future__ import annotations  # defers annotation evaluation (PEP 563)
from typing import Any, Optional, Union  # FastMCP resolves annotations via get_type_hints()

from skills._paywall import paywall_response

TOOL_META = {
    "name": "convexity_hedger",
    "tier": "premium",
    "description": "Determines barbell weights that match the duration of a bullet bond while maximizing convexity per CFA curriculum. (Premium — subscribe at https://snowdrop.ai)",
}


def convexity_hedger(barbell_assets: List[Dict[str, Any]], bullet_asset: Dict[str, float], target_notional: float) -> dict[str, Any]:
    """Premium skill — subscribe to access full implementation."""
    return paywall_response("convexity_hedger")
