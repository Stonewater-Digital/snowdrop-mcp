"""
waterfall_sensitivity_analyzer — Evaluates GP carry payouts across a grid of hurdle rates and carry percentages using a full 4-tier waterfall (ROC, pref, catch-up, split)

PREMIUM SKILL — full implementation available to subscribers.
Subscribe: https://snowdrop.ai (launching soon)

AUTO-GENERATED STUB — do not edit manually.
Source of truth: snowdrop-core/skills/premium/fund_admin/waterfall_sensitivity_analyzer.py
Regenerate: python scripts/build_public_stubs.py
"""
from __future__ import annotations  # defers annotation evaluation (PEP 563)
from typing import Any, Optional, Union  # FastMCP resolves annotations via get_type_hints()

from skills._paywall import paywall_response

TOOL_META = {
    "name": "waterfall_sensitivity_analyzer",
    "tier": "premium",
    "description": "Evaluates GP carry payouts across a grid of hurdle rates and carry percentages using a full 4-tier waterfall (ROC, pref, catch-up, split). Returns a sensitivity matrix and identifies optimal scenarios. (Premium — subscribe at https://snowdrop.ai)",
}


def waterfall_sensitivity_analyzer(capital_contributed: float, gross_proceeds: float, hurdle_rates: Sequence[float], carry_rates: Sequence[float], years: float = 1.0) -> dict[str, Any]:
    """Premium skill — subscribe to access full implementation."""
    return paywall_response("waterfall_sensitivity_analyzer")
