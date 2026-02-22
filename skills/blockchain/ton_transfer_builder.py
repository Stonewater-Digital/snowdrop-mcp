"""Prepare unsigned TON transfer payloads."""
from __future__ import annotations

import base64
from datetime import datetime, timezone
from typing import Any

TOOL_META: dict[str, Any] = {
    "name": "ton_transfer_builder",
    "description": "Constructs TON transfer payloads without broadcasting.",
    "inputSchema": {
        "type": "object",
        "properties": {
            "from_address": {"type": "string"},
            "to_address": {"type": "string"},
            "amount_ton": {"type": "number"},
            "memo": {"type": ["string", "null"]},
        },
        "required": ["from_address", "to_address", "amount_ton"],
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
                    "estimated_fee_ton": {"type": "number"},
                },
            },
            "timestamp": {"type": "string"},
        },
    },
}


def ton_transfer_builder(
    from_address: str,
    to_address: str,
    amount_ton: float,
    memo: str | None = None,
    **_: Any,
) -> dict[str, Any]:
    """Return an unsigned TON transfer payload."""

    try:
        _validate_ton_address(from_address)
        _validate_ton_address(to_address)
        if amount_ton <= 0:
            raise ValueError("amount_ton must be positive")

        transaction = {
            "from": from_address,
            "to": to_address,
            "amount": round(amount_ton, 9),
            "memo": memo,
        }
        data = {
            "transaction": transaction,
            "execution": "pending_thunder_approval",
            "estimated_fee_ton": 0.02,
        }
        return {
            "status": "success",
            "data": data,
            "timestamp": datetime.now(timezone.utc).isoformat(),
        }
    except Exception as exc:
        _log_lesson("ton_transfer_builder", str(exc))
        return {
            "status": "error",
            "data": {"error": str(exc)},
            "timestamp": datetime.now(timezone.utc).isoformat(),
        }


def _validate_ton_address(address: str) -> None:
    if len(address) != 48:
        raise ValueError("TON address must be 48 characters of base64")
    try:
        base64.b64decode(address + "==")
    except Exception as exc:  # pragma: no cover - base64 errors
        raise ValueError("Invalid TON base64 address") from exc


def _log_lesson(skill_name: str, error: str) -> None:
    with open("logs/lessons.md", "a", encoding="utf-8") as handle:
        handle.write(f"- [{datetime.now(timezone.utc).isoformat()}] {skill_name}: {error}\n")
