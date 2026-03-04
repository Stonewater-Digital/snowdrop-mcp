"""
latency_optimized_order_routing — Selects the optimal server route for a trade order by ranking available exchange server locations by latency and filtering out unreliable routes (reliability < 99%)

PREMIUM SKILL — full implementation available to subscribers.
Subscribe: https://snowdrop.ai (launching soon)

AUTO-GENERATED STUB — do not edit manually.
Source of truth: snowdrop-core/skills/premium/technical/latency_optimized_order_routing.py
Regenerate: python scripts/build_public_stubs.py
"""
from __future__ import annotations  # defers annotation evaluation (PEP 563)
from typing import Any, Optional, Union  # FastMCP resolves annotations via get_type_hints()

from skills._paywall import paywall_response

TOOL_META = {
    "name": "latency_optimized_order_routing",
    "tier": "premium",
    "description": "Selects the optimal server route for a trade order by ranking available exchange server locations by latency and filtering out unreliable routes (reliability < 99%). Returns the winning route, ranked alternatives, and estimated execution time advantage over the median route. (Premium — subscribe at https://snowdrop.ai)",
}


def latency_optimized_order_routing(order: dict[str, Any], server_locations: list[dict[str, Any]]) -> dict[str, Any]:
    """Premium skill — subscribe to access full implementation."""
    return paywall_response("latency_optimized_order_routing")
