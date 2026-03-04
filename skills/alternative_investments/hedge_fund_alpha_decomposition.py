"""
hedge_fund_alpha_decomposition — Performs multi-factor OLS (Fama-French-Carhart) to estimate alpha, betas, R², and information ratio for hedge fund returns

PREMIUM SKILL — full implementation available to subscribers.
Subscribe: https://snowdrop.ai (launching soon)

AUTO-GENERATED STUB — do not edit manually.
Source of truth: snowdrop-core/skills/premium/alternative_investments/hedge_fund_alpha_decomposition.py
Regenerate: python scripts/build_public_stubs.py
"""
from __future__ import annotations  # defers annotation evaluation (PEP 563)
from typing import Any, Optional, Union  # FastMCP resolves annotations via get_type_hints()

from skills._paywall import paywall_response

TOOL_META = {
    "name": "hedge_fund_alpha_decomposition",
    "tier": "premium",
    "description": "Performs multi-factor OLS (Fama-French-Carhart) to estimate alpha, betas, R², and information ratio for hedge fund returns. (Premium — subscribe at https://snowdrop.ai)",
}


def hedge_fund_alpha_decomposition(fund_returns: List[float], factor_returns: Dict[str, List[float]], risk_free_rate: float) -> dict[str, Any]:
    """Premium skill — subscribe to access full implementation."""
    return paywall_response("hedge_fund_alpha_decomposition")
