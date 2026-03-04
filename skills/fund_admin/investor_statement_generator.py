"""
investor_statement_generator — Builds LP investor statement data including NAV, DPI, TVPI, RVPI, unfunded commitment, and IRR

PREMIUM SKILL — full implementation available to subscribers.
Subscribe: https://snowdrop.ai (launching soon)

AUTO-GENERATED STUB — do not edit manually.
Source of truth: snowdrop-core/skills/premium/fund_admin/investor_statement_generator.py
Regenerate: python scripts/build_public_stubs.py
"""
from __future__ import annotations  # defers annotation evaluation (PEP 563)
from typing import Any, Optional, Union  # FastMCP resolves annotations via get_type_hints()

from skills._paywall import paywall_response

TOOL_META = {
    "name": "investor_statement_generator",
    "tier": "premium",
    "description": "Builds LP investor statement data including NAV, DPI, TVPI, RVPI, unfunded commitment, and IRR. Validates that called capital does not exceed commitment. (Premium — subscribe at https://snowdrop.ai)",
}


def investor_statement_generator(lp_name: str, commitment: float, capital_called: float, distributions: float, nav: float, irr_pct: float = 0.0) -> dict[str, Any]:
    """Premium skill — subscribe to access full implementation."""
    return paywall_response("investor_statement_generator")
