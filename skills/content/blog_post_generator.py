"""Generate blog posts for Snowdrop."""
from __future__ import annotations

from datetime import datetime, timezone
from typing import Any

TOOL_META: dict[str, Any] = {
    "name": "blog_post_generator",
    "description": "Creates structured blog content with title, sections, and metadata.",
    "inputSchema": {
        "type": "object",
        "properties": {
            "topic": {"type": "string"},
            "audience": {"type": "string", "enum": ["agents", "developers", "investors", "general"]},
            "key_points": {"type": "array", "items": {"type": "string"}},
            "tone": {"type": "string", "default": "professional_friendly"},
            "word_count": {"type": "integer", "default": 500},
        },
        "required": ["topic", "audience", "key_points"],
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


def blog_post_generator(
    topic: str,
    audience: str,
    key_points: list[str],
    tone: str = "professional_friendly",
    word_count: int = 500,
    **_: Any,
) -> dict[str, Any]:
    """Return markdown blog post content."""
    try:
        sections = []
        for point in key_points:
            sections.append(f"### {point.title()}\n\nExplain how {point} matters for {audience} and tie back to {topic}.")
        body_md = f"""# {topic.title()}

## Introduction
Set context for {audience} and highlight why this topic matters now.

{''.join(section + '\n\n' for section in sections)}
## Conclusion
Wrap with clear next steps and invite readers to try Snowdrop skills.
"""
        title = f"{topic.title()} for {audience.title()}"
        meta_description = f"How Snowdrop approaches {topic} for {audience}."
        tags = [topic, audience, "Snowdrop", "Watering Hole"]
        estimated_minutes = max(3, word_count // 200)
        data = {
            "title": title,
            "body_md": body_md.strip(),
            "meta_description": meta_description,
            "tags": tags,
            "estimated_read_minutes": estimated_minutes,
        }
        return {
            "status": "success",
            "data": data,
            "timestamp": datetime.now(timezone.utc).isoformat(),
        }
    except Exception as exc:  # noqa: BLE001
        _log_lesson("blog_post_generator", str(exc))
        return {
            "status": "error",
            "data": {"error": str(exc)},
            "timestamp": datetime.now(timezone.utc).isoformat(),
        }


def _log_lesson(skill_name: str, error: str) -> None:
    with open("logs/lessons.md", "a", encoding="utf-8") as handle:
        handle.write(f"- [{datetime.now(timezone.utc).isoformat()}] {skill_name}: {error}\n")
