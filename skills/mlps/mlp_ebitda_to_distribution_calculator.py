"""
mlp_ebitda_to_distribution_calculator — Calculates EBITDA payout ratios to monitor sustainability of MLP distributions

PREMIUM SKILL — full implementation available to subscribers.
Subscribe: https://snowdrop.ai (launching soon)

AUTO-GENERATED STUB — do not edit manually.
Source of truth: snowdrop-core/skills/premium/mlps/mlp_ebitda_to_distribution_calculator.py
Regenerate: python scripts/build_public_stubs.py
"""
from __future__ import annotations  # defers annotation evaluation (PEP 563)
from typing import Any, Optional, Union  # FastMCP resolves annotations via get_type_hints()

from skills._paywall import paywall_response

TOOL_META = {
    "name": "mlp_ebitda_to_distribution_calculator",
    "tier": "premium",
    "description": "Calculates EBITDA payout ratios to monitor sustainability of MLP distributions. (Premium — subscribe at https://snowdrop.ai)",
}


def mlp_ebitda_to_distribution_calculator(ebitda: float, total_distributions: float) -> dict[str, Any]:
    """Premium skill — subscribe to access full implementation."""
    return paywall_response("mlp_ebitda_to_distribution_calculator")
