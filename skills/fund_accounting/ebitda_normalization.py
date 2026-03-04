"""
ebitda_normalization — Scrubs and normalizes reported EBITDA by categorizing and summing add-back adjustments for M&A due diligence

PREMIUM SKILL — full implementation available to subscribers.
Subscribe: https://snowdrop.ai (launching soon)

AUTO-GENERATED STUB — do not edit manually.
Source of truth: snowdrop-core/skills/premium/fund_accounting/ebitda_normalization.py
Regenerate: python scripts/build_public_stubs.py
"""
from __future__ import annotations  # defers annotation evaluation (PEP 563)
from typing import Any, Optional, Union  # FastMCP resolves annotations via get_type_hints()

from skills._paywall import paywall_response

TOOL_META = {
    "name": "ebitda_normalization",
    "tier": "premium",
    "description": "Scrubs and normalizes reported EBITDA by categorizing and summing add-back adjustments for M&A due diligence. (Premium — subscribe at https://snowdrop.ai)",
}


def ebitda_normalization(reported_ebitda: float, adjustments: list[dict[str, Any]]) -> dict:
    """Premium skill — subscribe to access full implementation."""
    return paywall_response("ebitda_normalization")
