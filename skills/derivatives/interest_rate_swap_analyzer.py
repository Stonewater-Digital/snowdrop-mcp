"""
interest_rate_swap_analyzer — Values a fixed/float interest rate swap and reports DV01 and break-even rate

PREMIUM SKILL — full implementation available to subscribers.
Subscribe: https://snowdrop.ai (launching soon)

AUTO-GENERATED STUB — do not edit manually.
Source of truth: snowdrop-core/skills/premium/derivatives/interest_rate_swap_analyzer.py
Regenerate: python scripts/build_public_stubs.py
"""
from __future__ import annotations  # defers annotation evaluation (PEP 563)
from typing import Any, Optional, Union  # FastMCP resolves annotations via get_type_hints()

from skills._paywall import paywall_response

TOOL_META = {
    "name": "interest_rate_swap_analyzer",
    "tier": "premium",
    "description": "Values a fixed/float interest rate swap and reports DV01 and break-even rate. (Premium — subscribe at https://snowdrop.ai)",
}


def interest_rate_swap_analyzer(notional: float, fixed_rate_pct: float, floating_rate_pct: float, maturity_years: float, payment_frequency: int = 2, discount_rate_pct: float = 0.0) -> dict[str, Any]:
    """Premium skill — subscribe to access full implementation."""
    return paywall_response("interest_rate_swap_analyzer")
