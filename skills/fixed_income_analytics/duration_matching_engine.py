"""
duration_matching_engine — Solves for asset weights whose duration and convexity match a target liability, using least-squares immunization per Fabozzi

PREMIUM SKILL — full implementation available to subscribers.
Subscribe: https://snowdrop.ai (launching soon)

AUTO-GENERATED STUB — do not edit manually.
Source of truth: snowdrop-core/skills/premium/fixed_income_analytics/duration_matching_engine.py
Regenerate: python scripts/build_public_stubs.py
"""
from __future__ import annotations  # defers annotation evaluation (PEP 563)
from typing import Any, Optional, Union  # FastMCP resolves annotations via get_type_hints()

from skills._paywall import paywall_response

TOOL_META = {
    "name": "duration_matching_engine",
    "tier": "premium",
    "description": "Solves for asset weights whose duration and convexity match a target liability, using least-squares immunization per Fabozzi. (Premium — subscribe at https://snowdrop.ai)",
}


def duration_matching_engine(assets: List[Dict[str, Any]], liability_duration: float, liability_convexity: float) -> dict[str, Any]:
    """Premium skill — subscribe to access full implementation."""
    return paywall_response("duration_matching_engine")
