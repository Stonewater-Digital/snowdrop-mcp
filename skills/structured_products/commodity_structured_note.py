"""
commodity_structured_note — Values a participation note written on a commodity forward using Black's model and applies cap/floor constraints

PREMIUM SKILL — full implementation available to subscribers.
Subscribe: https://snowdrop.ai (launching soon)

AUTO-GENERATED STUB — do not edit manually.
Source of truth: snowdrop-core/skills/premium/structured_products/commodity_structured_note.py
Regenerate: python scripts/build_public_stubs.py
"""
from __future__ import annotations  # defers annotation evaluation (PEP 563)
from typing import Any, Optional, Union  # FastMCP resolves annotations via get_type_hints()

from skills._paywall import paywall_response

TOOL_META = {
    "name": "commodity_structured_note",
    "tier": "premium",
    "description": "Values a participation note written on a commodity forward using Black's model and applies cap/floor constraints. (Premium — subscribe at https://snowdrop.ai)",
}


def commodity_structured_note(spot_price: float, forward_curve: List[float], volatility: float, participation_rate: float, cap_return: float, floor_return: float, maturity_years: float, risk_free_rate: float) -> dict[str, Any]:
    """Premium skill — subscribe to access full implementation."""
    return paywall_response("commodity_structured_note")
