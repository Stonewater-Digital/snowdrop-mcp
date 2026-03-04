"""
statistical_arbitrage_zscore — Performs OLS regression of X on Y to compute hedge ratio, z-score, and Ornstein-Uhlenbeck half-life for pairs trading

PREMIUM SKILL — full implementation available to subscribers.
Subscribe: https://snowdrop.ai (launching soon)

AUTO-GENERATED STUB — do not edit manually.
Source of truth: snowdrop-core/skills/premium/alternative_investments/statistical_arbitrage_zscore.py
Regenerate: python scripts/build_public_stubs.py
"""
from __future__ import annotations  # defers annotation evaluation (PEP 563)
from typing import Any, Optional, Union  # FastMCP resolves annotations via get_type_hints()

from skills._paywall import paywall_response

TOOL_META = {
    "name": "statistical_arbitrage_zscore",
    "tier": "premium",
    "description": "Performs OLS regression of X on Y to compute hedge ratio, z-score, and Ornstein-Uhlenbeck half-life for pairs trading. (Premium — subscribe at https://snowdrop.ai)",
}


def statistical_arbitrage_zscore(series_x: List[float], series_y: List[float], entry_z: float, exit_z: float) -> dict[str, Any]:
    """Premium skill — subscribe to access full implementation."""
    return paywall_response("statistical_arbitrage_zscore")
