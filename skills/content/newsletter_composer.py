"""Compose Snowdrop newsletters."""
from __future__ import annotations

from datetime import datetime, timezone
from typing import Any

from skills.utils import _log_lesson

TOOL_META: dict[str, Any] = {
    "name": "newsletter_composer",
    "description": "Creates newsletters covering new skills, platform stats, and educational tips.",
    "inputSchema": {
        "type": "object",
        "properties": {
            "period": {"type": "string"},
            "new_skills": {"type": "array", "items": {"type": "string"}},
            "top_performing_skills": {"type": "array", "items": {"type": "string"}},
            "platform_metrics": {"type": "object"},
            "announcements": {"type": "array", "items": {"type": "string"}},
            "educational_tip": {"type": "string"},
        },
        "required": [
            "period",
            "new_skills",
            "top_performing_skills",
            "platform_metrics",
            "announcements",
            "educational_tip",
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


def newsletter_composer(
    period: str,
    new_skills: list[str],
    top_performing_skills: list[str],
    platform_metrics: dict[str, Any],
    announcements: list[str],
    educational_tip: str,
    **_: Any,
) -> dict[str, Any]:
    """Return newsletter markdown, subject, and preview text."""

    try:
        blocks = {
            "new": _format_bullets(new_skills, "No new skills this cycle"),
            "top": _format_bullets(
                top_performing_skills, "Stay tuned for next highlight"
            ),
            "announcements": _format_bullets(announcements, "Nothing pressing this week"),
        }
        stats = {
            "agents": platform_metrics.get("agents_count", 0),
            "uptime": platform_metrics.get("uptime", "99.9%"),
            "total_calls": platform_metrics.get("total_calls", 0),
        }
        newsletter_md = (
            f"# Snowdrop Dispatch — {period}\n\n"
            f"## What's New\n{blocks['new']}\n\n"
            f"## Top Skills This Week\n{blocks['top']}\n\n"
            "## Platform Stats\n"
            f"- Agents: {stats['agents']}\n"
            f"- Uptime: {stats['uptime']}\n"
            f"- Total Calls: {stats['total_calls']}\n\n"
            f"## Announcements\n{blocks['announcements']}\n\n"
            f"## Tip of the Week\n{educational_tip}"
        ).strip()
        subject_line = f"Snowdrop Weekly — {period}"
        preview_text = (
            f"{len(new_skills)} new skills, {stats['total_calls']} calls, tip inside"
        )
        data = {
            "newsletter_md": newsletter_md,
            "subject_line": subject_line,
            "preview_text": preview_text,
        }
        return {
            "status": "success",
            "data": data,
            "timestamp": datetime.now(timezone.utc).isoformat(),
        }
    except Exception as exc:  # noqa: BLE001
        _log_lesson("newsletter_composer", str(exc))
        return {
            "status": "error",
            "data": {"error": str(exc)},
            "timestamp": datetime.now(timezone.utc).isoformat(),
        }


def _format_bullets(entries: list[str], fallback: str) -> str:
    """Render bullet list markdown."""

    if not entries:
        return fallback
    return "- " + "\n- ".join(entries)
