"""Prepare docker secret injection templates using 1Password."""
from __future__ import annotations

import os
from datetime import datetime, timezone
from typing import Any

TOOL_META: dict[str, Any] = {
    "name": "docker_secret_injector",
    "description": "Builds op run templates for injecting secrets into containers.",
    "inputSchema": {
        "type": "object",
        "properties": {
            "secret_names": {
                "type": "array",
                "items": {"type": "string"},
            },
            "container_name": {"type": "string"},
        },
        "required": ["secret_names", "container_name"],
    },
    "outputSchema": {
        "type": "object",
        "properties": {
            "status": {"type": "string"},
            "data": {
                "type": "object",
                "properties": {
                    "command": {"type": "string"},
                    "env_mappings": {"type": "array", "items": {"type": "string"}},
                },
            },
            "timestamp": {"type": "string"},
        },
    },
}


def docker_secret_injector(
    secret_names: list[str],
    container_name: str,
    **_: Any,
) -> dict[str, Any]:
    """Return an op run template without executing it."""

    try:
        if not secret_names:
            raise ValueError("secret_names cannot be empty")
        if not container_name:
            raise ValueError("container_name is required")
        token = os.getenv("OP_SERVICE_ACCOUNT_TOKEN")
        if not token:
            raise ValueError("OP_SERVICE_ACCOUNT_TOKEN missing; see .env.template")

        env_flags = [f"--env '{name}=op://Snowdrop/{name}/value'" for name in secret_names]
        command = (
            "op run --account-token $OP_SERVICE_ACCOUNT_TOKEN "
            f"{' '.join(env_flags)} -- docker exec -it {container_name} /bin/sh"
        )
        return {
            "status": "success",
            "data": {"command": command, "env_mappings": env_flags},
            "timestamp": datetime.now(timezone.utc).isoformat(),
        }
    except Exception as exc:
        _log_lesson("docker_secret_injector", str(exc))
        return {
            "status": "error",
            "data": {"error": str(exc)},
            "timestamp": datetime.now(timezone.utc).isoformat(),
        }


def _log_lesson(skill_name: str, error: str) -> None:
    """Append a Ralph Wiggum lesson entry."""

    with open("logs/lessons.md", "a", encoding="utf-8") as handle:
        handle.write(f"- [{datetime.now(timezone.utc).isoformat()}] {skill_name}: {error}\n")
