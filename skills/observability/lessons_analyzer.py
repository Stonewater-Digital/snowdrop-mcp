"""Analyze Ralph Wiggum lesson entries."""
from __future__ import annotations

from collections import Counter
from datetime import datetime, timedelta, timezone
from typing import Any

TOOL_META: dict[str, Any] = {
    "name": "lessons_analyzer",
    "description": "Parses logs/lessons.md content for failure hotspots and trends.",
    "inputSchema": {
        "type": "object",
        "properties": {
            "lessons_content": {"type": "string"},
            "time_range_hours": {"type": ["integer", "null"]},
        },
        "required": ["lessons_content"],
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


def lessons_analyzer(
    lessons_content: str,
    time_range_hours: int | None = None,
    **_: Any,
) -> dict[str, Any]:
    """Return failure stats and directional trend."""

    try:
        entries = _parse_lessons(lessons_content, time_range_hours)
        counter = Counter(entry["skill"] for entry in entries)
        top_errors = counter.most_common(5)
        error_trend = _trend(entries)
        data = {
            "top_errors": [{"skill": skill, "count": count} for skill, count in top_errors],
            "error_trend": error_trend,
            "skills_most_failing": [skill for skill, _ in top_errors],
            "total_lessons": len(entries),
        }
        return {
            "status": "success",
            "data": data,
            "timestamp": datetime.now(timezone.utc).isoformat(),
        }
    except Exception as exc:
        _log_lesson("lessons_analyzer", str(exc))
        return {
            "status": "error",
            "data": {"error": str(exc)},
            "timestamp": datetime.now(timezone.utc).isoformat(),
        }


def _parse_lessons(content: str, time_range_hours: int | None) -> list[dict[str, Any]]:
    entries: list[dict[str, Any]] = []
    cutoff = None
    if time_range_hours:
        cutoff = datetime.now(timezone.utc) - timedelta(hours=time_range_hours)
    for line in content.splitlines():
        if not line.startswith("- ["):
            continue
        try:
            ts_text, remainder = line[3:].split("]", 1)
            timestamp = datetime.fromisoformat(ts_text)
            if cutoff and timestamp < cutoff:
                continue
            skill, error = remainder.strip().split(":", 1)
            entries.append({"timestamp": timestamp, "skill": skill.strip(), "error": error.strip()})
        except ValueError:
            continue
    return entries


def _trend(entries: list[dict[str, Any]]) -> str:
    if len(entries) < 6:
        return "insufficient data"
    midpoint = len(entries) // 2
    first_half = entries[:midpoint]
    second_half = entries[midpoint:]
    if len(second_half) > len(first_half) * 1.2:
        return "spiking"
    if len(second_half) < len(first_half) * 0.8:
        return "improving"
    return "steady"


def _log_lesson(skill_name: str, error: str) -> None:
    with open("logs/lessons.md", "a", encoding="utf-8") as handle:
        handle.write(f"- [{datetime.now(timezone.utc).isoformat()}] {skill_name}: {error}\n")
