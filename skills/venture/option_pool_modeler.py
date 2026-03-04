"""
option_pool_modeler — Evaluates current and proposed option pool sizing plus dilution to shareholders

PREMIUM SKILL — full implementation available to subscribers.
Subscribe: https://snowdrop.ai (launching soon)

AUTO-GENERATED STUB — do not edit manually.
Source of truth: snowdrop-core/skills/premium/venture/option_pool_modeler.py
Regenerate: python scripts/build_public_stubs.py
"""
from __future__ import annotations  # defers annotation evaluation (PEP 563)
from typing import Any, Optional, Union  # FastMCP resolves annotations via get_type_hints()

from skills._paywall import paywall_response

TOOL_META = {
    "name": "option_pool_modeler",
    "tier": "premium",
    "description": "Evaluates current and proposed option pool sizing plus dilution to shareholders. (Premium — subscribe at https://snowdrop.ai)",
}


def option_pool_modeler(current_pool_shares: int, current_pool_allocated: int, total_shares_outstanding: int, proposed_pool_increase_pct: float, new_round_pre_money: float | None = None) -> dict[str, Any]:
    """Premium skill — subscribe to access full implementation."""
    return paywall_response("option_pool_modeler")
