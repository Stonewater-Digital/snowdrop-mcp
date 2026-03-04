"""Build JSON-RPC 2.0 compliant responses for A2A workflows."""
from __future__ import annotations

from datetime import datetime, timezone
from typing import Any

TOOL_META: dict[str, Any] = {
    "name": "a2a_response_builder",
    "description": "Constructs JSON-RPC envelopes for outbound A2A traffic.",
    "inputSchema": {
        "type": "object",
        "properties": {
            "request_id": {"type": ["string", "number"], "description": "Echoed JSON-RPC id."},
            "result": {"type": "object", "description": "Success payload to return."},
            "error_code": {"type": "number", "description": "JSON-RPC error code."},
            "error_message": {"type": "string", "description": "JSON-RPC error message."},
        },
        "required": ["request_id"],
    },
    "outputSchema": {
        "type": "object",
        "properties": {
            "status": {"type": "string"},
            "data": {"type": "object"},
            "timestamp": {"type": "string", "format": "date-time"},
        },
    },
}


def a2a_response_builder(
    request_id: Any,
    result: Any | None = None,
    error_code: int | None = None,
    error_message: str | None = None,
    **_: Any,
) -> dict[str, Any]:
    """Return a JSON-RPC 2.0 response envelope.

    Args:
        request_id: ID to echo in the JSON-RPC response.
        result: Data payload to return on success.
        error_code: JSON-RPC error code when responding with an error.
        error_message: JSON-RPC error description when responding with an error.

    Returns:
        Standardized skill response containing the JSON-RPC response body.
    """

    try:
        response: dict[str, Any] = {"jsonrpc": "2.0", "id": request_id}

        if error_code is not None:
            if error_message is None:
                raise ValueError("error_message is required when error_code is provided")
            response["error"] = {"code": error_code, "message": error_message}
            status = "error"
        else:
            response["result"] = result if result is not None else {}
            status = "success"

        return {
            "status": status,
            "data": response,
            "timestamp": datetime.now(timezone.utc).isoformat(),
        }
    except Exception as exc:
        _log_lesson("a2a_response_builder", str(exc))
        return {
            "status": "error",
            "data": {"error": str(exc)},
            "timestamp": datetime.now(timezone.utc).isoformat(),
        }


def _log_lesson(skill_name: str, error: str) -> None:
    with open("logs/lessons.md", "a", encoding="utf-8") as handle:
        handle.write(f"- [{datetime.now(timezone.utc).isoformat()}] {skill_name}: {error}\n")
