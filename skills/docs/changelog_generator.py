"""Generate changelog entries from structured change data."""
from __future__ import annotations

from collections import Counter
from datetime import datetime, timezone
from typing import Any

TOOL_META: dict[str, Any] = {
    "name": "changelog_generator",
    "description": "Outputs Keep a Changelog formatted text from change entries.",
    "inputSchema": {
        "type": "object",
        "properties": {
            "changes": {
                "type": "array",
                "items": {"type": "object"},
            }
        },
        "required": ["changes"],
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


_SECTION_ORDER = ["added", "modified", "fixed", "removed"]


def changelog_generator(changes: list[dict[str, Any]], **_: Any) -> dict[str, Any]:
    """Render a changelog and stats from change dicts."""
    try:
        if not isinstance(changes, list):
            raise ValueError("changes must be a list")

        grouped: dict[str, list[str]] = {section: [] for section in _SECTION_ORDER}
        stats = Counter()
        for change in changes:
            if not isinstance(change, dict):
                raise ValueError("each change must be a dict")
            change_type = str(change.get("change_type", "added")).lower()
            description = change.get("description", "")
            name = change.get("name", "")
            line = f"- {name}: {description}" if name else f"- {description}"
            grouped.setdefault(change_type, []).append(line)
            stats[change_type] += 1

        today = datetime.now(timezone.utc).date().isoformat()
        lines = ["# Changelog", f"\n## [Unreleased] - {today}"]
        for section in _SECTION_ORDER:
            entries = grouped.get(section, [])
            if not entries:
                continue
            title = section.capitalize()
            lines.append(f"\n### {title}")
            lines.extend(entries)

        result = {
            "changelog_md": "\n".join(lines),
            "stats": dict(stats),
        }
        return {
            "status": "success",
            "data": result,
            "timestamp": datetime.now(timezone.utc).isoformat(),
        }
    except Exception as exc:  # noqa: BLE001
        _log_lesson("changelog_generator", str(exc))
        return {
            "status": "error",
            "data": {"error": str(exc)},
            "timestamp": datetime.now(timezone.utc).isoformat(),
        }


def _log_lesson(skill_name: str, error: str) -> None:
    with open("logs/lessons.md", "a", encoding="utf-8") as handle:
        handle.write(f"- [{datetime.now(timezone.utc).isoformat()}] {skill_name}: {error}\n")
