"""Post new community bounty opportunities."""
from __future__ import annotations

import json
import os
import uuid
from datetime import datetime, timezone
from typing import Any

LOG_PATH = "logs/bounties.jsonl"

TOOL_META: dict[str, Any] = {
    "name": "bounty_poster",
    "description": "Publishes new skill, feature, or bug-fix bounties to the community board.",
    "inputSchema": {
        "type": "object",
        "properties": {
            "title": {"type": "string"},
            "description": {"type": "string"},
            "reward_amount": {"type": "number"},
            "reward_currency": {
                "type": "string",
                "enum": ["USDC", "TON", "credit"],
            },
            "category": {
                "type": "string",
                "enum": [
                    "skill_creation",
                    "bug_fix",
                    "documentation",
                    "integration",
                    "research",
                ],
            },
            "deadline": {"type": ["string", "null"], "default": None},
            "difficulty": {
                "type": "string",
                "enum": ["beginner", "intermediate", "advanced", "expert"],
            },
        },
        "required": [
            "title",
            "description",
            "reward_amount",
            "reward_currency",
            "category",
            "difficulty",
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


_DIFFICULTY_APPLICANT_MAP = {
    "beginner": (25, 60),
    "intermediate": (15, 40),
    "advanced": (8, 20),
    "expert": (3, 10),
}


def bounty_poster(
    title: str,
    description: str,
    reward_amount: float,
    reward_currency: str,
    category: str,
    difficulty: str,
    deadline: str | None = None,
    **_: Any,
) -> dict[str, Any]:
    """Create a bounty entry and append it to the bounty log."""
    try:
        if reward_amount <= 0:
            raise ValueError("reward_amount must be positive")
        bounty_id = str(uuid.uuid4())
        now = datetime.now(timezone.utc)
        reward = {"amount": round(reward_amount, 2), "currency": reward_currency}
        bounty_record = {
            "bounty_id": bounty_id,
            "title": title,
            "description": description,
            "reward": reward,
            "category": category,
            "difficulty": difficulty,
            "deadline": deadline,
            "status": "open",
            "posted_at": now.isoformat(),
        }
        _append_jsonl(LOG_PATH, bounty_record)
        estimate_range = _DIFFICULTY_APPLICANT_MAP[difficulty]
        estimated_applicants = int(sum(estimate_range) / 2)
        data = {
            "bounty_id": bounty_id,
            "status": "open",
            "posted_at": bounty_record["posted_at"],
            "reward": reward,
            "estimated_applicants": estimated_applicants,
        }
        return {
            "status": "success",
            "data": data,
            "timestamp": now.isoformat(),
        }
    except Exception as exc:
        _log_lesson("bounty_poster", str(exc))
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
