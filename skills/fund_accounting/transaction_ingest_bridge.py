"""Normalize transactions sourced from Mercury and Kraken."""
from __future__ import annotations

import os
from datetime import datetime, timezone
from typing import Any

TOOL_META: dict[str, Any] = {
    "name": "transaction_ingest_bridge",
    "description": (
        "Fetches or accepts Mercury/Kraken transaction payloads and normalizes them for Ghost"
        " Ledger ingestion."
    ),
    "inputSchema": {
        "type": "object",
        "properties": {
            "mercury_feed": {
                "type": "array",
                "items": {"type": "object"},
                "description": "Optional pre-fetched Mercury transactions.",
            },
            "kraken_feed": {
                "type": "array",
                "items": {"type": "object"},
                "description": "Optional pre-fetched Kraken transactions.",
            },
        },
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


def transaction_ingest_bridge(
    mercury_feed: list[dict[str, Any]] | None = None,
    kraken_feed: list[dict[str, Any]] | None = None,
    **_: Any,
) -> dict[str, Any]:
    """Normalize and merge transactions across banking and exchange sources.

    Args:
        mercury_feed: Optional Mercury transactions to normalize.
        kraken_feed: Optional Kraken transactions to normalize.

    Returns:
        Envelope containing a combined list using the canonical ingestion schema.
    """

    try:
        if not os.getenv("MERCURY_API_TOKEN"):
            raise ValueError("MERCURY_API_TOKEN missing; see .env.template")
        if not os.getenv("KRAKEN_API_KEY"):
            raise ValueError("KRAKEN_API_KEY missing; see .env.template")

        normalized: list[dict[str, Any]] = []

        for tx in mercury_feed or []:
            normalized.append(_normalize_mercury(tx))

        for tx in kraken_feed or []:
            normalized.append(_normalize_kraken(tx))

        return {
            "status": "success",
            "data": {"records": normalized, "count": len(normalized)},
            "timestamp": datetime.now(timezone.utc).isoformat(),
        }
    except Exception as exc:
        _log_lesson("transaction_ingest_bridge", str(exc))
        return {
            "status": "error",
            "data": {"error": str(exc)},
            "timestamp": datetime.now(timezone.utc).isoformat(),
        }


def _normalize_mercury(tx: dict[str, Any]) -> dict[str, Any]:
    return {
        "source": "mercury",
        "tx_id": str(tx.get("id") or tx.get("transaction_id") or tx.get("ref")),
        "amount": float(tx.get("amount", 0) or 0),
        "currency": tx.get("currency", "USD"),
        "category": (tx.get("category") or "operations").lower(),
        "p": {
            "posted_at": tx.get("posted_at") or tx.get("created_at"),
            "memo": tx.get("memo") or tx.get("description"),
        },
    }


def _normalize_kraken(tx: dict[str, Any]) -> dict[str, Any]:
    return {
        "source": "kraken",
        "tx_id": str(tx.get("txid") or tx.get("id") or tx.get("ledger_id")),
        "amount": float(tx.get("amount", 0) or tx.get("vol", 0) or 0),
        "currency": tx.get("asset") or tx.get("currency") or "USD",
        "category": (tx.get("type") or tx.get("class") or "trade").lower(),
        "p": {
            "posted_at": tx.get("time") or tx.get("timestamp"),
            "memo": tx.get("description") or tx.get("note"),
        },
    }


def _log_lesson(skill_name: str, error: str) -> None:
    with open("logs/lessons.md", "a", encoding="utf-8") as handle:
        handle.write(f"- [{datetime.now(timezone.utc).isoformat()}] {skill_name}: {error}\n")
