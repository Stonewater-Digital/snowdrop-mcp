"""Prepare (but never execute) Mercury payments."""
from __future__ import annotations

import os
from datetime import datetime, timezone
from typing import Any

TOOL_META: dict[str, Any] = {
    "name": "mercury_payment_sender",
    "description": (
        "Constructs ACH/wire payloads for Mercury but leaves them pending Thunder approval."
    ),
    "inputSchema": {
        "type": "object",
        "properties": {
            "origin_account_id": {"type": "string"},
            "amount": {"type": "number"},
            "currency": {"type": "string", "default": "USD"},
            "memo": {"type": "string"},
            "beneficiary": {
                "type": "object",
                "description": "Beneficiary wiring instructions.",
            },
        },
        "required": ["origin_account_id", "amount", "beneficiary"],
    },
    "outputSchema": {
        "type": "object",
        "properties": {
            "status": {"type": "string"},
            "data": {
                "type": "object",
                "properties": {
                    "submission_status": {"type": "string"},
                    "payload": {"type": "object"},
                },
            },
            "timestamp": {"type": "string"},
        },
    },
}


def mercury_payment_sender(
    origin_account_id: str,
    amount: float,
    beneficiary: dict[str, Any],
    currency: str = "USD",
    memo: str | None = None,
    **_: Any,
) -> dict[str, Any]:
    """Build a pending Mercury payment payload."""
    try:
        if amount <= 0:
            raise ValueError("amount must be positive")
        if not beneficiary.get("name"):
            raise ValueError("beneficiary.name is required")

        if not os.getenv("MERCURY_API_TOKEN"):
            raise ValueError("MERCURY_API_TOKEN missing; see .env.template")

        payload = {
            "originAccountId": origin_account_id,
            "amount": round(amount, 2),
            "currency": currency,
            "memo": memo,
            "beneficiary": beneficiary,
            "execution": "pending_thunder_approval",
        }
        data = {
            "submission_status": "pending_thunder_approval",
            "payload": payload,
        }
        return {
            "status": "success",
            "data": data,
            "timestamp": datetime.now(timezone.utc).isoformat(),
        }
    except Exception as exc:
        _log_lesson("mercury_payment_sender", str(exc))
        return {
            "status": "error",
            "data": {"error": str(exc)},
            "timestamp": datetime.now(timezone.utc).isoformat(),
        }


def _log_lesson(skill_name: str, error: str) -> None:
    with open("logs/lessons.md", "a", encoding="utf-8") as handle:
        handle.write(f"- [{datetime.now(timezone.utc).isoformat()}] {skill_name}: {error}\n")
