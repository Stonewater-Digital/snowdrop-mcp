"""
weather_derivative_pricer — Converts historical temperatures into HDD/CDD indices, computes expected payout, and delivers burn analysis statistics

PREMIUM SKILL — full implementation available to subscribers.
Subscribe: https://snowdrop.ai (launching soon)

AUTO-GENERATED STUB — do not edit manually.
Source of truth: snowdrop-core/skills/premium/structured_products/weather_derivative_pricer.py
Regenerate: python scripts/build_public_stubs.py
"""
from __future__ import annotations  # defers annotation evaluation (PEP 563)
from typing import Any, Optional, Union  # FastMCP resolves annotations via get_type_hints()

from skills._paywall import paywall_response

TOOL_META = {
    "name": "weather_derivative_pricer",
    "tier": "premium",
    "description": "Converts historical temperatures into HDD/CDD indices, computes expected payout, and delivers burn analysis statistics. (Premium — subscribe at https://snowdrop.ai)",
}


def weather_derivative_pricer(historical_temps: List[float], derivative_type: str, strike_index: float, tick_size: float, base_temperature: float = 65.0) -> dict[str, Any]:
    """Premium skill — subscribe to access full implementation."""
    return paywall_response("weather_derivative_pricer")
