"""Collect anonymous telemetry events."""
from __future__ import annotations

import json
import re
import uuid
from datetime import datetime, timezone
from pathlib import Path
from typing import Any

LOG_PATH = Path("logs/telemetry.jsonl")
EMAIL_REGEX = re.compile(r"[A-Za-z0-9._%+-]+@[A-Za-z0-9.-]+\.[A-Za-z]{2,}")
IP_REGEX = re.compile(r"\b(?:\d{1,3}\.){3}\d{1,3}\b")

TOOL_META: dict[str, Any] = {
    "name": "telemetry_collector",
    "description": "Appends anonymous usage telemetry after stripping PII.",
    "inputSchema": {
        "type": "object",
        "properties": {
            "event_type": {
                "type": "string",
                "enum": ["skill_call", "error", "auth", "registration", "upgrade"],
            },
            "properties": {"type": "object"},
        },
        "required": ["event_type", "properties"],
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


def telemetry_collector(event_type: str, properties: dict[str, Any], **_: Any) -> dict[str, Any]:
    """Store sanitized telemetry event."""
    try:
        sanitized = _strip_pii(properties)
        event_id = str(uuid.uuid4())
        payload = {
            "event_id": event_id,
            "event_type": event_type,
            "properties": sanitized,
            "timestamp": datetime.now(timezone.utc).isoformat(),
        }
        LOG_PATH.parent.mkdir(parents=True, exist_ok=True)
        with LOG_PATH.open("a", encoding="utf-8") as handle:
            handle.write(json.dumps(payload) + "\n")
        data = {"collected": True, "event_id": event_id, "pii_stripped": sanitized != properties}
        return {
            "status": "success",
            "data": data,
            "timestamp": payload["timestamp"],
        }
    except Exception as exc:  # noqa: BLE001
        _log_lesson("telemetry_collector", str(exc))
        return {
            "status": "error",
            "data": {"error": str(exc)},
            "timestamp": datetime.now(timezone.utc).isoformat(),
        }


def _strip_pii(props: dict[str, Any]) -> dict[str, Any]:
    sanitized: dict[str, Any] = {}
    for key, value in props.items():
        if isinstance(value, str):
            value = EMAIL_REGEX.sub("[redacted-email]", value)
            value = IP_REGEX.sub("[redacted-ip]", value)
        sanitized[key] = value
    return sanitized


def _log_lesson(skill_name: str, error: str) -> None:
    with open("logs/lessons.md", "a", encoding="utf-8") as handle:
        handle.write(f"- [{datetime.now(timezone.utc).isoformat()}] {skill_name}: {error}\n")
