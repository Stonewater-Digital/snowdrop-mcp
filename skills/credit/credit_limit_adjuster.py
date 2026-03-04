"""Recommend credit limit adjustments."""
from __future__ import annotations

from datetime import datetime, timedelta, timezone
from typing import Any

TOOL_META: dict[str, Any] = {
    "name": "credit_limit_adjuster",
    "description": "Applies utilization and score rules to tab limit changes.",
    "inputSchema": {
        "type": "object",
        "properties": {
            "agent_id": {"type": "string"},
            "current_limit": {"type": "number"},
            "credit_score": {"type": "integer"},
            "utilization_pct": {"type": "number"},
            "months_since_last_review": {"type": "integer"},
        },
        "required": [
            "agent_id",
            "current_limit",
            "credit_score",
            "utilization_pct",
            "months_since_last_review",
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


def credit_limit_adjuster(
    agent_id: str,
    current_limit: float,
    credit_score: int,
    utilization_pct: float,
    months_since_last_review: int,
    **_: Any,
) -> dict[str, Any]:
    """Return the proposed action for a credit limit review."""
    try:
        if current_limit <= 0:
            raise ValueError("current_limit must be positive")
        if months_since_last_review < 0:
            raise ValueError("months_since_last_review cannot be negative")

        if (
            credit_score > 700
            and utilization_pct < 50
            and months_since_last_review >= 6
        ):
            action = "increase"
            multiplier = 1.25
            reason = "Strong score, low utilization, stale review"
        elif credit_score < 500 or utilization_pct > 90:
            action = "decrease"
            multiplier = 0.7
            reason = "High risk metrics triggered"
        else:
            action = "hold"
            multiplier = 1.0
            reason = "Risk within guardrails"

        new_limit = round(current_limit * multiplier, 2)
        review_gap = max(months_since_last_review, 3)
        next_review = datetime.now(timezone.utc) + timedelta(days=30 * review_gap)
        data = {
            "action": action,
            "new_limit": new_limit,
            "reason": reason,
            "next_review_date": next_review.isoformat(),
        }
        return {
            "status": "success",
            "data": data,
            "timestamp": datetime.now(timezone.utc).isoformat(),
        }
    except Exception as exc:
        _log_lesson("credit_limit_adjuster", str(exc))
        return {
            "status": "error",
            "data": {"error": str(exc)},
            "timestamp": datetime.now(timezone.utc).isoformat(),
        }


def _log_lesson(skill_name: str, error: str) -> None:
    with open("logs/lessons.md", "a", encoding="utf-8") as handle:
        handle.write(f"- [{datetime.now(timezone.utc).isoformat()}] {skill_name}: {error}\n")
