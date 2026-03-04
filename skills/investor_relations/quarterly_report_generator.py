"""
quarterly_report_generator — Summarizes fund performance against benchmarks for the quarter

PREMIUM SKILL — full implementation available to subscribers.
Subscribe: https://snowdrop.ai (launching soon)

AUTO-GENERATED STUB — do not edit manually.
Source of truth: snowdrop-core/skills/premium/investor_relations/quarterly_report_generator.py
Regenerate: python scripts/build_public_stubs.py
"""
from __future__ import annotations  # defers annotation evaluation (PEP 563)
from typing import Any, Optional, Union  # FastMCP resolves annotations via get_type_hints()

from skills._paywall import paywall_response

TOOL_META = {
    "name": "quarterly_report_generator",
    "tier": "premium",
    "description": "Summarizes fund performance against benchmarks for the quarter. (Premium — subscribe at https://snowdrop.ai)",
}


def quarterly_report_generator(quarter: str, revenue_by_source: dict[str, float], expenses_by_category: dict[str, float], portfolio_values: dict[str, float], benchmark_return: float) -> dict[str, Any]:
    """Premium skill — subscribe to access full implementation."""
    return paywall_response("quarterly_report_generator")
