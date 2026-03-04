"""
convertible_note_calculator — Computes accrued interest, conversion price, and shares for convertible notes

PREMIUM SKILL — full implementation available to subscribers.
Subscribe: https://snowdrop.ai (launching soon)

AUTO-GENERATED STUB — do not edit manually.
Source of truth: snowdrop-core/skills/premium/venture/convertible_note_calculator.py
Regenerate: python scripts/build_public_stubs.py
"""
from __future__ import annotations  # defers annotation evaluation (PEP 563)
from typing import Any, Optional, Union  # FastMCP resolves annotations via get_type_hints()

from skills._paywall import paywall_response

TOOL_META = {
    "name": "convertible_note_calculator",
    "tier": "premium",
    "description": "Computes accrued interest, conversion price, and shares for convertible notes. (Premium — subscribe at https://snowdrop.ai)",
}


def convertible_note_calculator(principal: float, interest_rate: float, term_months: int, valuation_cap: float | None, discount_pct: float = 20.0, issue_date: str = '', conversion_date: str = '', qualified_financing_amount: float = 0.0, next_round_pps: float = 0.0) -> dict[str, Any]:
    """Premium skill — subscribe to access full implementation."""
    return paywall_response("convertible_note_calculator")
