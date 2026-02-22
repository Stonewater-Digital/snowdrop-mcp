"""Estimate review cost for community submissions."""
from __future__ import annotations

from datetime import datetime, timezone
from typing import Any

COMPLEXITY_MULTIPLIER = {"low": 1.0, "medium": 2.0, "high": 3.0}

TOOL_META: dict[str, Any] = {
    "name": "review_cost_estimator",
    "description": "Approximates token/time cost to review a submission.",
    "inputSchema": {
        "type": "object",
        "properties": {
            "submission": {"type": "object"},
        },
        "required": ["submission"],
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


def review_cost_estimator(submission: dict[str, Any], **_: Any) -> dict[str, Any]:
    """Return review token estimates."""
    try:
        lines = submission.get("lines_of_code", 0)
        complexity = COMPLEXITY_MULTIPLIER.get(submission.get("complexity", "low"), 1.0)
        has_tests = submission.get("has_tests", False)
        follows_pattern = submission.get("follows_pattern", True)
        base_tokens = lines * 4
        estimate_tokens = int(base_tokens * complexity)
        if not has_tests:
            estimate_tokens += 200
        if not follows_pattern:
            estimate_tokens += 150
        estimated_cost = estimate_tokens / 1000 * 3  # assume Sonnet $3/MTok
        review_time = int(estimate_tokens / 200)
        auto_reviewable = complexity == 1.0 and follows_pattern
        recommendation = "auto_merge" if auto_reviewable else "manual_review"
        data = {
            "estimated_tokens": estimate_tokens,
            "estimated_review_cost_usd": round(estimated_cost, 2),
            "estimated_review_time_minutes": review_time,
            "auto_reviewable": auto_reviewable,
            "recommendation": recommendation,
        }
        return {
            "status": "success",
            "data": data,
            "timestamp": datetime.now(timezone.utc).isoformat(),
        }
    except Exception as exc:
        _log_lesson("review_cost_estimator", str(exc))
        return {
            "status": "error",
            "data": {"error": str(exc)},
            "timestamp": datetime.now(timezone.utc).isoformat(),
        }


def _log_lesson(skill_name: str, error: str) -> None:
    with open("logs/lessons.md", "a", encoding="utf-8") as handle:
        handle.write(f"- [{datetime.now(timezone.utc).isoformat()}] {skill_name}: {error}\n")
