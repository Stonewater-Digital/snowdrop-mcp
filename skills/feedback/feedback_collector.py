"""Collect structured agent feedback."""
from __future__ import annotations

import json
import uuid
from datetime import datetime, timezone
from pathlib import Path
from typing import Any

LOG_PATH = Path("logs/feedback.jsonl")
KEYWORDS = {
    "bug": ["error", "bug", "broken"],
    "feature_request": ["would love", "add", "feature"],
    "praise": ["love", "great", "awesome"],
    "complaint": ["frustrated", "angry", "annoyed"],
    "suggestion": ["maybe", "consider", "idea"],
}

TOOL_META: dict[str, Any] = {
    "name": "feedback_collector",
    "description": "Stores categorized feedback with auto-responses.",
    "inputSchema": {
        "type": "object",
        "properties": {
            "agent_id": {"type": "string"},
            "feedback_type": {
                "type": "string",
                "enum": ["bug", "feature_request", "praise", "complaint", "suggestion"],
            },
            "skill_name": {"type": "string"},
            "message": {"type": "string"},
            "rating": {"type": "integer"},
        },
        "required": ["agent_id", "feedback_type", "message"],
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


def feedback_collector(
    agent_id: str,
    feedback_type: str,
    message: str,
    skill_name: str | None = None,
    rating: int | None = None,
    **_: Any,
) -> dict[str, Any]:
    """Save feedback entry and respond."""
    try:
        rating = rating if rating is None or 1 <= rating <= 5 else None
        feedback_id = str(uuid.uuid4())
        category = _auto_category(message, feedback_type)
        record = {
            "feedback_id": feedback_id,
            "agent_id": agent_id,
            "feedback_type": feedback_type,
            "category": category,
            "skill_name": skill_name,
            "message": message,
            "rating": rating,
            "timestamp": datetime.now(timezone.utc).isoformat(),
        }
        LOG_PATH.parent.mkdir(parents=True, exist_ok=True)
        with LOG_PATH.open("a", encoding="utf-8") as handle:
            handle.write(json.dumps(record) + "\n")
        auto_response = "Thanks for helping level up Snowdrop!"
        data = {
            "feedback_id": feedback_id,
            "category": category,
            "acknowledged": True,
            "auto_response": auto_response,
        }
        return {
            "status": "success",
            "data": data,
            "timestamp": record["timestamp"],
        }
    except Exception as exc:  # noqa: BLE001
        _log_lesson("feedback_collector", str(exc))
        return {
            "status": "error",
            "data": {"error": str(exc)},
            "timestamp": datetime.now(timezone.utc).isoformat(),
        }


def _auto_category(message: str, fallback: str) -> str:
    lower = message.lower()
    for category, keywords in KEYWORDS.items():
        if any(keyword in lower for keyword in keywords):
            return category
    return fallback


def _log_lesson(skill_name: str, error: str) -> None:
    with open("logs/lessons.md", "a", encoding="utf-8") as handle:
        handle.write(f"- [{datetime.now(timezone.utc).isoformat()}] {skill_name}: {error}\n")
