"""Deterministic key derivation helper."""
from __future__ import annotations

import hashlib
import os
from datetime import datetime, timezone
from typing import Any

TOOL_META: dict[str, Any] = {
    "name": "key_derivation_helper",
    "description": "Derives deterministic key identifiers from the master seed.",
    "inputSchema": {
        "type": "object",
        "properties": {
            "purpose": {
                "type": "string",
                "enum": ["signing", "encryption", "api_auth"],
            },
            "context": {
                "type": "string",
                "description": "Context string such as agent_id or service name.",
            },
        },
        "required": ["purpose", "context"],
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


def key_derivation_helper(
    purpose: str,
    context: str,
    **_: Any,
) -> dict[str, Any]:
    """Derive a deterministic key identifier without exposing secrets."""
    try:
        master_seed = os.getenv("SNOWDROP_MASTER_SEED")
        if master_seed is None:
            raise ValueError("SNOWDROP_MASTER_SEED missing; see .env.template")
        if not purpose:
            raise ValueError("purpose is required")
        if not context:
            raise ValueError("context is required")

        info = f"{purpose}:{context}".encode("utf-8")
        digest = hashlib.sha256(master_seed.encode("utf-8") + info).hexdigest()
        key_id = f"{purpose}_{digest[:16]}"
        data = {
            "derived_key_id": key_id,
            "purpose": purpose,
            "context": context,
        }
        return {
            "status": "success",
            "data": data,
            "timestamp": datetime.now(timezone.utc).isoformat(),
        }
    except Exception as exc:  # noqa: BLE001
        _log_lesson("key_derivation_helper", str(exc))
        return {
            "status": "error",
            "data": {"error": str(exc)},
            "timestamp": datetime.now(timezone.utc).isoformat(),
        }


def _log_lesson(skill_name: str, error: str) -> None:
    with open("logs/lessons.md", "a", encoding="utf-8") as handle:
        handle.write(f"- [{datetime.now(timezone.utc).isoformat()}] {skill_name}: {error}\n")
