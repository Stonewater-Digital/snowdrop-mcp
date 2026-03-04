"""
crs_reporting_classifier — Flags CRS reportable accounts per OECD CRS Section VIII definitions

PREMIUM SKILL — full implementation available to subscribers.
Subscribe: https://snowdrop.ai (launching soon)

AUTO-GENERATED STUB — do not edit manually.
Source of truth: snowdrop-core/skills/premium/fund_tax/crs_reporting_classifier.py
Regenerate: python scripts/build_public_stubs.py
"""
from __future__ import annotations  # defers annotation evaluation (PEP 563)
from typing import Any, Optional, Union  # FastMCP resolves annotations via get_type_hints()

from skills._paywall import paywall_response

TOOL_META = {
    "name": "crs_reporting_classifier",
    "tier": "premium",
    "description": "Flags CRS reportable accounts per OECD CRS Section VIII definitions. (Premium — subscribe at https://snowdrop.ai)",
}


def crs_reporting_classifier() -> dict:
    """Premium skill — subscribe to access full implementation."""
    return paywall_response("crs_reporting_classifier")
