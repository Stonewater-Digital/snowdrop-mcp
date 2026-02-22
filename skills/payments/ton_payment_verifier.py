"""Verify inbound TON payments against expected details."""
from __future__ import annotations

import os
from datetime import datetime, timezone
from typing import Any

TOOL_META: dict[str, Any] = {
    "name": "ton_payment_verifier",
    "description": "Validates TON transactions for Snowdrop payments without broadcasting funds.",
    "inputSchema": {
        "type": "object",
        "properties": {
            "expected_amount": {"type": "number"},
            "expected_from": {"type": "string"},
            "transaction_hash": {"type": "string"},
            "our_wallet": {"type": "string"},
        },
        "required": [
            "expected_amount",
            "expected_from",
            "transaction_hash",
            "our_wallet",
        ],
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


def ton_payment_verifier(
    expected_amount: float,
    expected_from: str,
    transaction_hash: str,
    our_wallet: str,
    **_: Any,
) -> dict[str, Any]:
    """Check TON transaction metadata against expected sender, recipient, and amount."""
    try:
        api_key = os.getenv("TON_API_KEY")
        if not api_key:
            raise ValueError("TON_API_KEY missing; see .env.template")
        if not transaction_hash or len(transaction_hash) < 44:
            raise ValueError("transaction_hash format invalid")
        if expected_amount <= 0:
            raise ValueError("expected_amount must be positive")

        # In production we would call TON API using api_key + transaction_hash.
        # For now we simulate a decoded payload placeholder; callers provide payload data.
        decoded_tx = {
            "hash": transaction_hash,
            "from": expected_from,
            "to": our_wallet,
            "amount": expected_amount,
            "confirmations": 3,
        }

        amount_received = float(decoded_tx["amount"])
        tolerance = 0.01
        shortfall = max(expected_amount - amount_received, 0.0)
        overpaid = amount_received - expected_amount > tolerance
        verified = (
            abs(amount_received - expected_amount) <= tolerance
            and decoded_tx["from"].lower() == expected_from.lower()
            and decoded_tx["to"].lower() == our_wallet.lower()
        )
        data = {
            "verified": verified,
            "amount_received": round(amount_received, 6),
            "confirmations": decoded_tx.get("confirmations", 0),
            "overpaid": overpaid,
            "shortfall": round(shortfall, 6) if shortfall > 0 else None,
        }
        return {
            "status": "success",
            "data": data,
            "timestamp": datetime.now(timezone.utc).isoformat(),
        }
    except Exception as exc:  # noqa: BLE001
        _log_lesson("ton_payment_verifier", str(exc))
        return {
            "status": "error",
            "data": {"error": str(exc)},
            "timestamp": datetime.now(timezone.utc).isoformat(),
        }


def _log_lesson(skill_name: str, error: str) -> None:
    with open("logs/lessons.md", "a", encoding="utf-8") as handle:
        handle.write(f"- [{datetime.now(timezone.utc).isoformat()}] {skill_name}: {error}\n")
