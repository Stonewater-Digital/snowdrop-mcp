"""
mlp_unitholders_return_calculator — Calculates price and distribution contribution to total return for MLP units

PREMIUM SKILL — full implementation available to subscribers.
Subscribe: https://snowdrop.ai (launching soon)

AUTO-GENERATED STUB — do not edit manually.
Source of truth: snowdrop-core/skills/premium/mlps/mlp_unitholders_return_calculator.py
Regenerate: python scripts/build_public_stubs.py
"""
from __future__ import annotations  # defers annotation evaluation (PEP 563)
from typing import Any, Optional, Union  # FastMCP resolves annotations via get_type_hints()

from skills._paywall import paywall_response

TOOL_META = {
    "name": "mlp_unitholders_return_calculator",
    "tier": "premium",
    "description": "Calculates price and distribution contribution to total return for MLP units. (Premium — subscribe at https://snowdrop.ai)",
}


def mlp_unitholders_return_calculator(start_price: float, end_price: float, distributions_per_unit: float) -> dict[str, Any]:
    """Premium skill — subscribe to access full implementation."""
    return paywall_response("mlp_unitholders_return_calculator")
