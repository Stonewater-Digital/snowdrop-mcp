"""
fatca_withholding_calculator — Applies Chapter 4 withholding based on FATCA status and documentation validity

PREMIUM SKILL — full implementation available to subscribers.
Subscribe: https://snowdrop.ai (launching soon)

AUTO-GENERATED STUB — do not edit manually.
Source of truth: snowdrop-core/skills/premium/fund_tax/fatca_withholding_calculator.py
Regenerate: python scripts/build_public_stubs.py
"""
from __future__ import annotations  # defers annotation evaluation (PEP 563)
from typing import Any, Optional, Union  # FastMCP resolves annotations via get_type_hints()

from skills._paywall import paywall_response

TOOL_META = {
    "name": "fatca_withholding_calculator",
    "tier": "premium",
    "description": "Applies Chapter 4 withholding based on FATCA status and documentation validity. (Premium — subscribe at https://snowdrop.ai)",
}


def fatca_withholding_calculator() -> dict:
    """Premium skill — subscribe to access full implementation."""
    return paywall_response("fatca_withholding_calculator")
