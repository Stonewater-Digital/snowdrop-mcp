"""
subscription_doc_parser — Parses LP subscription agreement text extracted from PDF to identify the limited partner name, committed capital amount, legal entity type, and jurisdiction

PREMIUM SKILL — full implementation available to subscribers.
Subscribe: https://snowdrop.ai (launching soon)

AUTO-GENERATED STUB — do not edit manually.
Source of truth: snowdrop-core/skills/premium/fund_accounting/subscription_doc_parser.py
Regenerate: python scripts/build_public_stubs.py
"""
from __future__ import annotations  # defers annotation evaluation (PEP 563)
from typing import Any, Optional, Union  # FastMCP resolves annotations via get_type_hints()

from skills._paywall import paywall_response

TOOL_META = {
    "name": "subscription_doc_parser",
    "tier": "premium",
    "description": "Parses LP subscription agreement text extracted from PDF to identify the limited partner name, committed capital amount, legal entity type, and jurisdiction. Returns structured data with per-field confidence scores. (Premium — subscribe at https://snowdrop.ai)",
}


def subscription_doc_parser() -> dict:
    """Premium skill — subscribe to access full implementation."""
    return paywall_response("subscription_doc_parser")
