"""Extract structured entities from Thunder's text."""
from __future__ import annotations

import re
from datetime import datetime, timezone
from typing import Any

TOOL_META: dict[str, Any] = {
    "name": "entity_extractor",
    "description": "Uses regex heuristics to extract Snowdrop-relevant entities.",
    "inputSchema": {
        "type": "object",
        "properties": {
            "text": {"type": "string"},
            "entity_types": {
                "type": "array",
                "items": {"type": "string"},
                "default": [
                    "amount",
                    "currency",
                    "date",
                    "asset",
                    "agent_id",
                    "account",
                ],
            },
        },
        "required": ["text"],
    },
    "outputSchema": {
        "type": "object",
        "properties": {
            "status": {"type": "string"},
            "data": {
                "type": "object",
                "properties": {
                    "entities": {"type": "array", "items": {"type": "object"}},
                },
            },
            "timestamp": {"type": "string"},
        },
    },
}

PATTERNS: dict[str, re.Pattern[str]] = {
    "amount": re.compile(r"(?P<raw>\$?\d{1,3}(?:,\d{3})*(?:\.\d+)?|\$?\d+(?:\.\d+)?)"),
    "currency": re.compile(r"\b(USD|USDC|EUR|BTC|ETH|TON|SOL)\b", re.IGNORECASE),
    "date": re.compile(r"\b\d{4}-\d{2}-\d{2}\b"),
    "asset": re.compile(r"\b[A-Z]{2,5}\b"),
    "agent_id": re.compile(r"\bAGENT-[A-Z0-9]{4,}\b"),
    "account": re.compile(r"\bACC-[0-9A-Z]{6,}\b"),
}


def entity_extractor(
    text: str,
    entity_types: list[str] | None = None,
    **_: Any,
) -> dict[str, Any]:
    """Extract requested entity categories with location metadata."""

    try:
        if not text:
            raise ValueError("text cannot be empty")
        entity_types = entity_types or [
            "amount",
            "currency",
            "date",
            "asset",
            "agent_id",
            "account",
        ]
        results: list[dict[str, Any]] = []
        for entity_type in entity_types:
            pattern = PATTERNS.get(entity_type)
            if not pattern:
                continue
            for match in pattern.finditer(text):
                raw = match.group(0)
                value = raw.replace("$", "").replace(",", "")
                results.append(
                    {
                        "type": entity_type,
                        "value": value,
                        "raw_text": raw,
                        "position": match.start(),
                    }
                )

        return {
            "status": "success",
            "data": {"entities": results},
            "timestamp": datetime.now(timezone.utc).isoformat(),
        }
    except Exception as exc:
        _log_lesson("entity_extractor", str(exc))
        return {
            "status": "error",
            "data": {"error": str(exc)},
            "timestamp": datetime.now(timezone.utc).isoformat(),
        }


def _log_lesson(skill_name: str, error: str) -> None:
    with open("logs/lessons.md", "a", encoding="utf-8") as handle:
        handle.write(f"- [{datetime.now(timezone.utc).isoformat()}] {skill_name}: {error}\n")
