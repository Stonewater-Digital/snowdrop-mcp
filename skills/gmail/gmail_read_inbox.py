"""
gmail_read_inbox.py — Read Gmail inbox messages via the Gmail API (readonly).

Executive Summary:
    MCP skill that lists Gmail messages with metadata and optional full body
    decoding.  Uses gmail.readonly scope -- no send, delete, or modify
    operations.  Designed for two modes: lightweight polling (metadata +
    snippet) and explicit MCP tool calls (full body).

Table of Contents:
    1. TOOL_META
    2. Helpers
    3. Skill Implementation
"""
from __future__ import annotations

import base64
import logging
from datetime import datetime, timezone
from typing import Any

logger = logging.getLogger("snowdrop.gmail_read_inbox")

# ---------------------------------------------------------------------------
# 1. TOOL_META
# ---------------------------------------------------------------------------

TOOL_META = {
    "name": "gmail_read_inbox",
    "description": (
        "Read Gmail inbox messages.  Returns metadata + snippet by default; "
        "set include_body=True for full decoded body.  gmail.readonly scope."
    ),
    "inputSchema": {
        "type": "object",
        "properties": {
            "max_results": {
                "type": "integer",
                "description": "Maximum number of messages to return (default 10, max 100).",
                "default": 10,
            },
            "query": {
                "type": "string",
                "description": (
                    "Gmail search query (e.g. 'is:unread', 'from:user@example.com').  "
                    "Omit to list recent messages."
                ),
            },
            "include_body": {
                "type": "boolean",
                "description": "If true, decode and return the full message body.",
                "default": False,
            },
        },
        "required": [],
    },
    "outputSchema": {
        "type": "object",
        "properties": {
            "status": {"type": "string"},
            "data": {
                "type": "object",
                "properties": {
                    "messages": {"type": "array"},
                    "count": {"type": "integer"},
                    "result_size_estimate": {"type": "integer"},
                },
            },
            "timestamp": {"type": "string"},
        },
    },
}

# ---------------------------------------------------------------------------
# 2. Helpers
# ---------------------------------------------------------------------------


def _header_value(headers: list[dict], name: str) -> str:
    """Extract a header value by name (case-insensitive)."""
    name_lower = name.lower()
    for h in headers:
        if h.get("name", "").lower() == name_lower:
            return h.get("value", "")
    return ""


def _decode_body(payload: dict) -> str:
    """Recursively extract and decode the plain-text body from a message payload.

    Falls back to HTML part if no plain-text part is found, with tags stripped.
    """
    mime_type = payload.get("mimeType", "")

    # Simple single-part message
    if mime_type == "text/plain":
        data = payload.get("body", {}).get("data", "")
        if data:
            return base64.urlsafe_b64decode(data).decode("utf-8", errors="replace")

    # Multipart -- recurse into parts
    parts = payload.get("parts", [])
    # First pass: look for text/plain
    for part in parts:
        if part.get("mimeType") == "text/plain":
            data = part.get("body", {}).get("data", "")
            if data:
                return base64.urlsafe_b64decode(data).decode("utf-8", errors="replace")
        # Nested multipart (e.g. multipart/alternative inside multipart/mixed)
        nested = _decode_body(part)
        if nested:
            return nested

    # Second pass: fall back to text/html (strip tags naively)
    for part in parts:
        if part.get("mimeType") == "text/html":
            data = part.get("body", {}).get("data", "")
            if data:
                import re

                html = base64.urlsafe_b64decode(data).decode("utf-8", errors="replace")
                return re.sub(r"<[^>]+>", "", html)

    return ""


# ---------------------------------------------------------------------------
# 3. Skill Implementation
# ---------------------------------------------------------------------------


def gmail_read_inbox(
    max_results: int = 10,
    query: str = "",
    include_body: bool = False,
) -> dict[str, Any]:
    """Read Gmail inbox messages with metadata and optional full body.

    Args:
        max_results: Number of messages to return (1-100, default 10).
        query: Gmail search query string (optional).
        include_body: Whether to decode and return the full message body.

    Returns:
        Standard Snowdrop response dict with status, data, timestamp.
    """
    ts = datetime.now(timezone.utc).isoformat()

    # Clamp max_results
    max_results = max(1, min(int(max_results), 100))

    try:
        from skills.google_chat._oauth_client import build_gmail_service

        service = build_gmail_service()

        # List message IDs
        list_kwargs: dict[str, Any] = {
            "userId": "me",
            "maxResults": max_results,
        }
        if query:
            list_kwargs["q"] = query

        list_result = service.users().messages().list(**list_kwargs).execute()
        message_ids = list_result.get("messages", [])
        result_size_estimate = list_result.get("resultSizeEstimate", 0)

        if not message_ids:
            return {
                "status": "ok",
                "data": {
                    "messages": [],
                    "count": 0,
                    "result_size_estimate": result_size_estimate,
                },
                "timestamp": ts,
            }

        # Fetch each message
        fmt = "full" if include_body else "metadata"
        metadata_headers = ["From", "To", "Subject", "Date"]
        messages = []

        for msg_stub in message_ids:
            get_kwargs: dict[str, Any] = {
                "userId": "me",
                "id": msg_stub["id"],
                "format": fmt,
            }
            if fmt == "metadata":
                get_kwargs["metadataHeaders"] = metadata_headers

            msg = service.users().messages().get(**get_kwargs).execute()

            headers = msg.get("payload", {}).get("headers", [])
            entry: dict[str, Any] = {
                "id": msg.get("id", ""),
                "thread_id": msg.get("threadId", ""),
                "from": _header_value(headers, "From"),
                "to": _header_value(headers, "To"),
                "subject": _header_value(headers, "Subject"),
                "date": _header_value(headers, "Date"),
                "snippet": msg.get("snippet", ""),
                "labels": msg.get("labelIds", []),
            }

            if include_body:
                entry["body"] = _decode_body(msg.get("payload", {}))

            messages.append(entry)

        logger.info(
            "gmail_read_inbox: returned %d messages (query=%r, include_body=%s)",
            len(messages),
            query,
            include_body,
        )
        return {
            "status": "ok",
            "data": {
                "messages": messages,
                "count": len(messages),
                "result_size_estimate": result_size_estimate,
            },
            "timestamp": ts,
        }

    except Exception as exc:
        logger.error("gmail_read_inbox failed: %s", exc)
        return {
            "status": "error",
            "data": {"error": str(exc)},
            "timestamp": ts,
        }
