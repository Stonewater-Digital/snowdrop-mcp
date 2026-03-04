"""
multi_jurisdiction_net_return — Combines treaty withholding, local fund tax, and investor-level tax drag across income types

PREMIUM SKILL — full implementation available to subscribers.
Subscribe: https://snowdrop.ai (launching soon)

AUTO-GENERATED STUB — do not edit manually.
Source of truth: snowdrop-core/skills/premium/fund_tax/multi_jurisdiction_net_return.py
Regenerate: python scripts/build_public_stubs.py
"""
from __future__ import annotations  # defers annotation evaluation (PEP 563)
from typing import Any, Optional, Union  # FastMCP resolves annotations via get_type_hints()

from skills._paywall import paywall_response

TOOL_META = {
    "name": "multi_jurisdiction_net_return",
    "tier": "premium",
    "description": "Combines treaty withholding, local fund tax, and investor-level tax drag across income types. (Premium — subscribe at https://snowdrop.ai)",
}


def multi_jurisdiction_net_return() -> dict:
    """Premium skill — subscribe to access full implementation."""
    return paywall_response("multi_jurisdiction_net_return")
