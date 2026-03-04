"""
safe_note_converter — Calculates SAFE conversion price, shares, and founder dilution

PREMIUM SKILL — full implementation available to subscribers.
Subscribe: https://snowdrop.ai (launching soon)

AUTO-GENERATED STUB — do not edit manually.
Source of truth: snowdrop-core/skills/premium/venture/safe_note_converter.py
Regenerate: python scripts/build_public_stubs.py
"""
from __future__ import annotations  # defers annotation evaluation (PEP 563)
from typing import Any, Optional, Union  # FastMCP resolves annotations via get_type_hints()

from skills._paywall import paywall_response

TOOL_META = {
    "name": "safe_note_converter",
    "tier": "premium",
    "description": "Calculates SAFE conversion price, shares, and founder dilution. (Premium — subscribe at https://snowdrop.ai)",
}


def safe_note_converter(safe_amt: float, valuation_cap: float, discount_pct: float | None = 20.0, mfn: bool = False, next_round_pre_money: float = 0, next_round_pps: float = 0, pre_money_safe: bool = False) -> dict[str, Any]:
    """Premium skill — subscribe to access full implementation."""
    return paywall_response("safe_note_converter")
