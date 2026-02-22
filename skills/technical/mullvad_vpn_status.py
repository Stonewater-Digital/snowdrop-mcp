"""Check Mullvad VPN account status and kill switch state."""
from __future__ import annotations

import os
from datetime import datetime, timezone
from typing import Any

TOOL_META: dict[str, Any] = {
    "name": "mullvad_vpn_status",
    "description": "Constructs Mullvad account queries and summarizes connection health.",
    "inputSchema": {
        "type": "object",
        "properties": {
            "api_response": {"type": "object", "description": "Optional Mullvad response."},
        },
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


def mullvad_vpn_status(api_response: dict[str, Any] | None = None, **_: Any) -> dict[str, Any]:
    """Return a prepared Mullvad status request and parsed state when available.

    Args:
        api_response: Optional Mullvad API response body to parse.

    Returns:
        Envelope containing the prepared request and parsed connection metadata.
    """

    try:
        account_number = os.getenv("MULLVAD_ACCOUNT_NUMBER")
        if not account_number:
            raise ValueError("MULLVAD_ACCOUNT_NUMBER missing; see .env.template")

        prepared_request = {
            "url": f"https://api.mullvad.net/www/accounts/{account_number}",
        }

        status = _parse_response(api_response) if api_response else None

        data = {
            "prepared_request": prepared_request,
            "status": status,
            "submission_status": "pending_thunder_approval" if not api_response else "parsed",
        }

        return {
            "status": "success",
            "data": data,
            "timestamp": datetime.now(timezone.utc).isoformat(),
        }
    except Exception as exc:
        _log_lesson("mullvad_vpn_status", str(exc))
        return {
            "status": "error",
            "data": {"error": str(exc)},
            "timestamp": datetime.now(timezone.utc).isoformat(),
        }


def _parse_response(api_response: dict[str, Any] | None) -> dict[str, Any] | None:
    if not api_response:
        return None
    try:
        return {
            "connection_status": api_response.get("connection_status"),
            "exit_node": api_response.get("exit_ip"),
            "kill_switch": api_response.get("multihop") == "enabled",
        }
    except AttributeError:
        return None


def _log_lesson(skill_name: str, error: str) -> None:
    with open("logs/lessons.md", "a", encoding="utf-8") as handle:
        handle.write(f"- [{datetime.now(timezone.utc).isoformat()}] {skill_name}: {error}\n")
