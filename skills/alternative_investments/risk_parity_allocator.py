"""
risk_parity_allocator — Uses iterative proportional fitting on the covariance matrix to achieve target risk budgets per asset

PREMIUM SKILL — full implementation available to subscribers.
Subscribe: https://snowdrop.ai (launching soon)

AUTO-GENERATED STUB — do not edit manually.
Source of truth: snowdrop-core/skills/premium/alternative_investments/risk_parity_allocator.py
Regenerate: python scripts/build_public_stubs.py
"""
from __future__ import annotations  # defers annotation evaluation (PEP 563)
from typing import Any, Optional, Union  # FastMCP resolves annotations via get_type_hints()

from skills._paywall import paywall_response

TOOL_META = {
    "name": "risk_parity_allocator",
    "tier": "premium",
    "description": "Uses iterative proportional fitting on the covariance matrix to achieve target risk budgets per asset. (Premium — subscribe at https://snowdrop.ai)",
}


def risk_parity_allocator(covariance_matrix: List[List[float]], risk_budgets: List[float]) -> dict[str, Any]:
    """Premium skill — subscribe to access full implementation."""
    return paywall_response("risk_parity_allocator")
