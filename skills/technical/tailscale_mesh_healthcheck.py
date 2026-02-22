"""Check the status of the Tailscale mesh network."""
from __future__ import annotations

import os
from datetime import datetime, timezone
from typing import Any

import requests

TOOL_META: dict[str, Any] = {
    "name": "tailscale_mesh_healthcheck",
    "description": "Pulls device metadata from Tailscale and surfaces online/offline state.",
    "inputSchema": {
        "type": "object",
        "properties": {
            "tailnet": {
                "type": "string",
                "description": "Tailnet slug (e.g., example.gmail.com).",
            },
            "devices": {
                "type": "array",
                "items": {"type": "object"},
                "description": "Optional pre-fetched device list.",
            },
        },
        "required": [],
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


def tailscale_mesh_healthcheck(
    tailnet: str | None = None, devices: list[dict[str, Any]] | None = None, **_: Any
) -> dict[str, Any]:
    """Return node status for the Snowdrop mesh.

    Args:
        tailnet: Tailnet slug to query via the Tailscale API.
        devices: Optional pre-fetched device payload to parse instead of querying.

    Returns:
        Envelope enumerating node names with online/offline states and timestamps.
    """

    try:
        auth_key = os.getenv("TAILSCALE_AUTH_KEY")
        if not auth_key:
            raise ValueError("TAILSCALE_AUTH_KEY missing; see .env.template")

        if devices is None:
            if not tailnet:
                raise ValueError("Provide either devices or a tailnet to query")
            devices = _fetch_devices(tailnet, auth_key)

        nodes = [
            {
                "name": device.get("name"),
                "online": bool(device.get("online")),
                "last_seen": device.get("lastSeen") or device.get("last_seen"),
            }
            for device in devices
        ]

        return {
            "status": "success",
            "data": {"nodes": nodes},
            "timestamp": datetime.now(timezone.utc).isoformat(),
        }
    except Exception as exc:
        _log_lesson("tailscale_mesh_healthcheck", str(exc))
        return {
            "status": "error",
            "data": {"error": str(exc)},
            "timestamp": datetime.now(timezone.utc).isoformat(),
        }


def _fetch_devices(tailnet: str, auth_key: str) -> list[dict[str, Any]]:
    url = f"https://api.tailscale.com/api/v2/tailnet/{tailnet}/devices"
    response = requests.get(url, auth=(auth_key, ""), timeout=10)
    response.raise_for_status()
    payload = response.json()
    return payload.get("devices", payload)


def _log_lesson(skill_name: str, error: str) -> None:
    with open("logs/lessons.md", "a", encoding="utf-8") as handle:
        handle.write(f"- [{datetime.now(timezone.utc).isoformat()}] {skill_name}: {error}\n")
