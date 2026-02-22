"""Prepare unsigned Solana transfer payloads."""
from __future__ import annotations

import re
from datetime import datetime, timezone
from typing import Any

TOOL_META: dict[str, Any] = {
    "name": "sol_transfer_builder",
    "description": "Constructs Solana transfer payloads and fee estimates pending approval.",
    "inputSchema": {
        "type": "object",
        "properties": {
            "from_pubkey": {"type": "string"},
            "to_pubkey": {"type": "string"},
            "amount_sol": {"type": "number"},
            "memo": {"type": ["string", "null"]},
        },
        "required": ["from_pubkey", "to_pubkey", "amount_sol"],
    },
    "outputSchema": {
        "type": "object",
        "properties": {
            "status": {"type": "string"},
            "data": {
                "type": "object",
                "properties": {
                    "transaction": {"type": "object"},
                    "execution": {"type": "string"},
                    "estimated_fee_sol": {"type": "number"},
                },
            },
            "timestamp": {"type": "string"},
        },
    },
}

BASE58_PATTERN = re.compile(r"^[1-9A-HJ-NP-Za-km-z]{32,44}$")


def sol_transfer_builder(
    from_pubkey: str,
    to_pubkey: str,
    amount_sol: float,
    memo: str | None = None,
    **_: Any,
) -> dict[str, Any]:
    """Return unsigned Solana transfer details."""

    try:
        if not BASE58_PATTERN.match(from_pubkey):
            raise ValueError("from_pubkey must be a valid base58 string")
        if not BASE58_PATTERN.match(to_pubkey):
            raise ValueError("to_pubkey must be a valid base58 string")
        if amount_sol <= 0:
            raise ValueError("amount_sol must be positive")

        transaction = {
            "from": from_pubkey,
            "to": to_pubkey,
            "amount": round(amount_sol, 9),
            "memo": memo,
        }
        data = {
            "transaction": transaction,
            "execution": "pending_thunder_approval",
            "estimated_fee_sol": 0.0005,
        }
        return {
            "status": "success",
            "data": data,
            "timestamp": datetime.now(timezone.utc).isoformat(),
        }
    except Exception as exc:
        _log_lesson("sol_transfer_builder", str(exc))
        return {
            "status": "error",
            "data": {"error": str(exc)},
            "timestamp": datetime.now(timezone.utc).isoformat(),
        }


def _log_lesson(skill_name: str, error: str) -> None:
    with open("logs/lessons.md", "a", encoding="utf-8") as handle:
        handle.write(f"- [{datetime.now(timezone.utc).isoformat()}] {skill_name}: {error}\n")
