"""Detect PII prior to external communication."""
from __future__ import annotations

import re
from typing import Any

from skills.utils import SkillTelemetryEmitter, get_iso_timestamp, log_lesson

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

    check_types = check_types or [
        "email",
        "phone",
        "ssn",
        "address",
        "name",
        "credit_card",
    ]
    emitter = SkillTelemetryEmitter(
        "pii_detector",
        {
            "text_length": len(text or ""),
            "requested_checks": len(check_types),
        },
    )
    try:
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
        emitter.record(
            "ok",
            {
                "detection_count": len(detections),
                "pii_found": bool(detections),
                "checks_evaluated": len(check_types),
            },
        )
        return {
            "status": "success",
            "data": data,
            "timestamp": get_iso_timestamp(),
        }
    except Exception as exc:
        log_lesson(f"pii_detector: {exc}")
        emitter.record("error", {"error": str(exc)})
        return {
            "status": "error",
            "data": {"error": str(exc)},
            "timestamp": get_iso_timestamp(),
        }


def _mask_value(value: str) -> str:
    if len(value) <= 4:
        return "*" * len(value)
    return value[0] + "*" * (len(value) - 2) + value[-1]
