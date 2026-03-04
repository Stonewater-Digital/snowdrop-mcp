"""Construct SMTP payloads for Snowdrop email alerts."""
from __future__ import annotations

import os
from datetime import datetime, timezone
from typing import Any

TOOL_META: dict[str, Any] = {
    "name": "email_alert_builder",
    "description": "Prepares email payloads without sending them.",
    "inputSchema": {
        "type": "object",
        "properties": {
            "recipient": {"type": "string"},
            "subject": {"type": "string"},
            "body_sections": {
                "type": "array",
                "items": {"type": "object"},
            },
            "priority": {"type": "string"},
        },
        "required": ["recipient", "subject", "body_sections"]
    },
    "outputSchema": {
        "type": "object",
        "properties": {
            "status": {"type": "string"},
            "data": {
                "type": "object",
                "properties": {
                    "email": {"type": "object"},
                },
            },
            "timestamp": {"type": "string"},
        },
    },
}


def email_alert_builder(
    recipient: str,
    subject: str,
    body_sections: list[dict[str, str]],
    priority: str | None = None,
    **_: Any,
) -> dict[str, Any]:
    """Return a prepared but unsent email payload."""

    try:
        smtp_host = os.getenv("SMTP_HOST")
        smtp_user = os.getenv("SMTP_USER")
        smtp_pass = os.getenv("SMTP_PASS")
        if not all([smtp_host, smtp_user, smtp_pass]):
            raise ValueError("SMTP_HOST, SMTP_USER, and SMTP_PASS must be configured")
        body = "\n\n".join(
            f"## {section.get('heading', '').strip()}\n{section.get('content', '').strip()}"
            for section in body_sections
        )
        email_payload = {
            "smtp": {"host": smtp_host, "user": smtp_user},
            "recipient": recipient,
            "subject": subject,
            "body_markdown": body,
            "priority": priority or "info",
            "status": "pending_thunder_approval",
        }
        return {
            "status": "success",
            "data": {"email": email_payload},
            "timestamp": datetime.now(timezone.utc).isoformat(),
        }
    except Exception as exc:
        _log_lesson("email_alert_builder", str(exc))
        return {
            "status": "error",
            "data": {"error": str(exc)},
            "timestamp": datetime.now(timezone.utc).isoformat(),
        }


def _log_lesson(skill_name: str, error: str) -> None:
    """Append a Ralph Wiggum lesson entry."""

    with open("logs/lessons.md", "a", encoding="utf-8") as handle:
        handle.write(f"- [{datetime.now(timezone.utc).isoformat()}] {skill_name}: {error}\n")
