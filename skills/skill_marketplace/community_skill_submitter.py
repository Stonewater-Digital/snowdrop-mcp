"""Accept community skill submissions for review."""
from __future__ import annotations

import json
import os
import re
import uuid
from datetime import datetime, timezone
from typing import Any

LOG_PATH = "logs/community_skill_submissions.jsonl"

TOOL_META: dict[str, Any] = {
    "name": "community_skill_submitter",
    "description": "Validates community skill code before it enters the review queue.",
    "inputSchema": {
        "type": "object",
        "properties": {
            "agent_id": {"type": "string"},
            "skill_name": {"type": "string"},
            "skill_code": {"type": "string"},
            "description": {"type": "string"},
            "category": {"type": "string"},
            "requested_price": {"type": "number"},
        },
        "required": [
            "agent_id",
            "skill_name",
            "skill_code",
            "description",
            "category",
            "requested_price",
        ],
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

RE_DENY = re.compile(r"(os\.system|subprocess|eval\(|exec\()")


def community_skill_submitter(
    agent_id: str,
    skill_name: str,
    skill_code: str,
    description: str,
    category: str,
    requested_price: float,
    **_: Any,
) -> dict[str, Any]:
    """Validate the submission and add it to the queue."""
    try:
        if requested_price < 0:
            raise ValueError("requested_price cannot be negative")
        errors = []
        if "TOOL_META" not in skill_code:
            errors.append("TOOL_META definition missing")
        if f"def {skill_name}" not in skill_code:
            errors.append("Main function not found")
        if "_log_lesson" not in skill_code:
            errors.append("_log_lesson helper missing")
        if RE_DENY.search(skill_code):
            errors.append("Prohibited system call detected")
        if "return {\"status\"" not in skill_code.replace("'", "\""):
            errors.append("Return envelope missing")
        submission_id = str(uuid.uuid4())
        submission_record = {
            "submission_id": submission_id,
            "agent_id": agent_id,
            "skill_name": skill_name,
            "description": description,
            "category": category,
            "requested_price": requested_price,
            "validation_errors": errors,
            "status": "pending_review",
            "submitted_at": datetime.now(timezone.utc).isoformat(),
        }
        _append_jsonl(LOG_PATH, submission_record)
        data = {
            "submission_id": submission_id,
            "validation_passed": not errors,
            "validation_errors": errors,
            "status": "pending_review",
            "estimated_review_time": "48h",
        }
        return {
            "status": "success",
            "data": data,
            "timestamp": submission_record["submitted_at"],
        }
    except Exception as exc:
        _log_lesson("community_skill_submitter", str(exc))
        return {
            "status": "error",
            "data": {"error": str(exc)},
            "timestamp": datetime.now(timezone.utc).isoformat(),
        }


def _append_jsonl(path: str, payload: dict[str, Any]) -> None:
    os.makedirs(os.path.dirname(path), exist_ok=True)
    with open(path, "a", encoding="utf-8") as handle:
        handle.write(json.dumps(payload) + "\n")


def _log_lesson(skill_name: str, error: str) -> None:
    with open("logs/lessons.md", "a", encoding="utf-8") as handle:
        handle.write(f"- [{datetime.now(timezone.utc).isoformat()}] {skill_name}: {error}\n")
