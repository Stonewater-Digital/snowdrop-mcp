"""Detect PII prior to external communication."""
from __future__ import annotations

import re
from datetime import datetime, timezone
from typing import Any

TOOL_META: dict[str, Any] = {
    "name": "pii_detector",
    "description": "Finds PII in free-form text and masks the findings.",
    "inputSchema": {
        "type": "object",
        "properties": {
            "text": {"type": "string"},
            "check_types": {
                "type": "array",
                "items": {"type": "string"},
                "default": ["email", "phone", "ssn", "address", "name", "credit_card"],
            },
        },
        "required": ["text"],
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

PATTERNS = {
    "email": re.compile(r"[A-Za-z0-9._%+-]+@[A-Za-z0-9.-]+\.[A-Za-z]{2,}"),
    "phone": re.compile(r"\+?1?-?\(?\d{3}\)?[-. ]?\d{3}[-. ]?\d{4}"),
    "ssn": re.compile(r"\b\d{3}-\d{2}-\d{4}\b"),
    "address": re.compile(r"\d+\s+[A-Za-z0-9 .]+(Street|St|Ave|Avenue|Blvd|Lane|Ln|Road|Rd)"),
    "name": re.compile(r"\b[A-Z][a-z]+\s+[A-Z][a-z]+\b"),
    "credit_card": re.compile(r"\b(?:\d[ -]*?){13,16}\b"),
}


def pii_detector(
    text: str,
    check_types: list[str] | None = None,
    **_: Any,
) -> dict[str, Any]:
    """Return detection list with masked values."""

    try:
        check_types = check_types or [
            "email",
            "phone",
            "ssn",
            "address",
            "name",
            "credit_card",
        ]
        detections: list[dict[str, Any]] = []
        for check_type in check_types:
            pattern = PATTERNS.get(check_type)
            if not pattern:
                continue
            for match in pattern.finditer(text):
                detections.append(
                    {
                        "type": check_type,
                        "value": _mask_value(match.group(0)),
                        "position": match.start(),
                    }
                )
        data = {"pii_found": bool(detections), "detections": detections}
        return {
            "status": "success",
            "data": data,
            "timestamp": datetime.now(timezone.utc).isoformat(),
        }
    except Exception as exc:
        _log_lesson("pii_detector", str(exc))
        return {
            "status": "error",
            "data": {"error": str(exc)},
            "timestamp": datetime.now(timezone.utc).isoformat(),
        }


def _mask_value(value: str) -> str:
    if len(value) <= 4:
        return "*" * len(value)
    return value[0] + "*" * (len(value) - 2) + value[-1]


def _log_lesson(skill_name: str, error: str) -> None:
    with open("logs/lessons.md", "a", encoding="utf-8") as handle:
        handle.write(f"- [{datetime.now(timezone.utc).isoformat()}] {skill_name}: {error}\n")
