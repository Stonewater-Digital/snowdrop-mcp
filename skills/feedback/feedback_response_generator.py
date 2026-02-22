"""Create responses to agent feedback."""
from __future__ import annotations

from datetime import datetime, timezone
from typing import Any

TEMPLATES = {
    "bug": "Thanks for reporting this bug. Engineering is investigating and we'll update you soon.",
    "feature_request": "Appreciate the feature idea! We've added it to the backlog and will consider it during prioritization.",
    "praise": "Thank you! We're glad the skill is helping—keep the wins coming.",
    "complaint": "Thanks for raising this. We're reviewing the experience to address your concern.",
    "suggestion": "Great suggestion. We'll evaluate how it fits into the roadmap.",
}

TOOL_META: dict[str, Any] = {
    "name": "feedback_response_generator",
    "description": "Generates human-like responses to agent feedback with priority flags.",
    "inputSchema": {
        "type": "object",
        "properties": {
            "feedback": {"type": "object"},
        },
        "required": ["feedback"],
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


def feedback_response_generator(feedback: dict[str, Any], **_: Any) -> dict[str, Any]:
    """Return tailored response and escalation guidance."""
    try:
        feedback_type = feedback.get("type", "suggestion")
        template = TEMPLATES.get(feedback_type, TEMPLATES["suggestion"])
        rating = feedback.get("rating") or 0
        agent_tier = feedback.get("agent_tier", "standard")
        priority = "high" if agent_tier == "premium" or feedback_type == "bug" else "normal"
        escalate = priority == "high" and rating <= 2
        follow_up = "Create Jira ticket" if feedback_type in {"bug", "complaint"} else None
        data = {
            "response": template,
            "priority": priority,
            "follow_up_action": follow_up,
            "escalate": escalate,
        }
        return {
            "status": "success",
            "data": data,
            "timestamp": datetime.now(timezone.utc).isoformat(),
        }
    except Exception as exc:  # noqa: BLE001
        _log_lesson("feedback_response_generator", str(exc))
        return {
            "status": "error",
            "data": {"error": str(exc)},
            "timestamp": datetime.now(timezone.utc).isoformat(),
        }


def _log_lesson(skill_name: str, error: str) -> None:
    with open("logs/lessons.md", "a", encoding="utf-8") as handle:
        handle.write(f"- [{datetime.now(timezone.utc).isoformat()}] {skill_name}: {error}\n")
