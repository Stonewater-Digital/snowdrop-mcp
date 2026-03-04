"""Route Telegram slash commands to Snowdrop actions."""
from __future__ import annotations

from datetime import datetime, timezone
from typing import Any

SUPPORTED_COMMANDS = {
    "balance": "show_balance",
    "audit": "run_audit",
    "brief": "send_briefing",
    "price": "quote_pricing",
    "status": "system_status",
    "help": "show_help",
}

TOOL_META: dict[str, Any] = {
    "name": "telegram_command_router",
    "description": "Parses Telegram commands (/balance, /audit, /brief, /price, /status, /help).",
    "inputSchema": {
        "type": "object",
        "properties": {
            "command_text": {"type": "string"},
            "chat_id": {"type": "string"},
        },
        "required": ["command_text", "chat_id"],
    },
    "outputSchema": {
        "type": "object",
        "properties": {
            "status": {"type": "string"},
            "data": {
                "type": "object",
                "properties": {
                    "intent": {"type": "string"},
                    "args": {"type": "array"},
                    "chat_id": {"type": "string"},
                },
            },
            "timestamp": {"type": "string"},
        },
    },
}


def telegram_command_router(command_text: str, chat_id: str, **_: Any) -> dict[str, Any]:
    """Convert Telegram commands into intents."""
    try:
        if not command_text.startswith("/"):
            raise ValueError("Telegram commands must start with '/'")
        tokens = [token for token in command_text.split() if token]
        command = tokens[0][1:].lower()
        args = tokens[1:]
        intent = SUPPORTED_COMMANDS.get(command)
        if not intent:
            intent = "unknown"
        data = {
            "chat_id": chat_id,
            "intent": intent,
            "args": args,
            "raw_command": command_text,
        }
        return {
            "status": "success",
            "data": data,
            "timestamp": datetime.now(timezone.utc).isoformat(),
        }
    except Exception as exc:
        _log_lesson("telegram_command_router", str(exc))
        return {
            "status": "error",
            "data": {"error": str(exc)},
            "timestamp": datetime.now(timezone.utc).isoformat(),
        }


def _log_lesson(skill_name: str, error: str) -> None:
    with open("logs/lessons.md", "a", encoding="utf-8") as handle:
        handle.write(f"- [{datetime.now(timezone.utc).isoformat()}] {skill_name}: {error}\n")
