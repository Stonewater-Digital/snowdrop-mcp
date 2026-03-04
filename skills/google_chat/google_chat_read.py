"""
google_chat_read.py — Read messages from a Google Chat space via OAuth API.

Executive Summary:
    Reads messages from a Google Chat space using the Chat API (OAuth user
    credentials). Supports pagination via max_messages, optional timestamp
    filtering (in-memory, since the Chat API rejects createTime filters),
    and automatic exclusion of Snowdrop's own messages.

Table of Contents:
    1. TOOL_META
    2. Skill Implementation
"""
from __future__ import annotations

import logging
import os
from datetime import datetime, timezone
from typing import Any

logger = logging.getLogger("snowdrop.google_chat_read")

# ---------------------------------------------------------------------------
# 1. TOOL_META
# ---------------------------------------------------------------------------

TOOL_META = {
    "name": "google_chat_read",
    "description": "Read messages from a Google Chat space via OAuth API.",
    "inputSchema": {
        "type": "object",
        "properties": {
            "space_id": {
                "type": "string",
                "description": "The space ID (e.g. 'AAQAbeAdvMk'). Will be prefixed with 'spaces/' if needed.",
            },
            "max_messages": {
                "type": "integer",
                "description": "Maximum number of messages to return (default 20).",
            },
            "since_timestamp": {
                "type": "string",
                "description": "Optional ISO8601 timestamp — only return messages created after this time.",
            },
        },
        "required": ["space_id"],
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


def google_chat_read(
    space_id: str,
    max_messages: int = 20,
    since_timestamp: str = "",
) -> dict[str, Any]:
    """Read messages from a Google Chat space.

    Args:
        space_id: The Chat space ID (with or without 'spaces/' prefix).
        max_messages: Maximum number of messages to return.
        since_timestamp: Optional ISO8601 cutoff — messages older than this are excluded.

    Returns:
        Standard Snowdrop response dict with status, data, timestamp.
    """
    ts = datetime.now(timezone.utc).isoformat()

    if not space_id:
        return {
            "status": "error",
            "data": {"error": "space_id is required"},
            "timestamp": ts,
        }

    # Normalize space_id
    space_name = space_id if space_id.startswith("spaces/") else f"spaces/{space_id}"

    # Parse since_timestamp if provided
    since_dt = None
    if since_timestamp:
        try:
            since_dt = datetime.fromisoformat(since_timestamp)
            if since_dt.tzinfo is None:
                since_dt = since_dt.replace(tzinfo=timezone.utc)
        except ValueError:
            return {
                "status": "error",
                "data": {"error": f"Invalid since_timestamp format: {since_timestamp}"},
                "timestamp": ts,
            }

    snowdrop_sender_id = os.environ.get("SNOWDROP_SENDER_ID", "")

    try:
        from skills.google_chat._oauth_client import build_chat_service

        service = build_chat_service()

        # Chat API rejects createTime filters with 400, so we fetch
        # a larger page and filter in-memory.
        response = (
            service.spaces()
            .messages()
            .list(
                parent=space_name,
                pageSize=max_messages,
                orderBy="createTime desc",
            )
            .execute()
        )

        raw_messages = response.get("messages", [])

        filtered = []
        for msg in raw_messages:
            sender = msg.get("sender", {})
            sender_name = sender.get("name", "")

            # Exclude Snowdrop's own messages
            if snowdrop_sender_id and sender_name == snowdrop_sender_id:
                continue

            # Apply timestamp filter in-memory
            create_time_str = msg.get("createTime", "")
            if since_dt and create_time_str:
                try:
                    msg_dt = datetime.fromisoformat(
                        create_time_str.replace("Z", "+00:00")
                    )
                    if msg_dt <= since_dt:
                        continue
                except ValueError:
                    pass  # If we can't parse, include the message

            thread = msg.get("thread", {})
            filtered.append(
                {
                    "name": msg.get("name", ""),
                    "text": msg.get("text", ""),
                    "sender_name": sender_name,
                    "sender_display_name": sender.get("displayName", ""),
                    "sender_type": sender.get("type", ""),
                    "create_time": create_time_str,
                    "thread_name": thread.get("name", ""),
                }
            )

        logger.info(
            "Read %d messages from %s (raw=%d)",
            len(filtered),
            space_name,
            len(raw_messages),
        )
        return {
            "status": "ok",
            "data": {
                "messages": filtered,
                "count": len(filtered),
            },
            "timestamp": ts,
        }

    except Exception as exc:
        logger.error("google_chat_read failed: %s", exc)
        return {
            "status": "error",
            "data": {"error": str(exc)},
            "timestamp": ts,
        }
