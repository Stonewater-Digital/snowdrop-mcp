"""Generate deprecation notices for public APIs."""
from __future__ import annotations

from datetime import datetime, timezone
from typing import Any

TOOL_META: dict[str, Any] = {
    "name": "deprecation_notice_generator",
    "description": "Formats structured deprecation notices for skills/endpoints.",
    "inputSchema": {
        "type": "object",
        "properties": {
            "deprecated_items": {"type": "array", "items": {"type": "object"}},
        },
        "required": ["deprecated_items"],
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


def deprecation_notice_generator(deprecated_items: list[dict[str, Any]], **_: Any) -> dict[str, Any]:
    """Return formatted notices and summary stats."""
    try:
        notices = []
        upcoming = []
        for item in deprecated_items:
            notice = {
                "name": item.get("name"),
                "type": item.get("type"),
                "deprecated_date": item.get("deprecated_date"),
                "sunset_date": item.get("sunset_date"),
                "replacement": item.get("replacement"),
                "migration_guide": item.get("migration_guide"),
            }
            notices.append(notice)
            upcoming.append(item.get("sunset_date"))
        md_lines = ["# Deprecation Notices"]
        for notice in notices:
            md_lines.append(
                f"\n## {notice['name']} ({notice['type']})\n- Deprecated: {notice['deprecated_date']}\n- Sunset: {notice['sunset_date']}\n- Replacement: {notice.get('replacement') or 'TBD'}\n- Guide: {notice.get('migration_guide') or 'Contact support'}\n"
            )
        data = {
            "notices": notices,
            "active_deprecations": len(notices),
            "upcoming_sunsets": upcoming,
            "notice_md": "\n".join(md_lines),
        }
        return {
            "status": "success",
            "data": data,
            "timestamp": datetime.now(timezone.utc).isoformat(),
        }
    except Exception as exc:  # noqa: BLE001
        _log_lesson("deprecation_notice_generator", str(exc))
        return {
            "status": "error",
            "data": {"error": str(exc)},
            "timestamp": datetime.now(timezone.utc).isoformat(),
        }


def _log_lesson(skill_name: str, error: str) -> None:
    with open("logs/lessons.md", "a", encoding="utf-8") as handle:
        handle.write(f"- [{datetime.now(timezone.utc).isoformat()}] {skill_name}: {error}\n")
