"""
mlp_distribution_coverage_ratio — Computes distribution coverage ratio and leverage on payouts for midstream partnerships

PREMIUM SKILL — full implementation available to subscribers.
Subscribe: https://snowdrop.ai (launching soon)

AUTO-GENERATED STUB — do not edit manually.
Source of truth: snowdrop-core/skills/premium/mlps/mlp_distribution_coverage_ratio.py
Regenerate: python scripts/build_public_stubs.py
"""
from __future__ import annotations  # defers annotation evaluation (PEP 563)
from typing import Any, Optional, Union  # FastMCP resolves annotations via get_type_hints()

from skills._paywall import paywall_response

TOOL_META = {
    "name": "mlp_distribution_coverage_ratio",
    "tier": "premium",
    "description": "Computes distribution coverage ratio and leverage on payouts for midstream partnerships. (Premium — subscribe at https://snowdrop.ai)",
}


def mlp_distribution_coverage_ratio(distributable_cash_flow: float, distributions_paid: float) -> dict[str, Any]:
    """Premium skill — subscribe to access full implementation."""
    return paywall_response("mlp_distribution_coverage_ratio")
