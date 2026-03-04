"""Prepare Coinbase AgentKit verification payloads."""
from __future__ import annotations

import os
from datetime import datetime, timezone
from typing import Any

TOOL_META: dict[str, Any] = {
    "name": "coinbase_agentkit_verifier",
    "description": "Drafts the JSON payload needed to verify Snowdrop in Coinbase AgentKit.",
    "inputSchema": {
        "type": "object",
        "properties": {
            "agent_name": {"type": "string"},
            "capabilities": {
                "type": "array",
                "items": {"type": "string"},
            },
        },
        "required": ["agent_name", "capabilities"],
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


def coinbase_agentkit_verifier(
    agent_name: str,
    capabilities: list[str],
    **_: Any,
) -> dict[str, Any]:
    """Return a pending Coinbase AgentKit verification request.

    Args:
        agent_name: Name of the agent being certified.
        capabilities: Capabilities that should be associated with the agent.

    Returns:
        Envelope containing the prepared payload awaiting Thunder approval.
    """

    try:
        api_key_name = os.getenv("COINBASE_API_KEY_NAME")
        if not api_key_name:
            raise ValueError("COINBASE_API_KEY_NAME missing; see .env.template")

        payload = {
            "agent": agent_name,
            "capabilities": capabilities,
            "apiKeyName": api_key_name,
            "timestamp": datetime.now(timezone.utc).isoformat(),
        }

        data = {
            "submission_status": "pending_thunder_approval",
            "payload": payload,
        }

        return {
            "status": "success",
            "data": data,
            "timestamp": payload["timestamp"],
        }
    except Exception as exc:
        _log_lesson("coinbase_agentkit_verifier", str(exc))
        return {
            "status": "error",
            "data": {"error": str(exc)},
            "timestamp": datetime.now(timezone.utc).isoformat(),
        }


def _log_lesson(skill_name: str, error: str) -> None:
    with open("logs/lessons.md", "a", encoding="utf-8") as handle:
        handle.write(f"- [{datetime.now(timezone.utc).isoformat()}] {skill_name}: {error}\n")
