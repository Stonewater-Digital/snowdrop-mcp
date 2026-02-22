"""Route payment verification requests to appropriate gateways."""
from __future__ import annotations

import uuid
from datetime import datetime, timezone
from typing import Any

TOOL_META: dict[str, Any] = {
    "name": "payment_gateway_router",
    "description": "Determines which verification skill should process a payment receipt.",
    "inputSchema": {
        "type": "object",
        "properties": {
            "currency": {
                "type": "string",
                "enum": ["TON", "USDC", "USD_MERCURY"],
            },
            "transaction_ref": {"type": "string"},
            "expected_amount": {"type": "number"},
            "payer_agent_id": {"type": "string"},
        },
        "required": ["currency", "transaction_ref", "expected_amount", "payer_agent_id"],
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

_ROUTING_TABLE = {
    "TON": "ton_payment_verifier",
    "USDC": "usdc_payment_verifier",
    "USD_MERCURY": "mercury_payment_sender",
}


def payment_gateway_router(
    currency: str,
    transaction_ref: str,
    expected_amount: float,
    payer_agent_id: str,
    **_: Any,
) -> dict[str, Any]:
    """Provide downstream verification instructions without executing transfers."""
    try:
        currency = currency.upper()
        if currency not in _ROUTING_TABLE:
            raise ValueError("Unsupported currency")
        receipt_id = str(uuid.uuid4())
        verification_request = {
            "transaction_ref": transaction_ref,
            "expected_amount": expected_amount,
            "payer_agent_id": payer_agent_id,
        }
        routed_to = _ROUTING_TABLE[currency]
        if currency == "USD_MERCURY":
            verification_request["execution"] = "pending_thunder_approval"
        data = {
            "routed_to": routed_to,
            "verification_request": verification_request,
            "status": "pending_verification",
            "receipt_id": receipt_id,
        }
        return {
            "status": "success",
            "data": data,
            "timestamp": datetime.now(timezone.utc).isoformat(),
        }
    except Exception as exc:  # noqa: BLE001
        _log_lesson("payment_gateway_router", str(exc))
        return {
            "status": "error",
            "data": {"error": str(exc)},
            "timestamp": datetime.now(timezone.utc).isoformat(),
        }


def _log_lesson(skill_name: str, error: str) -> None:
    with open("logs/lessons.md", "a", encoding="utf-8") as handle:
        handle.write(f"- [{datetime.now(timezone.utc).isoformat()}] {skill_name}: {error}\n")
