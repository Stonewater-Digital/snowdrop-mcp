"""
variance_swap_pricer — Applies the Carr-Madan replication integral to infer fair variance strikes and MTM P&L

PREMIUM SKILL — full implementation available to subscribers.
Subscribe: https://snowdrop.ai (launching soon)

AUTO-GENERATED STUB — do not edit manually.
Source of truth: snowdrop-core/skills/premium/exotic_options/variance_swap_pricer.py
Regenerate: python scripts/build_public_stubs.py
"""
from __future__ import annotations  # defers annotation evaluation (PEP 563)
from typing import Any, Optional, Union  # FastMCP resolves annotations via get_type_hints()

from skills._paywall import paywall_response

TOOL_META = {
    "name": "variance_swap_pricer",
    "tier": "premium",
    "description": "Applies the Carr-Madan replication integral to infer fair variance strikes and MTM P&L. (Premium — subscribe at https://snowdrop.ai)",
}


def variance_swap_pricer() -> dict[str, Any]:
    """Premium skill — subscribe to access full implementation."""
    return paywall_response("variance_swap_pricer")
