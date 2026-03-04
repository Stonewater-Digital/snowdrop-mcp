"""Manage Ralph Wiggum retry logic before Thunder escalation."""
from __future__ import annotations

from datetime import datetime, timezone
from typing import Any

TOOL_META: dict[str, Any] = {
    "name": "ralph_wiggum_retry_manager",
    "description": "Determines whether to retry or escalate tasks per ethics playbook.",
    "inputSchema": {
        "type": "object",
        "properties": {
            "task_name": {"type": "string"},
            "attempt_number": {"type": "integer"},
            "max_attempts": {"type": "integer", "default": 3},
            "previous_error": {"type": ["string", "null"]},
            "previous_lessons": {
                "type": "array",
                "items": {"type": "string"},
                "default": [],
            },
        },
        "required": ["task_name", "attempt_number"],
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


def ralph_wiggum_retry_manager(
    task_name: str,
    attempt_number: int,
    max_attempts: int = 3,
    previous_error: str | None = None,
    previous_lessons: list[str] | None = None,
    **_: Any,
) -> dict[str, Any]:
    """Return retry or escalate guidance."""
    try:
        lessons = previous_lessons or []
        if attempt_number < max_attempts:
            context = _build_retry_context(task_name, attempt_number, lessons, previous_error)
            action = {
                "action": "retry",
                "attempt": attempt_number + 1,
                "context_injection": context,
            }
        else:
            action = {
                "action": "escalate",
                "notify": "thunder_signal",
                "details": {
                    "task_name": task_name,
                    "last_error": previous_error,
                    "lessons": lessons,
                },
            }
        return {
            "status": "success",
            "data": action,
            "timestamp": datetime.now(timezone.utc).isoformat(),
        }
    except Exception as exc:
        _log_lesson("ralph_wiggum_retry_manager", str(exc))
        return {
            "status": "error",
            "data": {"error": str(exc)},
            "timestamp": datetime.now(timezone.utc).isoformat(),
        }


def _build_retry_context(
    task_name: str,
    attempt_number: int,
    lessons: list[str],
    previous_error: str | None,
) -> str:
    lesson_text = "; ".join(lessons) if lessons else "No logged lessons yet"
    error_text = previous_error or "Unspecified error"
    return (
        f"Task {task_name} attempt {attempt_number} failed due to {error_text}."
        f" Inject lessons: {lesson_text}. Emphasize mitigation and new debug steps."
    )


def _log_lesson(skill_name: str, error: str) -> None:
    with open("logs/lessons.md", "a", encoding="utf-8") as handle:
        handle.write(f"- [{datetime.now(timezone.utc).isoformat()}] {skill_name}: {error}\n")
