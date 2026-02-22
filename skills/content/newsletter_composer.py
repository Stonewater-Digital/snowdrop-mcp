"""Compose Snowdrop newsletters."""
from __future__ import annotations

from datetime import datetime, timezone
from typing import Any

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
        "required": ["period", "new_skills", "top_performing_skills", "platform_metrics", "announcements", "educational_tip"],
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
        newsletter_md = f"""# Snowdrop Dispatch — {period}

## What's New
- {('\n- '.join(new_skills)) if new_skills else 'No new skills this cycle'}

## Top Skills This Week
- {('\n- '.join(top_performing_skills)) if top_performing_skills else 'Stay tuned for next highlight'}

## Platform Stats
- Agents: {platform_metrics.get('agents_count', 0)}
- Uptime: {platform_metrics.get('uptime', '99.9%')}
- Total Calls: {platform_metrics.get('total_calls', 0)}

## Announcements
- {('\n- '.join(announcements)) if announcements else 'Nothing pressing this week'}

## Tip of the Week
{educational_tip}
"""
        subject_line = f"Snowdrop Weekly — {period}"
        preview_text = f"{len(new_skills)} new skills, {platform_metrics.get('total_calls', 0)} calls, tip inside"
        data = {
            "newsletter_md": newsletter_md.strip(),
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


def _log_lesson(skill_name: str, error: str) -> None:
    with open("logs/lessons.md", "a", encoding="utf-8") as handle:
        handle.write(f"- [{datetime.now(timezone.utc).isoformat()}] {skill_name}: {error}\n")
