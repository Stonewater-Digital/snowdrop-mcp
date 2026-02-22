"""Signature verification helper for agent communications."""
from __future__ import annotations

import hashlib
import hmac
from datetime import datetime, timezone
from typing import Any

TOOL_META: dict[str, Any] = {
    "name": "signature_verifier",
    "description": "Verifies HMAC-SHA256 signatures for incoming agent messages.",
    "inputSchema": {
        "type": "object",
        "properties": {
            "message": {"type": "string"},
            "signature": {"type": "string"},
            "agent_id": {"type": "string"},
            "known_public_keys": {
                "type": "object",
                "description": "Mapping of agent_id to shared secret.",
            },
        },
        "required": ["message", "signature", "agent_id", "known_public_keys"],
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


def signature_verifier(
    message: str,
    signature: str,
    agent_id: str,
    known_public_keys: dict[str, str],
    **_: Any,
) -> dict[str, Any]:
    """Validate an incoming signature using shared secrets."""
    try:
        if not isinstance(known_public_keys, dict):
            raise ValueError("known_public_keys must be a dict mapping agent_id to key")
        shared_secret = known_public_keys.get(agent_id)
        if shared_secret is None:
            raise ValueError(f"No shared key registered for agent {agent_id}")

        expected = hmac.new(
            shared_secret.encode("utf-8"),
            message.encode("utf-8"),
            hashlib.sha256,
        ).hexdigest()
        valid = hmac.compare_digest(expected, signature)
        verified_at = datetime.now(timezone.utc).isoformat()
        return {
            "status": "success",
            "data": {"valid": valid, "agent_id": agent_id, "verified_at": verified_at},
            "timestamp": verified_at,
        }
    except Exception as exc:  # noqa: BLE001
        _log_lesson("signature_verifier", str(exc))
        return {
            "status": "error",
            "data": {"error": str(exc)},
            "timestamp": datetime.now(timezone.utc).isoformat(),
        }


def _log_lesson(skill_name: str, error: str) -> None:
    with open("logs/lessons.md", "a", encoding="utf-8") as handle:
        handle.write(f"- [{datetime.now(timezone.utc).isoformat()}] {skill_name}: {error}\n")
