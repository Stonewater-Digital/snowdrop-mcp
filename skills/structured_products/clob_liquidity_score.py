"""
clob_liquidity_score — Computes a composite score from depth-weighted spread, imbalance, and volume decay to quantify CLOB liquidity

PREMIUM SKILL — full implementation available to subscribers.
Subscribe: https://snowdrop.ai (launching soon)

AUTO-GENERATED STUB — do not edit manually.
Source of truth: snowdrop-core/skills/premium/structured_products/clob_liquidity_score.py
Regenerate: python scripts/build_public_stubs.py
"""
from __future__ import annotations  # defers annotation evaluation (PEP 563)
from typing import Any, Optional, Union  # FastMCP resolves annotations via get_type_hints()

from skills._paywall import paywall_response

TOOL_META = {
    "name": "clob_liquidity_score",
    "tier": "premium",
    "description": "Computes a composite score from depth-weighted spread, imbalance, and volume decay to quantify CLOB liquidity. (Premium — subscribe at https://snowdrop.ai)",
}


def clob_liquidity_score(bid_levels: List[Dict[str, float]], ask_levels: List[Dict[str, float]], recent_volume: float, decay_half_life_minutes: float = 5.0) -> dict[str, Any]:
    """Premium skill — subscribe to access full implementation."""
    return paywall_response("clob_liquidity_score")
