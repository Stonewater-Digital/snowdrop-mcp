"""Generate failure diagnostics for Ralph Wiggum escalation."""
from __future__ import annotations

from collections import Counter
from datetime import datetime, timezone
from typing import Any

TOOL_META: dict[str, Any] = {
    "name": "failure_diagnostic_generator",
    "description": "Summarizes attempts, hypothesizes root causes, and prescribes human actions.",
    "inputSchema": {
        "type": "object",
        "properties": {
            "task_name": {"type": "string"},
            "attempts": {"type": "array", "items": {"type": "object"}},
            "system_state": {"type": "object"},
        },
        "required": ["task_name", "attempts", "system_state"],
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


def failure_diagnostic_generator(
    task_name: str,
    attempts: list[dict[str, Any]],
    system_state: dict[str, Any],
    **_: Any,
) -> dict[str, Any]:
    """Return diagnostic summary for Thunder."""
    try:
        if len(attempts) < 1:
            raise ValueError("attempts cannot be empty")
        error_terms = Counter()
        for attempt in attempts:
            error = str(attempt.get("error", "")).lower()
            for token in error.split():
                if token.isalpha() and len(token) > 3:
                    error_terms[token] += 1
        common_term = error_terms.most_common(1)
        root_cause = (
            f"Likely recurring issue around '{common_term[0][0]}'"
            if common_term
            else "Insufficient data; manual triage required"
        )
        diagnostic = {
            "task_name": task_name,
            "root_cause_hypothesis": root_cause,
            "attempted_fixes": attempts,
            "system_state_snapshot": system_state,
            "recommended_human_action": _recommend_action(system_state),
        }
        return {
            "status": "success",
            "data": diagnostic,
            "timestamp": datetime.now(timezone.utc).isoformat(),
        }
    except Exception as exc:
        _log_lesson("failure_diagnostic_generator", str(exc))
        return {
            "status": "error",
            "data": {"error": str(exc)},
            "timestamp": datetime.now(timezone.utc).isoformat(),
        }


def _recommend_action(system_state: dict[str, Any]) -> str:
    if system_state.get("api_health") == "down":
        return "Escalate to infra for API restart"
    if system_state.get("active_freezes"):
        return "Coordinate with Treasury to lift freezes before retry"
    return "Request Thunder guidance with fresh context log"


def _log_lesson(skill_name: str, error: str) -> None:
    with open("logs/lessons.md", "a", encoding="utf-8") as handle:
        handle.write(f"- [{datetime.now(timezone.utc).isoformat()}] {skill_name}: {error}\n")
