"""
mlp_k1_income_allocator — Allocates taxable income across unitholders based on ownership units

PREMIUM SKILL — full implementation available to subscribers.
Subscribe: https://snowdrop.ai (launching soon)

AUTO-GENERATED STUB — do not edit manually.
Source of truth: snowdrop-core/skills/premium/mlps/mlp_k1_income_allocator.py
Regenerate: python scripts/build_public_stubs.py
"""
from __future__ import annotations  # defers annotation evaluation (PEP 563)
from typing import Any, Optional, Union  # FastMCP resolves annotations via get_type_hints()

from skills._paywall import paywall_response

TOOL_META = {
    "name": "mlp_k1_income_allocator",
    "tier": "premium",
    "description": "Allocates taxable income across unitholders based on ownership units. (Premium — subscribe at https://snowdrop.ai)",
}


def mlp_k1_income_allocator(total_taxable_income: float, unitholders: Sequence[dict[str, Any]]) -> dict[str, Any]:
    """Premium skill — subscribe to access full implementation."""
    return paywall_response("mlp_k1_income_allocator")
