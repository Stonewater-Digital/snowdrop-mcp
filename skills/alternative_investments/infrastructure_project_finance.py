"""
infrastructure_project_finance — Constructs a single-asset project model to evaluate DSCR, LLCR, and equity IRR against capex and leverage assumptions

PREMIUM SKILL — full implementation available to subscribers.
Subscribe: https://snowdrop.ai (launching soon)

AUTO-GENERATED STUB — do not edit manually.
Source of truth: snowdrop-core/skills/premium/alternative_investments/infrastructure_project_finance.py
Regenerate: python scripts/build_public_stubs.py
"""
from __future__ import annotations  # defers annotation evaluation (PEP 563)
from typing import Any, Optional, Union  # FastMCP resolves annotations via get_type_hints()

from skills._paywall import paywall_response

TOOL_META = {
    "name": "infrastructure_project_finance",
    "tier": "premium",
    "description": "Constructs a single-asset project model to evaluate DSCR, LLCR, and equity IRR against capex and leverage assumptions. (Premium — subscribe at https://snowdrop.ai)",
}


def infrastructure_project_finance(capex: float, revenue_forecast: List[float], opex_forecast: List[float], debt_rate: float, debt_tenor_years: int, debt_ratio: float) -> dict[str, Any]:
    """Premium skill — subscribe to access full implementation."""
    return paywall_response("infrastructure_project_finance")
