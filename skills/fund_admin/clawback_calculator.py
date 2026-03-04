"""
clawback_calculator — Determines GP clawback due when interim carried interest distributions exceed final entitlement

PREMIUM SKILL — full implementation available to subscribers.
Subscribe: https://snowdrop.ai (launching soon)

AUTO-GENERATED STUB — do not edit manually.
Source of truth: snowdrop-core/skills/premium/fund_admin/clawback_calculator.py
Regenerate: python scripts/build_public_stubs.py
"""
from __future__ import annotations  # defers annotation evaluation (PEP 563)
from typing import Any, Optional, Union  # FastMCP resolves annotations via get_type_hints()

from skills._paywall import paywall_response

TOOL_META = {
    "name": "clawback_calculator",
    "tier": "premium",
    "description": "Determines GP clawback due when interim carried interest distributions exceed final entitlement. Optionally applies interest on the outstanding clawback amount. (Premium — subscribe at https://snowdrop.ai)",
}


def clawback_calculator(carry_distributed: float, final_carry_entitlement: float, interest_rate_pct: float = 0.0, years_outstanding: float = 0.0, tax_rate_pct: float = 0.0) -> dict[str, Any]:
    """Premium skill — subscribe to access full implementation."""
    return paywall_response("clawback_calculator")
