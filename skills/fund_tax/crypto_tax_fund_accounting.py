"""
crypto_tax_fund_accounting — Applies FIFO cost basis to crypto trades per IRS Notice 2014-21 and captures staking income

PREMIUM SKILL — full implementation available to subscribers.
Subscribe: https://snowdrop.ai (launching soon)

AUTO-GENERATED STUB — do not edit manually.
Source of truth: snowdrop-core/skills/premium/fund_tax/crypto_tax_fund_accounting.py
Regenerate: python scripts/build_public_stubs.py
"""
from __future__ import annotations  # defers annotation evaluation (PEP 563)
from typing import Any, Optional, Union  # FastMCP resolves annotations via get_type_hints()

from skills._paywall import paywall_response

TOOL_META = {
    "name": "crypto_tax_fund_accounting",
    "tier": "premium",
    "description": "Applies FIFO cost basis to crypto trades per IRS Notice 2014-21 and captures staking income. (Premium — subscribe at https://snowdrop.ai)",
}


def crypto_tax_fund_accounting() -> dict:
    """Premium skill — subscribe to access full implementation."""
    return paywall_response("crypto_tax_fund_accounting")
