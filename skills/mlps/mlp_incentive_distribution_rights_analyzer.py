"""
mlp_incentive_distribution_rights_analyzer — Applies MLP IDR tiers to calculate GP vs LP cash splits at current distribution rates

PREMIUM SKILL — full implementation available to subscribers.
Subscribe: https://snowdrop.ai (launching soon)

AUTO-GENERATED STUB — do not edit manually.
Source of truth: snowdrop-core/skills/premium/mlps/mlp_incentive_distribution_rights_analyzer.py
Regenerate: python scripts/build_public_stubs.py
"""
from __future__ import annotations  # defers annotation evaluation (PEP 563)
from typing import Any, Optional, Union  # FastMCP resolves annotations via get_type_hints()

from skills._paywall import paywall_response

TOOL_META = {
    "name": "mlp_incentive_distribution_rights_analyzer",
    "tier": "premium",
    "description": "Applies MLP IDR tiers to calculate GP vs LP cash splits at current distribution rates. (Premium — subscribe at https://snowdrop.ai)",
}


def mlp_incentive_distribution_rights_analyzer(distribution_per_unit: float, total_units: float, idr_tiers: Sequence[dict[str, float]]) -> dict[str, Any]:
    """Premium skill — subscribe to access full implementation."""
    return paywall_response("mlp_incentive_distribution_rights_analyzer")
