"""Summarize Snowdrop conversations with decision traces."""
from __future__ import annotations

from datetime import datetime, timezone
from typing import Any

TOOL_META: dict[str, Any] = {
    "name": "conversation_summarizer",
    "description": "Compress multi-turn logs into actionable decisions and questions.",
    "inputSchema": {
        "type": "object",
        "properties": {
            "messages": {
                "type": "array",
                "items": {"type": "object"},
                "description": "Chat messages containing role, content, timestamp.",
            },
            "max_output_tokens": {
                "type": "integer",
                "default": 2000,
                "description": "Maximum tokens to allocate for summary payload.",
            },
        },
        "required": ["messages"],
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

_KEYWORDS = {
    "decision": ["decide", "approved", "confirmed"],
    "action": ["todo", "ship", "follow up", "action"],
    "question": ["?", "pending", "unclear"],
}


def conversation_summarizer(
    messages: list[dict[str, Any]],
    max_output_tokens: int = 2000,
    **_: Any,
) -> dict[str, Any]:
    """Summarize chat logs while keeping decision memory."""
    try:
        if not messages:
            raise ValueError("messages cannot be empty")
        if max_output_tokens <= 0:
            raise ValueError("max_output_tokens must be positive")

        decisions: list[str] = []
        action_items: list[str] = []
        open_questions: list[str] = []
        key_facts: list[str] = []
        total_chars = 0

        for entry in messages:
            content = str(entry.get("content", "")).strip()
            if not content:
                continue
            total_chars += len(content)
            normalized = content.lower()
            note = f"[{entry.get('role', 'unknown')}] {content}"[:400]
            if any(token in normalized for token in _KEYWORDS["decision"]):
                decisions.append(note)
            if any(token in normalized for token in _KEYWORDS["action"]):
                action_items.append(note)
            if any(token in normalized for token in _KEYWORDS["question"]):
                open_questions.append(note)
            if "key fact" in normalized or len(key_facts) < 5:
                key_facts.append(note)

        token_estimate = min(max_output_tokens, max(1, round(total_chars / 4)))
        summary = {
            "decisions_made": decisions[:10],
            "action_items": action_items[:10],
            "open_questions": open_questions[:10],
            "key_facts": key_facts[:10],
            "token_estimate": token_estimate,
        }
        return {
            "status": "success",
            "data": summary,
            "timestamp": datetime.now(timezone.utc).isoformat(),
        }
    except Exception as exc:
        _log_lesson("conversation_summarizer", str(exc))
        return {
            "status": "error",
            "data": {"error": str(exc)},
            "timestamp": datetime.now(timezone.utc).isoformat(),
        }


def _log_lesson(skill_name: str, error: str) -> None:
    with open("logs/lessons.md", "a", encoding="utf-8") as handle:
        handle.write(f"- [{datetime.now(timezone.utc).isoformat()}] {skill_name}: {error}\n")
