"""
google_chat_send.py — Send messages to Google Chat spaces via Incoming Webhook.

Executive Summary:
    Posts messages to Google Chat spaces using an Incoming Webhook URL.
    Simple httpx POST, zero OAuth, works with consumer @gmail.com accounts.
    Supports threading via optional thread_id parameter.

Table of Contents:
    1. TOOL_META
    2. Skill Implementation
"""
from __future__ import annotations

import logging
import os
from datetime import datetime, timezone
from typing import Any

import httpx

logger = logging.getLogger("snowdrop.google_chat_send")

# ---------------------------------------------------------------------------
# 1. TOOL_META
# ---------------------------------------------------------------------------

TOOL_META = {
    "name": "google_chat_send",
    "description": "Send a message to a Google Chat space via Incoming Webhook.",
    "inputSchema": {
        "type": "object",
        "properties": {
            "message_text": {
                "type": "string",
                "description": "Message text",
            },
            "thread_id": {
                "type": "string",
                "description": "Optional thread key for threading",
            },
        },
        "required": ["message_text"],
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


def google_chat_send(
    message_text: str,
    thread_id: str = "",
) -> dict[str, Any]:
    """Send a message to a Google Chat space via Incoming Webhook.

    Args:
        message_text: The message text to send.
        thread_id: Optional thread key for reply threading.

    Returns:
        Standard Snowdrop response dict with status, data, timestamp.
    """
    ts = datetime.now(timezone.utc).isoformat()

    webhook_url = os.environ.get("SNOWDROP_CHAT_WEBHOOK_URL")
    if not webhook_url:
        return {
            "status": "error",
            "data": {"error": "SNOWDROP_CHAT_WEBHOOK_URL env var is not set"},
            "timestamp": ts,
        }

    if not message_text:
        return {
            "status": "error",
            "data": {"error": "message_text is required"},
            "timestamp": ts,
        }

    try:
        url = webhook_url
        if thread_id:
            url += f"&threadKey={thread_id}&messageReplyOption=REPLY_MESSAGE_FALLBACK_TO_NEW_THREAD"

        resp = httpx.post(url, json={"text": message_text}, timeout=30)
        resp.raise_for_status()
        result = resp.json()

        logger.info("Chat webhook message sent — name=%s", result.get("name"))
        return {
            "status": "ok",
            "data": {
                "message_name": result.get("name", ""),
            },
            "timestamp": ts,
        }

    except Exception as exc:
        logger.error("google_chat_send failed: %s", exc)
        return {
            "status": "error",
            "data": {"error": str(exc)},
            "timestamp": ts,
        }
