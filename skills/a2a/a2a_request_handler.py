"""Validate inbound Google A2A JSON-RPC 2.0 requests."""
from __future__ import annotations

import os
from datetime import datetime, timezone
from typing import Any

TOOL_META: dict[str, Any] = {
    "name": "a2a_request_handler",
    "description": "Performs JSON-RPC compliance checks and bearer-token auth for A2A requests.",
    "inputSchema": {
        "type": "object",
        "properties": {
            "payload": {
                "type": "object",
                "description": "Raw JSON-RPC 2.0 request object from the counterparty.",
            },
            "authorization": {
                "type": "string",
                "description": "HTTP Authorization header value (Bearer token).",
            },
        },
        "required": ["payload", "authorization"],
    },
    "outputSchema": {
        "type": "object",
        "properties": {
            "status": {"type": "string", "enum": ["success", "error"]},
            "data": {"type": "object"},
            "timestamp": {"type": "string", "format": "date-time"},
        },
    },
}


def a2a_request_handler(payload: dict[str, Any], authorization: str, **_: Any) -> dict[str, Any]:
    """Validate JSON-RPC and bearer auth before dispatching downstream.

    Args:
        payload: JSON-RPC 2.0 request body from Google A2A.
        authorization: HTTP Authorization header string with the bearer token.

    Returns:
        Envelope containing the validated request metadata or a structured error.
    """

    try:
        expected_token = os.getenv("A2A_BEARER_TOKEN")
        if not expected_token:
            raise ValueError("A2A_BEARER_TOKEN missing; see .env.template")

        token = _extract_token(authorization)
        if token != expected_token:
            raise PermissionError("Invalid bearer token for A2A ingress")

        if payload.get("jsonrpc") != "2.0":
            raise ValueError("jsonrpc version must be '2.0'")

        method = payload.get("method")
        if not isinstance(method, str) or not method:
            raise ValueError("method must be a non-empty string")

        request_id = payload.get("id")
        if request_id is None:
            raise ValueError("id is required for correlation")

        params = payload.get("params", {})
        if params is None:
            params = {}

        return {
            "status": "success",
            "data": {
                "id": request_id,
                "method": method,
                "params": params,
                "jsonrpc": "2.0",
            },
            "timestamp": datetime.now(timezone.utc).isoformat(),
        }
    except Exception as exc:
        _log_lesson("a2a_request_handler", str(exc))
        return {
            "status": "error",
            "data": {
                "error": {
                    "code": -32000,
                    "message": str(exc),
                }
            },
            "timestamp": datetime.now(timezone.utc).isoformat(),
        }


def _extract_token(header: str) -> str:
    if not header:
        raise PermissionError("Authorization header missing")
    scheme, _, token = header.partition(" ")
    if scheme.lower() != "bearer" or not token:
        raise PermissionError("Authorization header must be 'Bearer <token>'")
    return token.strip()


def _log_lesson(skill_name: str, error: str) -> None:
    with open("logs/lessons.md", "a", encoding="utf-8") as handle:
        handle.write(f"- [{datetime.now(timezone.utc).isoformat()}] {skill_name}: {error}\n")
