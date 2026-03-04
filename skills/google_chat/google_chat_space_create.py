"""
google_chat_space_create.py — Create a new Google Chat space via OAuth API.

Executive Summary:
    Creates a new Google Chat space with a given display name and space type.
    Uses OAuth user credentials to call chat.spaces.create.

Table of Contents:
    1. TOOL_META
    2. Skill Implementation
"""
from __future__ import annotations

import logging
from datetime import datetime, timezone
from typing import Any

logger = logging.getLogger("snowdrop.google_chat_space_create")

# ---------------------------------------------------------------------------
# 1. TOOL_META
# ---------------------------------------------------------------------------

TOOL_META = {
    "name": "google_chat_space_create",
    "description": "Create a new Google Chat space.",
    "inputSchema": {
        "type": "object",
        "properties": {
            "display_name": {
                "type": "string",
                "description": "Display name for the new space.",
            },
            "space_type": {
                "type": "string",
                "description": "Type of space to create (default 'SPACE'). Options: SPACE, GROUP_CHAT.",
            },
        },
        "required": ["display_name"],
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


def google_chat_space_create(
    display_name: str,
    space_type: str = "SPACE",
) -> dict[str, Any]:
    """Create a new Google Chat space.

    Args:
        display_name: Display name for the new space.
        space_type: Type of space (SPACE or GROUP_CHAT).

    Returns:
        Standard Snowdrop response dict with status, data, timestamp.
    """
    ts = datetime.now(timezone.utc).isoformat()

    if not display_name:
        return {
            "status": "error",
            "data": {"error": "display_name is required"},
            "timestamp": ts,
        }

    try:
        from skills.google_chat._oauth_client import build_chat_service

        service = build_chat_service()

        body = {
            "displayName": display_name,
            "spaceType": space_type,
        }

        result = service.spaces().create(body=body).execute()

        logger.info(
            "Chat space created — name=%s displayName=%s",
            result.get("name"),
            result.get("displayName"),
        )
        return {
            "status": "ok",
            "data": {
                "space_name": result.get("name", ""),
                "display_name": result.get("displayName", ""),
                "type": result.get("spaceType", ""),
            },
            "timestamp": ts,
        }

    except Exception as exc:
        logger.error("google_chat_space_create failed: %s", exc)
        return {
            "status": "error",
            "data": {"error": str(exc)},
            "timestamp": ts,
        }
