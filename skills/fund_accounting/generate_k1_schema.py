"""
generate_k1_schema — Structures partner tax allocation data into an IRS-compatible Schedule K-1 JSON schema with Part III line items

PREMIUM SKILL — full implementation available to subscribers.
Subscribe: https://snowdrop.ai (launching soon)

AUTO-GENERATED STUB — do not edit manually.
Source of truth: snowdrop-core/skills/premium/fund_accounting/generate_k1_schema.py
Regenerate: python scripts/build_public_stubs.py
"""
from __future__ import annotations  # defers annotation evaluation (PEP 563)
from typing import Any, Optional, Union  # FastMCP resolves annotations via get_type_hints()

from skills._paywall import paywall_response

TOOL_META = {
    "name": "generate_k1_schema",
    "tier": "premium",
    "description": "Structures partner tax allocation data into an IRS-compatible Schedule K-1 JSON schema with Part III line items. (Premium — subscribe at https://snowdrop.ai)",
}


def generate_k1_schema(partner_id: str, fund_id: str, tax_year: int, allocations: dict[str, float]) -> dict:
    """Premium skill — subscribe to access full implementation."""
    return paywall_response("generate_k1_schema")
