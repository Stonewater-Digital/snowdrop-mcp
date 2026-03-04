"""Coordinate community hackathons and judging."""
from __future__ import annotations

from datetime import datetime, timezone
from typing import Any

TOOL_META: dict[str, Any] = {
    "name": "hackathon_coordinator",
    "description": "Manages hackathon lifecycle and scores submissions when provided.",
    "inputSchema": {
        "type": "object",
        "properties": {
            "hackathon": {"type": "object"},
            "submissions": {"type": ["array", "null"], "default": None},
        },
        "required": ["hackathon"],
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

WEIGHTS = {
    "functionality": 0.4,
    "creativity": 0.25,
    "code_quality": 0.2,
    "documentation": 0.15,
}


def hackathon_coordinator(
    hackathon: dict[str, Any],
    submissions: list[dict[str, Any]] | None = None,
    **_: Any,
) -> dict[str, Any]:
    """Return hackathon phase, stats, and optional rankings."""
    try:
        now = datetime.now(timezone.utc)
        start = datetime.fromisoformat(hackathon.get("start_date").replace("Z", "+00:00"))
        end = datetime.fromisoformat(hackathon.get("end_date").replace("Z", "+00:00"))
        phase = _determine_phase(now, start, end, submissions)
        rankings = _score_submissions(submissions) if submissions else None
        participants = len(hackathon.get("participants", []))
        data = {
            "phase": phase,
            "participants": participants,
            "submissions": len(submissions or []),
            "rankings": rankings,
        }
        return {
            "status": "success",
            "data": data,
            "timestamp": now.isoformat(),
        }
    except Exception as exc:
        _log_lesson("hackathon_coordinator", str(exc))
        return {
            "status": "error",
            "data": {"error": str(exc)},
            "timestamp": datetime.now(timezone.utc).isoformat(),
        }


def _determine_phase(now: datetime, start: datetime, end: datetime, submissions: list[dict[str, Any]] | None) -> str:
    if now < start:
        return "registration"
    if start <= now <= end:
        return "building"
    if submissions and now > end:
        return "judging"
    if now > end:
        return "awards"
    return "planning"


def _score_submissions(submissions: list[dict[str, Any]]) -> list[dict[str, Any]]:
    rankings = []
    for submission in submissions:
        score = 0.0
        for metric, weight in WEIGHTS.items():
            metric_score = float(submission.get(metric, 0))
            score += metric_score * weight
        rankings.append({**submission, "score": round(score, 3)})
    rankings.sort(key=lambda entry: entry["score"], reverse=True)
    return rankings


def _log_lesson(skill_name: str, error: str) -> None:
    with open("logs/lessons.md", "a", encoding="utf-8") as handle:
        handle.write(f"- [{datetime.now(timezone.utc).isoformat()}] {skill_name}: {error}\n")
