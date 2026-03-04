"""
j_curve_analyzer — Builds cumulative net cash flow timeline highlighting J-curve characteristics: trough depth, trough year, recovery year (breakeven), and total net return

PREMIUM SKILL — full implementation available to subscribers.
Subscribe: https://snowdrop.ai (launching soon)

AUTO-GENERATED STUB — do not edit manually.
Source of truth: snowdrop-core/skills/premium/fund_admin/j_curve_analyzer.py
Regenerate: python scripts/build_public_stubs.py
"""
from __future__ import annotations  # defers annotation evaluation (PEP 563)
from typing import Any, Optional, Union  # FastMCP resolves annotations via get_type_hints()

from skills._paywall import paywall_response

TOOL_META = {
    "name": "j_curve_analyzer",
    "tier": "premium",
    "description": "Builds cumulative net cash flow timeline highlighting J-curve characteristics: trough depth, trough year, recovery year (breakeven), and total net return. Negative early net flows create the characteristic J shape. (Premium — subscribe at https://snowdrop.ai)",
}


def j_curve_analyzer(periods: list[dict[str, Any]]) -> dict[str, Any]:
    """Premium skill — subscribe to access full implementation."""
    return paywall_response("j_curve_analyzer")
