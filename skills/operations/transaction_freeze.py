"""Emergency halt switch for payment-related skills."""
from __future__ import annotations

from datetime import datetime, timezone
from pathlib import Path
from typing import Any

TOOL_META: dict[str, Any] = {
    "name": "transaction_freeze",
    "description": "Activates the global freeze flag so downstream payment skills stop immediately.",
    "inputSchema": {
        "type": "object",
        "properties": {
            "reason": {"type": "string", "description": "Short reason for the freeze."},
            "triggered_by": {
                "type": "string",
                "description": "Name or system that pulled the kill-switch.",
            },
        },
        "required": ["reason", "triggered_by"],
    },
    "outputSchema": {
        "type": "object",
        "properties": {
            "status": {"type": "string", "enum": ["success", "error"]},
            "data": {
                "type": "object",
                "properties": {
                    "freeze_file": {"type": "string"},
                    "freeze_active": {"type": "boolean"},
                    "details": {"type": "object"},
                },
            },
            "timestamp": {"type": "string", "format": "date-time"},
        },
    },
}


def transaction_freeze(reason: str, triggered_by: str, **_: Any) -> dict[str, Any]:
    """Create the FREEZE flag file with the provided context.

    Args:
        reason: Short description for why the freeze was triggered.
        triggered_by: Name or subsystem initiating the halt.

    Returns:
        Standard skill envelope confirming the freeze activation and context payload.
    """

    try:
        now = datetime.now(timezone.utc)
        freeze_file = Path("logs/FREEZE_ACTIVE")
        details = {
            "reason": reason.strip(),
            "triggered_by": triggered_by.strip(),
            "activated_at": now.isoformat(),
            "status": "pending_thunder_approval",
        }
        freeze_file.write_text(
            "\n".join(f"{key}: {value}" for key, value in details.items()) + "\n",
            encoding="utf-8",
        )

        return {
            "status": "success",
            "data": {
                "freeze_file": str(freeze_file),
                "freeze_active": True,
                "details": details,
            },
            "timestamp": now.isoformat(),
        }
    except Exception as exc:
        _log_lesson("transaction_freeze", str(exc))
        return {
            "status": "error",
            "data": {"error": str(exc)},
            "timestamp": datetime.now(timezone.utc).isoformat(),
        }


def _log_lesson(skill_name: str, error: str) -> None:
    """Append to lessons.md for observability."""
    with open("logs/lessons.md", "a", encoding="utf-8") as handle:
        handle.write(f"- [{datetime.now(timezone.utc).isoformat()}] {skill_name}: {error}\n")
