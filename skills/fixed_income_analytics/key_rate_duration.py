"""
key_rate_duration — Computes key rate durations by bumping individual zero buckets (1/2/5/10/20/30y) consistent with the Basel IRRBB supervisory outlier test

PREMIUM SKILL — full implementation available to subscribers.
Subscribe: https://snowdrop.ai (launching soon)

AUTO-GENERATED STUB — do not edit manually.
Source of truth: snowdrop-core/skills/premium/fixed_income_analytics/key_rate_duration.py
Regenerate: python scripts/build_public_stubs.py
"""
from __future__ import annotations  # defers annotation evaluation (PEP 563)
from typing import Any, Optional, Union  # FastMCP resolves annotations via get_type_hints()

from skills._paywall import paywall_response

TOOL_META = {
    "name": "key_rate_duration",
    "tier": "premium",
    "description": "Computes key rate durations by bumping individual zero buckets (1/2/5/10/20/30y) consistent with the Basel IRRBB supervisory outlier test. (Premium — subscribe at https://snowdrop.ai)",
}


def key_rate_duration(zero_curve: List[Dict[str, float]], cashflows: List[Dict[str, float]], bump_size_bps: float = 1.0) -> dict[str, Any]:
    """Premium skill — subscribe to access full implementation."""
    return paywall_response("key_rate_duration")
