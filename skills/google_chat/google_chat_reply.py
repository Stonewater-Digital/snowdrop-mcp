"""
google_chat_reply.py — Send a message or threaded reply to a Google Chat space via OAuth API.

Executive Summary:
    Sends messages to a Google Chat space using OAuth user credentials (NOT
    webhook). Supports threaded replies by passing thread_name with
    REPLY_MESSAGE_FALLBACK_TO_NEW_THREAD reply option.

Table of Contents:
    1. TOOL_META
    2. Skill Implementation
"""
from __future__ import annotations

import logging
from datetime import datetime, timezone
from typing import Any

logger = logging.getLogger("snowdrop.google_chat_reply")

# ---------------------------------------------------------------------------
# 1. TOOL_META
# ---------------------------------------------------------------------------

TOOL_META = {
    "name": "google_chat_reply",
    "description": "Send a message or threaded reply to a Google Chat space via OAuth API.",
    "inputSchema": {
        "type": "object",
        "properties": {
            "space_id": {
                "type": "string",
                "description": "The space ID (e.g. 'AAQAbeAdvMk'). Will be prefixed with 'spaces/' if needed.",
            },
            "message_text": {
                "type": "string",
                "description": "The message text to send.",
            },
            "thread_name": {
                "type": "string",
                "description": "Optional thread resource name for threaded replies (e.g. 'spaces/AAQAbeAdvMk/threads/abc123').",
            },
        },
        "required": ["space_id", "message_text"],
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

# ---------------------------------------------------------------------------
# 2. Skill Implementation
# ---------------------------------------------------------------------------


def google_chat_reply(
    space_id: str,
    message_text: str,
    thread_name: str = "",
) -> dict[str, Any]:
    """Send a message or threaded reply to a Google Chat space.

    Args:
        space_id: The Chat space ID (with or without 'spaces/' prefix).
        message_text: The message text to send.
        thread_name: Optional thread resource name for threaded replies.

    Returns:
        Standard Snowdrop response dict with status, data, timestamp.
    """
    ts = datetime.now(timezone.utc).isoformat()

    if not message_text:
        return {
            "status": "error",
            "data": {"error": "message_text is required"},
            "timestamp": ts,
        }

    if not space_id:
        return {
            "status": "error",
            "data": {"error": "space_id is required"},
            "timestamp": ts,
        }

    # Normalize space_id
    space_name = space_id if space_id.startswith("spaces/") else f"spaces/{space_id}"

    try:
        from skills.google_chat._oauth_client import build_chat_service

        service = build_chat_service()

        body: dict[str, Any] = {"text": message_text}

        # Build request kwargs
        kwargs: dict[str, Any] = {
            "parent": space_name,
            "body": body,
        }

        if thread_name:
            body["thread"] = {"name": thread_name}
            kwargs["messageReplyOption"] = "REPLY_MESSAGE_FALLBACK_TO_NEW_THREAD"

        result = service.spaces().messages().create(**kwargs).execute()

        result_thread = result.get("thread", {})
        logger.info(
            "Chat message sent — name=%s thread=%s",
            result.get("name"),
            result_thread.get("name"),
        )
        return {
            "status": "ok",
            "data": {
                "message_name": result.get("name", ""),
                "thread_name": result_thread.get("name", ""),
                "create_time": result.get("createTime", ""),
            },
            "timestamp": ts,
        }

    except Exception as exc:
        logger.error("google_chat_reply failed: %s", exc)
        return {
            "status": "error",
            "data": {"error": str(exc)},
            "timestamp": ts,
        }
