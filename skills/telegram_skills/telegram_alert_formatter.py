"""Format alerts for Telegram with MarkdownV2."""
from __future__ import annotations

from datetime import datetime, timezone
from typing import Any, Iterable

SPECIAL_CHARS = "_[]()~`>#+-=|{}.!"

TOOL_META: dict[str, Any] = {
    "name": "telegram_alert_formatter",
    "description": "Formats alerts using Telegram MarkdownV2 with escaping and CTA support.",
    "inputSchema": {
        "type": "object",
        "properties": {
            "title": {"type": "string"},
            "body_lines": {
                "type": "array",
                "items": {"type": "string"},
            },
            "cta_url": {"type": "string"},
        },
        "required": ["title", "body_lines"],
    },
    "outputSchema": {
        "type": "object",
        "properties": {
            "status": {"type": "string"},
            "data": {
                "type": "object",
                "properties": {
                    "message": {"type": "string"},
                },
            },
            "timestamp": {"type": "string"},
        },
    },
}


def telegram_alert_formatter(
    title: str,
    body_lines: Iterable[str],
    cta_url: str | None = None,
    **_: Any,
) -> dict[str, Any]:
    """Produce a Telegram-safe MarkdownV2 alert."""
    try:
        escaped_title = _escape(title)
        escaped_lines = [f"• {_escape(line)}" for line in body_lines]
        message = f"*{escaped_title}*\n" + "\n".join(escaped_lines)
        if cta_url:
            message += f"\n[Tap to review]({_escape(cta_url)})"
        data = {"message": message}
        return {
            "status": "success",
            "data": data,
            "timestamp": datetime.now(timezone.utc).isoformat(),
        }
    except Exception as exc:
        _log_lesson("telegram_alert_formatter", str(exc))
        return {
            "status": "error",
            "data": {"error": str(exc)},
            "timestamp": datetime.now(timezone.utc).isoformat(),
        }


def _escape(text: str) -> str:
    escaped = []
    for char in text:
        if char in SPECIAL_CHARS:
            escaped.append(f"\\{char}")
        else:
            escaped.append(char)
    return "".join(escaped)


def _log_lesson(skill_name: str, error: str) -> None:
    with open("logs/lessons.md", "a", encoding="utf-8") as handle:
        handle.write(f"- [{datetime.now(timezone.utc).isoformat()}] {skill_name}: {error}\n")
