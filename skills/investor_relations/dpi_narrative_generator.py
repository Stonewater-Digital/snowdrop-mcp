"""
dpi_narrative_generator — Converts DPI metrics into LP-facing narrative with severity tiers when below target

PREMIUM SKILL — full implementation available to subscribers.
Subscribe: https://snowdrop.ai (launching soon)

AUTO-GENERATED STUB — do not edit manually.
Source of truth: snowdrop-core/skills/premium/investor_relations/dpi_narrative_generator.py
Regenerate: python scripts/build_public_stubs.py
"""
from __future__ import annotations  # defers annotation evaluation (PEP 563)
from typing import Any, Optional, Union  # FastMCP resolves annotations via get_type_hints()

from skills._paywall import paywall_response

TOOL_META = {
    "name": "dpi_narrative_generator",
    "tier": "premium",
    "description": "Converts DPI metrics into LP-facing narrative with severity tiers when below target. (Premium — subscribe at https://snowdrop.ai)",
}


def dpi_narrative_generator(lp_name: str, contributed: float, distributed: float, residual_value: float = 0.0, target_dpi: float = 1.5) -> dict[str, Any]:
    """Premium skill — subscribe to access full implementation."""
    return paywall_response("dpi_narrative_generator")
