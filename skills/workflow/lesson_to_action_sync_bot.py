"""
Executive Summary: Converts lessons log entries into structured action recommendations and cluster stats for Thunder and Ops pods.

Inputs: lessons_path (str, optional), owner_map (dict[str, str], optional), max_items (int, optional)
Outputs: status (str), data (actions/clusters/summary), timestamp (str)
MCP Tool Name: lesson_to_action_sync_bot
"""
from __future__ import annotations

from collections import Counter, defaultdict
from pathlib import Path
from typing import Any

from skills.utils import (
    SkillTelemetryEmitter,
    get_iso_timestamp,
    logger,
    log_lesson as _shared_log_lesson,
)

TOOL_META: dict[str, Any] = {
    "name": "lesson_to_action_sync_bot",
    "description": "Scan logs/lessons.md, cluster recurring entries, and emit recommended follow-up actions.",
    "inputSchema": {
        "type": "object",
        "properties": {
            "lessons_path": {
                "type": "string",
                "default": "logs/lessons.md",
                "description": "Path to Ralph Wiggum log file.",
            },
            "owner_map": {
                "type": "object",
                "description": "Keyword -> owner/team routing map to tag recommendations.",
            },
            "max_items": {
                "type": "integer",
                "default": 10,
                "description": "Maximum number of action recommendations to return.",
            },
        },
    },
    "outputSchema": {
        "type": "object",
        "properties": {
            "status": {"type": "string", "enum": ["ok", "error"]},
            "data": {
                "type": "object",
                "properties": {
                    "actions": {"type": "array", "items": {"type": "object"}},
                    "clusters": {"type": "array", "items": {"type": "object"}},
                    "summary": {"type": "object"},
                },
            },
            "timestamp": {"type": "string", "format": "date-time"},
        },
        "required": ["status", "timestamp"],
    },
}


def lesson_to_action_sync_bot(
    lessons_path: str = "logs/lessons.md",
    owner_map: dict[str, str] | None = None,
    max_items: int = 10,
) -> dict[str, Any]:
    """Convert lessons log into structured actions and cluster stats.

    Args:
        lessons_path: Path to lessons log file.
        owner_map: Keyword routes for recommended owner tagging.
        max_items: Maximum number of actions to return.

    Returns:
        Snowdrop response dict containing actions, clusters, and summary metrics.

    Raises:
        ValueError: When lessons_path is invalid or max_items < 1.
    """
    emitter = SkillTelemetryEmitter(
        "lesson_to_action_sync_bot",
        {
            "lessons_path": lessons_path,
            "owner_map": len(owner_map or {}),
            "max_items": max_items,
        },
    )
    try:
        if max_items <= 0:
            raise ValueError("max_items must be positive")
        normalized_owner_map = _normalize_owner_map(owner_map)
        lessons_file = Path(lessons_path)
        if not lessons_file.exists():
            raise ValueError(f"Lessons file not found: {lessons_path}")

        lines = lessons_file.read_text(encoding="utf-8").splitlines()
        entries = _parse_lessons(lines)

        if not entries:
            _log_lesson("lesson_to_action_sync_bot", "Lessons log empty or unparsable")

        summary = _build_summary(lines, entries)
        actions = _build_actions(entries, normalized_owner_map, max_items)
        clusters = _build_clusters(entries)

        data = {"actions": actions, "clusters": clusters, "summary": summary}
        emitter.record(
            "ok",
            {
                "actions": len(actions),
                "clusters": len(clusters),
                "entries_processed": summary["processed_entries"],
            },
        )
        return {"status": "ok", "data": data, "timestamp": get_iso_timestamp()}
    except Exception as exc:
        msg = f"lesson_to_action_sync_bot failed: {exc}"
        logger.error(msg)
        _log_lesson("lesson_to_action_sync_bot", str(exc))
        emitter.record("error", {"error": str(exc)})
        return {"status": "error", "data": {"error": str(exc)}, "timestamp": get_iso_timestamp()}


def _normalize_owner_map(owner_map: dict[str, str] | None) -> dict[str, str]:
    """Return a lowercase keyword -> owner map."""
    if not owner_map:
        return {}
    normalized: dict[str, str] = {}
    for key, value in owner_map.items():
        if not isinstance(key, str) or not isinstance(value, str):
            continue
        normalized[key.lower()] = value
    return normalized


def _parse_lessons(lines: list[str]) -> list[dict[str, Any]]:
    """Parse lessons lines into structured entries."""
    entries: list[dict[str, Any]] = []
    for line in lines:
        text = line.strip()
        if not text.startswith("- ["):
            continue

        try:
            _, remainder = text.split("] ", maxsplit=1)
        except ValueError:
            continue

        if ":" in remainder:
            skill, message = remainder.split(":", maxsplit=1)
        else:
            skill, message = "unknown", remainder

        skill_name = skill.strip()
        lesson_text = message.strip()
        if not lesson_text:
            continue

        entries.append(
            {
                "skill": skill_name or "unknown",
                "lesson": lesson_text,
            }
        )
    return entries


def _build_summary(lines: list[str], entries: list[dict[str, Any]]) -> dict[str, Any]:
    """Create summary metadata about processed lessons."""
    unique_lessons = {entry["lesson"] for entry in entries}
    return {
        "total_lines": len(lines),
        "processed_entries": len(entries),
        "unique_lessons": len(unique_lessons),
        "timestamp": get_iso_timestamp(),
    }


def _build_actions(
    entries: list[dict[str, Any]],
    owner_map: dict[str, str],
    max_items: int,
) -> list[dict[str, Any]]:
    """Return recommended actions sorted by severity and frequency."""
    counter = Counter(entry["lesson"] for entry in entries)
    ranked = counter.most_common(max_items * 2)
    actions: list[dict[str, Any]] = []

    for lesson, count in ranked:
        severity = "high" if count >= 5 else "medium" if count >= 2 else "low"
        recommended_owner = _route_owner(lesson, owner_map)
        next_step = f"Create remediation task for: {lesson}"
        action = {
            "lesson": lesson,
            "occurrences": count,
            "severity": severity,
            "recommended_owner": recommended_owner,
            "next_step": next_step,
        }
        actions.append(action)
        if len(actions) >= max_items:
            break
    return actions


def _route_owner(lesson: str, owner_map: dict[str, str]) -> str:
    """Determine recommended owner using keyword routing."""
    lowered = lesson.lower()
    for keyword, owner in owner_map.items():
        if keyword in lowered:
            return owner
    return "ops_enablement"


def _build_clusters(entries: list[dict[str, Any]]) -> list[dict[str, Any]]:
    """Group lessons by skill for quick analytics."""
    cluster_map: dict[str, defaultdict[str, int]] = defaultdict(lambda: defaultdict(int))
    for entry in entries:
        cluster_map[entry["skill"]][entry["lesson"]] += 1

    clusters: list[dict[str, Any]] = []
    for skill, lessons in cluster_map.items():
        clusters.append(
            {
                "skill": skill,
                "lesson_count": sum(lessons.values()),
                "top_lessons": sorted(lessons.items(), key=lambda item: item[1], reverse=True)[:3],
            }
        )
    return clusters


def _log_lesson(skill_name: str, error: str) -> None:
    """Proxy to shared lesson logger."""
    _shared_log_lesson(skill_name, error)
