"""HMAC-based message signing for Snowdrop agents."""
from __future__ import annotations

import hashlib
import hmac
import os
from datetime import datetime, timezone
from typing import Any

TOOL_META: dict[str, Any] = {
    "name": "message_signer",
    "description": "Signs messages with an env-provided key for agent authentication.",
    "inputSchema": {
        "type": "object",
        "properties": {
            "message": {"type": "string"},
            "signing_key_env": {
                "type": "string",
                "default": "SNOWDROP_SIGNING_KEY",
                "description": "Environment variable holding the signing key.",
            },
        },
        "required": ["message"],
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


def message_signer(
    message: str,
    signing_key_env: str = "SNOWDROP_SIGNING_KEY",
    **_: Any,
) -> dict[str, Any]:
    """Sign a message using HMAC-SHA256."""
    try:
        signing_key = os.getenv(signing_key_env)
        if signing_key is None:
            raise ValueError(f"{signing_key_env} missing; see .env.template")

        message_bytes = message.encode("utf-8")
        key_bytes = signing_key.encode("utf-8")
        signature = hmac.new(key_bytes, message_bytes, hashlib.sha256).hexdigest()
        issued_at = datetime.now(timezone.utc).isoformat()
        payload = {
            "message_hash": hashlib.sha256(message_bytes).hexdigest(),
            "signature": signature,
            "algorithm": "hmac-sha256",
            "timestamp": issued_at,
        }
        return {
            "status": "success",
            "data": payload,
            "timestamp": issued_at,
        }
    except Exception as exc:  # noqa: BLE001
        _log_lesson("message_signer", str(exc))
        return {
            "status": "error",
            "data": {"error": str(exc)},
            "timestamp": datetime.now(timezone.utc).isoformat(),
        }


def _log_lesson(skill_name: str, error: str) -> None:
    with open("logs/lessons.md", "a", encoding="utf-8") as handle:
        handle.write(f"- [{datetime.now(timezone.utc).isoformat()}] {skill_name}: {error}\n")
