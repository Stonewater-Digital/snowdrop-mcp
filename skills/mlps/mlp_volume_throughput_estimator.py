"""
mlp_volume_throughput_estimator — Measures asset utilization and tariff revenue for MLP pipeline systems

PREMIUM SKILL — full implementation available to subscribers.
Subscribe: https://snowdrop.ai (launching soon)

AUTO-GENERATED STUB — do not edit manually.
Source of truth: snowdrop-core/skills/premium/mlps/mlp_volume_throughput_estimator.py
Regenerate: python scripts/build_public_stubs.py
"""
from __future__ import annotations  # defers annotation evaluation (PEP 563)
from typing import Any, Optional, Union  # FastMCP resolves annotations via get_type_hints()

from skills._paywall import paywall_response

TOOL_META = {
    "name": "mlp_volume_throughput_estimator",
    "tier": "premium",
    "description": "Measures asset utilization and tariff revenue for MLP pipeline systems. (Premium — subscribe at https://snowdrop.ai)",
}


def mlp_volume_throughput_estimator(throughput_barrels_per_day: float, capacity_barrels_per_day: float, tariff_per_barrel: float) -> dict[str, Any]:
    """Premium skill — subscribe to access full implementation."""
    return paywall_response("mlp_volume_throughput_estimator")
