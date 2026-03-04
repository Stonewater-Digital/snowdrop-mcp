"""
transaction_ingest_bridge — Fetches or accepts Mercury/Kraken transaction payloads and normalizes them for Ghost Ledger ingestion

PREMIUM SKILL — full implementation available to subscribers.
Subscribe: https://snowdrop.ai (launching soon)

AUTO-GENERATED STUB — do not edit manually.
Source of truth: snowdrop-core/skills/premium/fund_accounting/transaction_ingest_bridge.py
Regenerate: python scripts/build_public_stubs.py
"""
from __future__ import annotations  # defers annotation evaluation (PEP 563)
from typing import Any, Optional, Union  # FastMCP resolves annotations via get_type_hints()

from skills._paywall import paywall_response

TOOL_META = {
    "name": "transaction_ingest_bridge",
    "tier": "premium",
    "description": "Fetches or accepts Mercury/Kraken transaction payloads and normalizes them for Ghost Ledger ingestion. (Premium — subscribe at https://snowdrop.ai)",
}


def transaction_ingest_bridge(mercury_feed: list[dict[str, Any]] | None = None, kraken_feed: list[dict[str, Any]] | None = None) -> dict[str, Any]:
    """Premium skill — subscribe to access full implementation."""
    return paywall_response("transaction_ingest_bridge")
