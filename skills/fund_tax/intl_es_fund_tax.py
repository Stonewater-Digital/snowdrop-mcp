"""
intl_es_fund_tax — Analyzes Spanish savings tax withholding and corporate tax for Spanish managers

PREMIUM SKILL — full implementation available to subscribers.
Subscribe: https://snowdrop.ai (launching soon)

AUTO-GENERATED STUB — do not edit manually.
Source of truth: snowdrop-core/skills/premium/fund_tax/intl_es_fund_tax.py
Regenerate: python scripts/build_public_stubs.py
"""
from __future__ import annotations  # defers annotation evaluation (PEP 563)
from typing import Any, Optional, Union  # FastMCP resolves annotations via get_type_hints()

from skills._paywall import paywall_response

TOOL_META = {
    "name": "intl_es_fund_tax",
    "tier": "premium",
    "description": "Analyzes Spanish savings tax withholding and corporate tax for Spanish managers. (Premium — subscribe at https://snowdrop.ai)",
}


def intl_es_fund_tax() -> dict:
    """Premium skill — subscribe to access full implementation."""
    return paywall_response("intl_es_fund_tax")
