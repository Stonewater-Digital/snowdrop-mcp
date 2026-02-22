"""Extract actionable follow-ups from meeting text."""
from __future__ import annotations

import re
from datetime import datetime, timezone
from typing import Any

TOOL_META: dict[str, Any] = {
    "name": "action_item_extractor",
    "description": "Uses heuristics to identify action items, assignees, and priority from text.",
    "inputSchema": {
        "type": "object",
        "properties": {
            "text": {"type": "string"},
            "participants": {"type": "array", "items": {"type": "string"}},
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


_KEYWORDS = [
    r"need to",
    r"should",
    r"will",
    r"must",
    r"TODO",
    r"action item",
    r"follow up",
]
_PRIORITY_WORDS = {
    "urgent": "high",
    "asap": "high",
    "priority": "high",
    "later": "low",
}


def action_item_extractor(
    text: str,
    participants: list[str] | None = None,
    **_: Any,
) -> dict[str, Any]:
    """Parse text for action items."""
    try:
        participants = [p.lower() for p in (participants or [])]
        sentences = re.split(r"(?<=[.!?])\s+", text)
        action_items = []
        pattern = re.compile("|".join(_KEYWORDS), re.IGNORECASE)
        for sentence in sentences:
            if pattern.search(sentence):
                assignee = _find_assignee(sentence, participants)
                priority = _priority(sentence)
                action_items.append(
                    {
                        "description": sentence.strip(),
                        "assignee": assignee,
                        "priority": priority,
                        "source_quote": sentence.strip(),
                    }
                )
        data = {"action_items": action_items}
        return {
            "status": "success",
            "data": data,
            "timestamp": datetime.now(timezone.utc).isoformat(),
        }
    except Exception as exc:  # noqa: BLE001
        _log_lesson("action_item_extractor", str(exc))
        return {
            "status": "error",
            "data": {"error": str(exc)},
            "timestamp": datetime.now(timezone.utc).isoformat(),
        }


def _find_assignee(sentence: str, participants: list[str]) -> str | None:
    tokens = re.findall(r"[A-Za-z']+", sentence.lower())
    for participant in participants:
        if participant.lower() in tokens:
            return participant
    return None


def _priority(sentence: str) -> str:
    lower = sentence.lower()
    for word, level in _PRIORITY_WORDS.items():
        if word in lower:
            return level
    return "medium"


def _log_lesson(skill_name: str, error: str) -> None:
    with open("logs/lessons.md", "a", encoding="utf-8") as handle:
        handle.write(f"- [{datetime.now(timezone.utc).isoformat()}] {skill_name}: {error}\n")
