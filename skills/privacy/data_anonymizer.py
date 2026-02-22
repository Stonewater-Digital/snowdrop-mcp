"""Anonymize Snowdrop data prior to sharing externally."""
from __future__ import annotations

import hashlib
from datetime import datetime, timezone
from typing import Any

TOOL_META: dict[str, Any] = {
    "name": "data_anonymizer",
    "description": "Transforms sensitive fields using hash/mask/redact/generalize strategies.",
    "inputSchema": {
        "type": "object",
        "properties": {
            "data": {
                "type": "array",
                "items": {"type": "object"},
            },
            "fields_to_anonymize": {
                "type": "array",
                "items": {"type": "string"},
            },
            "method": {
                "type": "string",
                "enum": ["hash", "mask", "redact", "generalize"],
            },
        },
        "required": ["data", "fields_to_anonymize", "method"],
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


def data_anonymizer(
    data: list[dict[str, Any]],
    fields_to_anonymize: list[str],
    method: str,
    **_: Any,
) -> dict[str, Any]:
    """Return anonymized dataset and audit log."""

    try:
        log: list[dict[str, Any]] = []
        sanitized: list[dict[str, Any]] = []
        for record in data:
            updated = dict(record)
            for field in fields_to_anonymize:
                if field not in updated:
                    continue
                original = updated[field]
                updated[field] = _transform_value(original, method)
                log.append({"field": field, "method": method})
            sanitized.append(updated)
        payload = {"anonymized_data": sanitized, "transformation_log": log}
        return {
            "status": "success",
            "data": payload,
            "timestamp": datetime.now(timezone.utc).isoformat(),
        }
    except Exception as exc:
        _log_lesson("data_anonymizer", str(exc))
        return {
            "status": "error",
            "data": {"error": str(exc)},
            "timestamp": datetime.now(timezone.utc).isoformat(),
        }


def _transform_value(value: Any, method: str) -> Any:
    if method == "hash":
        digest = hashlib.sha256(str(value).encode("utf-8")).hexdigest()
        return digest[:16]
    if method == "mask":
        text = str(value)
        if len(text) <= 2:
            return "*" * len(text)
        return text[0] + "*" * (len(text) - 2) + text[-1]
    if method == "redact":
        return "[REDACTED]"
    if method == "generalize":
        if isinstance(value, (int, float)):
            return round(value, -1) if value else 0
        text = str(value)
        return text[:3] + "..." if len(text) > 3 else text
    raise ValueError(f"Unsupported method {method}")


def _log_lesson(skill_name: str, error: str) -> None:
    with open("logs/lessons.md", "a", encoding="utf-8") as handle:
        handle.write(f"- [{datetime.now(timezone.utc).isoformat()}] {skill_name}: {error}\n")
