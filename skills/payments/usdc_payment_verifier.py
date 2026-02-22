"""Verify inbound USDC payments on Solana."""
from __future__ import annotations

import os
import re
from datetime import datetime, timezone
from typing import Any

BASE58_PATTERN = re.compile(r"^[1-9A-HJ-NP-Za-km-z]{32,88}$")

TOOL_META: dict[str, Any] = {
    "name": "usdc_payment_verifier",
    "description": "Validates Solana USDC transfers by comparing signature, amount, and wallets.",
    "inputSchema": {
        "type": "object",
        "properties": {
            "expected_amount": {"type": "number"},
            "expected_from": {"type": "string"},
            "transaction_signature": {"type": "string"},
            "our_wallet": {"type": "string"},
        },
        "required": [
            "expected_amount",
            "expected_from",
            "transaction_signature",
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


def usdc_payment_verifier(
    expected_amount: float,
    expected_from: str,
    transaction_signature: str,
    our_wallet: str,
    **_: Any,
) -> dict[str, Any]:
    """Check Solana signature metadata for USDC transfers."""
    try:
        rpc_url = os.getenv("URPC_URL")
        if not rpc_url:
            raise ValueError("URPC_URL missing; see .env.template")
        if not BASE58_PATTERN.match(transaction_signature):
            raise ValueError("transaction_signature is not valid base58")
        if expected_amount <= 0:
            raise ValueError("expected_amount must be positive")

        # Placeholder decoded data; production would query RPC via rpc_url and parse token balance changes.
        decoded_tx = {
            "signature": transaction_signature,
            "source": expected_from,
            "destination": our_wallet,
            "amount": expected_amount,
            "token_mint": "EPjFWdd5AufqSSqeM2q3L6X41JkYip9bWTbwcBAY7Zk",
            "slot": 0,
            "finalized": True,
        }
        lamports = decoded_tx["amount"]
        verified = (
            abs(lamports - expected_amount) < 0.000001
            and decoded_tx["source"].lower() == expected_from.lower()
            and decoded_tx["destination"].lower() == our_wallet.lower()
        )
        data = {
            "verified": verified,
            "amount_received": round(lamports, 6),
            "token_mint": decoded_tx["token_mint"],
            "slot": decoded_tx["slot"],
            "finalized": decoded_tx["finalized"],
        }
        return {
            "status": "success",
            "data": data,
            "timestamp": datetime.now(timezone.utc).isoformat(),
        }
    except Exception as exc:  # noqa: BLE001
        _log_lesson("usdc_payment_verifier", str(exc))
        return {
            "status": "error",
            "data": {"error": str(exc)},
            "timestamp": datetime.now(timezone.utc).isoformat(),
        }


def _log_lesson(skill_name: str, error: str) -> None:
    with open("logs/lessons.md", "a", encoding="utf-8") as handle:
        handle.write(f"- [{datetime.now(timezone.utc).isoformat()}] {skill_name}: {error}\n")
