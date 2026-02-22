"""Validate inbound webhooks from strategic partners."""
from __future__ import annotations

import hmac
import json
import os
from datetime import datetime, timezone
from hashlib import sha256
from typing import Any

TOOL_META: dict[str, Any] = {
    "name": "webhook_receiver",
    "description": "Verifies webhook signatures and normalizes payloads.",
    "inputSchema": {
        "type": "object",
        "properties": {
            "source": {
                "type": "string",
                "enum": ["mercury", "kraken", "github"],
            },
            "headers": {"type": "object"},
            "payload": {"type": "object"},
        },
        "required": ["source", "headers", "payload"],
    },
    "outputSchema": {
        "type": "object",
        "properties": {
            "status": {"type": "string"},
            "data": {
                "type": "object",
                "properties": {
                    "authorized": {"type": "boolean"},
                    "event": {"type": "object"},
                },
            },
            "timestamp": {"type": "string"},
        },
    },
}


def webhook_receiver(
    source: str,
    headers: dict[str, Any],
    payload: dict[str, Any],
    **_: Any,
) -> dict[str, Any]:
    """Validate webhook signature and return normalized event data."""

    try:
        normalized_source = source.lower()
        secret = _resolve_secret(normalized_source)
        signed_body = json.dumps(payload, separators=(",", ":"), sort_keys=True).encode("utf-8")
        authorized = _validate_signature(normalized_source, headers, signed_body, secret)
        event_type = _extract_event(normalized_source, headers)
        event = {
            "source": normalized_source,
            "event_type": event_type,
            "payload": payload,
        }
        status = "success" if authorized else "error"
        data = {"authorized": authorized, "event": event}
        return {
            "status": status,
            "data": data,
            "timestamp": datetime.now(timezone.utc).isoformat(),
        }
    except Exception as exc:
        _log_lesson("webhook_receiver", str(exc))
        return {
            "status": "error",
            "data": {"error": str(exc)},
            "timestamp": datetime.now(timezone.utc).isoformat(),
        }


def _resolve_secret(source: str) -> str:
    mapping = {
        "mercury": "MERCURY_WEBHOOK_SECRET",
        "kraken": "KRAKEN_WEBHOOK_SECRET",
        "github": "GITHUB_WEBHOOK_SECRET",
    }
    env_key = mapping[source]
    secret = os.getenv(env_key)
    if not secret:
        raise ValueError(f"{env_key} missing; see .env.template")
    return secret


def _validate_signature(
    source: str,
    headers: dict[str, Any],
    body: bytes,
    secret: str,
) -> bool:
    provided = ""
    if source == "mercury":
        provided = headers.get("X-Mercury-Signature", "")
    elif source == "kraken":
        provided = headers.get("X-Kraken-Signature", "")
    else:
        provided = headers.get("X-Hub-Signature-256", "").split("=")[-1]
    calculated = hmac.new(secret.encode("utf-8"), body, sha256).hexdigest()
    return hmac.compare_digest(calculated, str(provided))


def _extract_event(source: str, headers: dict[str, Any]) -> str:
    if source == "github":
        return headers.get("X-GitHub-Event", "unknown")
    if source == "mercury":
        return headers.get("X-Mercury-Event", "unknown")
    return headers.get("X-Kraken-Event", "unknown")


def _log_lesson(skill_name: str, error: str) -> None:
    """Append a Ralph Wiggum lesson entry."""

    with open("logs/lessons.md", "a", encoding="utf-8") as handle:
        handle.write(f"- [{datetime.now(timezone.utc).isoformat()}] {skill_name}: {error}\n")
