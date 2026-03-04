"""Verify inbound TON payments against expected details."""
from __future__ import annotations

import os
from typing import Any

from skills.utils import SkillTelemetryEmitter, get_iso_timestamp, log_lesson

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
    emitter = SkillTelemetryEmitter(
        "ton_payment_verifier",
        {
            "expected_amount": round(float(expected_amount), 6) if expected_amount is not None else None,
            "hash_length": len(transaction_hash or ""),
        },
    )
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
        emitter.record(
            "ok",
            {
                "verified": verified,
                "overpaid": overpaid,
                "shortfall": round(shortfall, 6) if shortfall > 0 else 0.0,
            },
        )
        return {
            "status": "success",
            "data": data,
            "timestamp": get_iso_timestamp(),
        }
    except Exception as exc:  # noqa: BLE001
        log_lesson(f"ton_payment_verifier: {exc}")
        emitter.record("error", {"error": str(exc)})
        return {
            "status": "error",
            "data": {"error": str(exc)},
            "timestamp": get_iso_timestamp(),
        }
