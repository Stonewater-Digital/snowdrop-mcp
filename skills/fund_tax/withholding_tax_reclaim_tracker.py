"""
withholding_tax_reclaim_tracker — Summarizes reclaimable withholding tax amounts and filing deadlines per country

PREMIUM SKILL — full implementation available to subscribers.
Subscribe: https://snowdrop.ai (launching soon)

AUTO-GENERATED STUB — do not edit manually.
Source of truth: snowdrop-core/skills/premium/fund_tax/withholding_tax_reclaim_tracker.py
Regenerate: python scripts/build_public_stubs.py
"""
from __future__ import annotations  # defers annotation evaluation (PEP 563)
from typing import Any, Optional, Union  # FastMCP resolves annotations via get_type_hints()

from skills._paywall import paywall_response

TOOL_META = {
    "name": "withholding_tax_reclaim_tracker",
    "tier": "premium",
    "description": "Summarizes reclaimable withholding tax amounts and filing deadlines per country. (Premium — subscribe at https://snowdrop.ai)",
}


def withholding_tax_reclaim_tracker() -> dict:
    """Premium skill — subscribe to access full implementation."""
    return paywall_response("withholding_tax_reclaim_tracker")
