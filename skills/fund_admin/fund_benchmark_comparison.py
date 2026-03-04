"""
fund_benchmark_comparison — Compares a fund's KPIs to benchmark values and flags underperformance

PREMIUM SKILL — full implementation available to subscribers.
Subscribe: https://snowdrop.ai (launching soon)

AUTO-GENERATED STUB — do not edit manually.
Source of truth: snowdrop-core/skills/premium/fund_admin/fund_benchmark_comparison.py
Regenerate: python scripts/build_public_stubs.py
"""
from __future__ import annotations  # defers annotation evaluation (PEP 563)
from typing import Any, Optional, Union  # FastMCP resolves annotations via get_type_hints()

from skills._paywall import paywall_response

TOOL_META = {
    "name": "fund_benchmark_comparison",
    "tier": "premium",
    "description": "Compares a fund's KPIs to benchmark values and flags underperformance. Returns per-metric deltas, beat/miss flags, and overall hit rate. (Premium — subscribe at https://snowdrop.ai)",
}


def fund_benchmark_comparison(fund_metrics: dict[str, float], benchmark_metrics: dict[str, float]) -> dict[str, Any]:
    """Premium skill — subscribe to access full implementation."""
    return paywall_response("fund_benchmark_comparison")
