"""
correlation_swap_pricer — Computes the fair correlation (average off-diagonal) and marks the swap relative to strike with delta/vega style metrics

PREMIUM SKILL — full implementation available to subscribers.
Subscribe: https://snowdrop.ai (launching soon)

AUTO-GENERATED STUB — do not edit manually.
Source of truth: snowdrop-core/skills/premium/structured_products/correlation_swap_pricer.py
Regenerate: python scripts/build_public_stubs.py
"""
from __future__ import annotations  # defers annotation evaluation (PEP 563)
from typing import Any, Optional, Union  # FastMCP resolves annotations via get_type_hints()

from skills._paywall import paywall_response

TOOL_META = {
    "name": "correlation_swap_pricer",
    "tier": "premium",
    "description": "Computes the fair correlation (average off-diagonal) and marks the swap relative to strike with delta/vega style metrics. (Premium — subscribe at https://snowdrop.ai)",
}


def correlation_swap_pricer(correlation_matrix: List[List[float]], strike_correlation: float, realized_correlation: float, notional: float) -> dict[str, Any]:
    """Premium skill — subscribe to access full implementation."""
    return paywall_response("correlation_swap_pricer")
