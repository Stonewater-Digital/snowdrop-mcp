"""Lightweight sanctions screening covering OFAC themes."""
from __future__ import annotations

import difflib
from datetime import datetime, timezone
from typing import Any

TOOL_META: dict[str, Any] = {
    "name": "sanctions_screener",
    "description": "Checks entities/wallets against curated sanctions heuristics.",
    "inputSchema": {
        "type": "object",
        "properties": {
            "entity": {"type": "string"},
            "entity_type": {
                "type": "string",
                "enum": ["individual", "organization", "wallet_address"],
            },
            "chains_to_check": {
                "type": "array",
                "items": {"type": "string"},
            },
        },
        "required": ["entity", "entity_type", "chains_to_check"],
    },
    "outputSchema": {
        "type": "object",
        "properties": {
            "status": {"type": "string"},
            "data": {"type": "object"},
            "timestamp": {"type": "string"},
        },
    },
}

WATCHLIST = [
    {"label": "Tornado Cash", "type": "organization", "markers": ["0x8589427373d6d84e98730d7795d8f6f8731e0e03"]},
    {"label": "Lazarus Group", "type": "organization", "markers": ["lazarus", "labyrinth", "0x098be8"]},
    {"label": "Sinbad Mixer", "type": "organization", "markers": ["sinbad", "0x0aa"], "chains": ["btc", "eth"]},
]


def sanctions_screener(
    entity: str,
    entity_type: str,
    chains_to_check: list[str],
    **_: Any,
) -> dict[str, Any]:
    """Return sanction match evaluation with heuristic confidence."""

    try:
        normalized_entity = entity.lower()
        best_match: dict[str, Any] | None = None
        best_confidence = 0.0
        details = ""
        for watch in WATCHLIST:
            if watch.get("chains") and not any(chain.lower() in watch["chains"] for chain in chains_to_check):
                continue
            ratio = difflib.SequenceMatcher(None, normalized_entity, watch["label"].lower()).ratio()
            for marker in watch.get("markers", []):
                if marker in normalized_entity:
                    ratio = max(ratio, 0.95)
                    details = f"Matched marker {marker}"
                    break
            if ratio > best_confidence:
                best_confidence = ratio
                best_match = watch

        sanctioned = best_confidence >= 0.75
        match_type = best_match["label"] if best_match else "none"
        if sanctioned and not details:
            details = f"High similarity to {match_type}"
        data = {
            "sanctioned": sanctioned,
            "match_type": match_type,
            "confidence": round(best_confidence, 3),
            "details": details,
        }
        return {
            "status": "success",
            "data": data,
            "timestamp": datetime.now(timezone.utc).isoformat(),
        }
    except Exception as exc:
        _log_lesson("sanctions_screener", str(exc))
        return {
            "status": "error",
            "data": {"error": str(exc)},
            "timestamp": datetime.now(timezone.utc).isoformat(),
        }


def _log_lesson(skill_name: str, error: str) -> None:
    with open("logs/lessons.md", "a", encoding="utf-8") as handle:
        handle.write(f"- [{datetime.now(timezone.utc).isoformat()}] {skill_name}: {error}\n")
