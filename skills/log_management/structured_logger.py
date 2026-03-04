"""Write structured JSON logs for Snowdrop operations."""
from __future__ import annotations

import json
import uuid
from datetime import datetime, timezone
from pathlib import Path
from typing import Any

TOOL_META: dict[str, Any] = {
    "name": "structured_logger",
    "description": "Appends structured log entries with correlation metadata to a JSONL file.",
    "inputSchema": {
        "type": "object",
        "properties": {
            "level": {
                "type": "string",
                "enum": ["debug", "info", "warn", "error", "fatal"],
            },
            "message": {"type": "string"},
            "context": {"type": "object"},
            "log_file": {"type": "string", "default": "logs/structured.jsonl"},
        },
        "required": ["level", "message"],
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


def structured_logger(
    level: str,
    message: str,
    context: dict[str, Any] | None = None,
    log_file: str = "logs/structured.jsonl",
    **_: Any,
) -> dict[str, Any]:
    """Persist a structured log entry."""
    try:
        level = level.lower()
        if level not in {"debug", "info", "warn", "error", "fatal"}:
            raise ValueError("Unsupported level")
        entry_id = str(uuid.uuid4())
        timestamp = datetime.now(timezone.utc).isoformat()
        payload = {
            "timestamp": timestamp,
            "level": level,
            "message": message,
            "context": context or {},
            "entry_id": entry_id,
            "correlation_id": (context or {}).get("request_id", entry_id),
        }
        path = Path(log_file)
        path.parent.mkdir(parents=True, exist_ok=True)
        with path.open("a", encoding="utf-8") as handle:
            handle.write(json.dumps(payload) + "\n")
        data = {"logged": True, "entry_id": entry_id, "log_file": str(path)}
        return {
            "status": "success",
            "data": data,
            "timestamp": timestamp,
        }
    except Exception as exc:  # noqa: BLE001
        _log_lesson("structured_logger", str(exc))
        return {
            "status": "error",
            "data": {"error": str(exc)},
            "timestamp": datetime.now(timezone.utc).isoformat(),
        }


def _log_lesson(skill_name: str, error: str) -> None:
    with open("logs/lessons.md", "a", encoding="utf-8") as handle:
        handle.write(f"- [{datetime.now(timezone.utc).isoformat()}] {skill_name}: {error}\n")
