"""
hardware_wallet_handshake — Gate-keeps large on-chain transfers by requiring hardware wallet confirmation when a transaction exceeds the configured USD threshold

PREMIUM SKILL — full implementation available to subscribers.
Subscribe: https://snowdrop.ai (launching soon)

AUTO-GENERATED STUB — do not edit manually.
Source of truth: snowdrop-core/skills/premium/technical/hardware_wallet_handshake.py
Regenerate: python scripts/build_public_stubs.py
"""
from __future__ import annotations  # defers annotation evaluation (PEP 563)
from typing import Any, Optional, Union  # FastMCP resolves annotations via get_type_hints()

from skills._paywall import paywall_response

TOOL_META = {
    "name": "hardware_wallet_handshake",
    "tier": "premium",
    "description": "Gate-keeps large on-chain transfers by requiring hardware wallet confirmation when a transaction exceeds the configured USD threshold. Generates a cryptographically random nonce and a confirmation request payload with a 5-minute expiry window. (Premium — subscribe at https://snowdrop.ai)",
}


def hardware_wallet_handshake(transaction: dict[str, Any], threshold_usd: float = 5000.0) -> dict[str, Any]:
    """Premium skill — subscribe to access full implementation."""
    return paywall_response("hardware_wallet_handshake")
