"""
google_chat_list_spaces.py — List Google Chat spaces accessible to the authenticated user.

Executive Summary:
    Lists all Google Chat spaces the OAuth-authenticated user belongs to.
    Returns space name, display name, type, and space_type for each space.

Table of Contents:
    1. TOOL_META
    2. Skill Implementation
"""
from __future__ import annotations

import logging
from datetime import datetime, timezone
from typing import Any

logger = logging.getLogger("snowdrop.google_chat_list_spaces")

# ---------------------------------------------------------------------------
# 1. TOOL_META
# ---------------------------------------------------------------------------

TOOL_META = {
    "name": "google_chat_list_spaces",
    "description": "List Google Chat spaces accessible to the authenticated user.",
    "inputSchema": {
        "type": "object",
        "properties": {},
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


def google_chat_list_spaces() -> dict[str, Any]:
    """List all Google Chat spaces accessible to the authenticated user.

    Returns:
        Standard Snowdrop response dict with status, data, timestamp.
    """
    ts = datetime.now(timezone.utc).isoformat()

    try:
        from skills.google_chat._oauth_client import build_chat_service

        service = build_chat_service()

        response = service.spaces().list().execute()
        raw_spaces = response.get("spaces", [])

        spaces = [
            {
                "name": space.get("name", ""),
                "display_name": space.get("displayName", ""),
                "type": space.get("type", ""),
                "space_type": space.get("spaceType", ""),
            }
            for space in raw_spaces
        ]

        logger.info("Listed %d Chat spaces", len(spaces))
        return {
            "status": "ok",
            "data": {
                "spaces": spaces,
                "count": len(spaces),
            },
            "timestamp": ts,
        }

    except Exception as exc:
        logger.error("google_chat_list_spaces failed: %s", exc)
        return {
            "status": "error",
            "data": {"error": str(exc)},
            "timestamp": ts,
        }
