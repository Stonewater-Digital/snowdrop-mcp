"""
fund_expense_allocator — Allocates a total expense amount across sub-funds based on their chosen allocation basis: 'pro_rata_nav' (weighted by current NAV), 'equal' (split evenly), or 'committed_capital' (weighted by LP capital commitments)

PREMIUM SKILL — full implementation available to subscribers.
Subscribe: https://snowdrop.ai (launching soon)

AUTO-GENERATED STUB — do not edit manually.
Source of truth: snowdrop-core/skills/premium/fund_accounting/fund_expense_allocator.py
Regenerate: python scripts/build_public_stubs.py
"""
from __future__ import annotations  # defers annotation evaluation (PEP 563)
from typing import Any, Optional, Union  # FastMCP resolves annotations via get_type_hints()

from skills._paywall import paywall_response

TOOL_META = {
    "name": "fund_expense_allocator",
    "tier": "premium",
    "description": "Allocates a total expense amount across sub-funds based on their chosen allocation basis: 'pro_rata_nav' (weighted by current NAV), 'equal' (split evenly), or 'committed_capital' (weighted by LP capital commitments). Returns dollar allocations and percentage shares for each sub-fund. (Premium — subscribe at https://snowdrop.ai)",
}


def fund_expense_allocator(total_expenses: float, sub_funds: list) -> dict:
    """Premium skill — subscribe to access full implementation."""
    return paywall_response("fund_expense_allocator")
