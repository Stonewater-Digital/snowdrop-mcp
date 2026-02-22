"""Monitor Fly.io MCP gateway deployments."""
from __future__ import annotations

import os
from datetime import datetime, timezone
from typing import Any

TOOL_META: dict[str, Any] = {
    "name": "flyio_deploy_status",
    "description": "Builds Fly.io API requests and summarizes allocation health.",
    "inputSchema": {
        "type": "object",
        "properties": {
            "app_name": {"type": "string"},
            "api_response": {
                "type": "object",
                "description": "Optional machines API response to parse.",
            },
        },
        "required": ["app_name"],
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


def flyio_deploy_status(
    app_name: str,
    api_response: dict[str, Any] | None = None,
    **_: Any,
) -> dict[str, Any]:
    """Return prepared request plus allocation health.

    Args:
        app_name: Fly.io application slug.
        api_response: Optional Machines API response for immediate parsing.

    Returns:
        Envelope detailing the prepared request and parsed allocation status.
    """

    try:
        token = os.getenv("FLY_API_TOKEN")
        if not token:
            raise ValueError("FLY_API_TOKEN missing; see .env.template")

        prepared_request = {
            "url": f"https://api.machines.dev/v1/apps/{app_name}",
            "headers": {"Authorization": "Bearer ***redacted***"},
        }

        allocation = _parse_response(api_response) if api_response else None

        data = {
            "prepared_request": prepared_request,
            "allocation": allocation,
            "submission_status": "pending_thunder_approval" if not api_response else "parsed",
        }

        return {
            "status": "success",
            "data": data,
            "timestamp": datetime.now(timezone.utc).isoformat(),
        }
    except Exception as exc:
        _log_lesson("flyio_deploy_status", str(exc))
        return {
            "status": "error",
            "data": {"error": str(exc)},
            "timestamp": datetime.now(timezone.utc).isoformat(),
        }


def _parse_response(api_response: dict[str, Any] | None) -> dict[str, Any] | None:
    if not api_response:
        return None
    try:
        machines = api_response.get("machines", [])
        if not machines:
            return None
        primary = machines[0]
        return {
            "state": primary.get("state"),
            "region": primary.get("region"),
            "uptime_seconds": primary.get("created_at"),
        }
    except AttributeError:
        return None


def _log_lesson(skill_name: str, error: str) -> None:
    with open("logs/lessons.md", "a", encoding="utf-8") as handle:
        handle.write(f"- [{datetime.now(timezone.utc).isoformat()}] {skill_name}: {error}\n")
