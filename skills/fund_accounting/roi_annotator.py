"""
roi_annotator — Enriches ledger transactions with qualitative ROI commentary

PREMIUM SKILL — full implementation available to subscribers.
Subscribe: https://snowdrop.ai (launching soon)

AUTO-GENERATED STUB — do not edit manually.
Source of truth: snowdrop-core/skills/premium/fund_accounting/roi_annotator.py
Regenerate: python scripts/build_public_stubs.py
"""
from __future__ import annotations  # defers annotation evaluation (PEP 563)
from typing import Any, Optional, Union  # FastMCP resolves annotations via get_type_hints()

from skills._paywall import paywall_response

TOOL_META = {
    "name": "roi_annotator",
    "tier": "premium",
    "description": "Enriches ledger transactions with qualitative ROI commentary. (Premium — subscribe at https://snowdrop.ai)",
}


def roi_annotator(transaction: dict[str, Any]) -> dict[str, Any]:
    """Premium skill — subscribe to access full implementation."""
    return paywall_response("roi_annotator")
