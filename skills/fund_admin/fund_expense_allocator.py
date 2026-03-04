"""
fund_expense_allocator — Allocates fund-level expenses to LP capital accounts on a pro-rata basis using each LP's relative balance weight

PREMIUM SKILL — full implementation available to subscribers.
Subscribe: https://snowdrop.ai (launching soon)

AUTO-GENERATED STUB — do not edit manually.
Source of truth: snowdrop-core/skills/premium/fund_admin/fund_expense_allocator.py
Regenerate: python scripts/build_public_stubs.py
"""
from __future__ import annotations  # defers annotation evaluation (PEP 563)
from typing import Any, Optional, Union  # FastMCP resolves annotations via get_type_hints()

from skills._paywall import paywall_response

TOOL_META = {
    "name": "fund_expense_allocator",
    "tier": "premium",
    "description": "Allocates fund-level expenses to LP capital accounts on a pro-rata basis using each LP's relative balance weight. (Premium — subscribe at https://snowdrop.ai)",
}


def fund_expense_allocator(expense_amount: float, capital_accounts: list[dict[str, Any]]) -> dict[str, Any]:
    """Premium skill — subscribe to access full implementation."""
    return paywall_response("fund_expense_allocator")
