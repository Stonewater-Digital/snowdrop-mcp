"""
exit_tax_calculator — Computes exit tax exposures for investors emigrating from the US, Germany, or Canada

PREMIUM SKILL — full implementation available to subscribers.
Subscribe: https://snowdrop.ai (launching soon)

AUTO-GENERATED STUB — do not edit manually.
Source of truth: snowdrop-core/skills/premium/fund_tax/exit_tax_calculator.py
Regenerate: python scripts/build_public_stubs.py
"""
from __future__ import annotations  # defers annotation evaluation (PEP 563)
from typing import Any, Optional, Union  # FastMCP resolves annotations via get_type_hints()

from skills._paywall import paywall_response

TOOL_META = {
    "name": "exit_tax_calculator",
    "tier": "premium",
    "description": "Computes exit tax exposures for investors emigrating from the US, Germany, or Canada. (Premium — subscribe at https://snowdrop.ai)",
}


def exit_tax_calculator() -> dict:
    """Premium skill — subscribe to access full implementation."""
    return paywall_response("exit_tax_calculator")
