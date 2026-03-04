"""
exit_multiple_analysis — Analyzes a portfolio of realized exits to compute Money-on-Invested-Capital (MoIC) multiples for each position

PREMIUM SKILL — full implementation available to subscribers.
Subscribe: https://snowdrop.ai (launching soon)

AUTO-GENERATED STUB — do not edit manually.
Source of truth: snowdrop-core/skills/premium/fund_accounting/exit_multiple_analysis.py
Regenerate: python scripts/build_public_stubs.py
"""
from __future__ import annotations  # defers annotation evaluation (PEP 563)
from typing import Any, Optional, Union  # FastMCP resolves annotations via get_type_hints()

from skills._paywall import paywall_response

TOOL_META = {
    "name": "exit_multiple_analysis",
    "tier": "premium",
    "description": "Analyzes a portfolio of realized exits to compute Money-on-Invested-Capital (MoIC) multiples for each position. Aggregates median, mean, min, and max multiples at the portfolio level and breaks down performance by sector and exit type (IPO, M&A, secondary, write-off, etc.). (Premium — subscribe at https://snowdrop.ai)",
}


def exit_multiple_analysis() -> dict:
    """Premium skill — subscribe to access full implementation."""
    return paywall_response("exit_multiple_analysis")
