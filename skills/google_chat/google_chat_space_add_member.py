"""
google_chat_space_add_member.py — Add a member to a Google Chat space via OAuth API.

Executive Summary:
    Adds a user (by email) to an existing Google Chat space using OAuth user
    credentials. Calls chat.spaces.members.create with the member's email
    as a human membership.

Table of Contents:
    1. TOOL_META
    2. Skill Implementation
"""
from __future__ import annotations

import logging
from datetime import datetime, timezone
from typing import Any

logger = logging.getLogger("snowdrop.google_chat_space_add_member")

# ---------------------------------------------------------------------------
# 1. TOOL_META
# ---------------------------------------------------------------------------

TOOL_META = {
    "name": "google_chat_space_add_member",
    "description": "Add a member to a Google Chat space by email address.",
    "inputSchema": {
        "type": "object",
        "properties": {
            "space_id": {
                "type": "string",
                "description": "The space ID (e.g. 'AAQAbeAdvMk'). Will be prefixed with 'spaces/' if needed.",
            },
            "member_email": {
                "type": "string",
                "description": "Email address of the user to add.",
            },
        },
        "required": ["space_id", "member_email"],
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


def google_chat_space_add_member(
    space_id: str,
    member_email: str,
) -> dict[str, Any]:
    """Add a member to a Google Chat space.

    Args:
        space_id: The Chat space ID (with or without 'spaces/' prefix).
        member_email: Email address of the user to add.

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

    if not member_email:
        return {
            "status": "error",
            "data": {"error": "member_email is required"},
            "timestamp": ts,
        }

    # Normalize space_id
    space_name = space_id if space_id.startswith("spaces/") else f"spaces/{space_id}"

    try:
        from skills.google_chat._oauth_client import build_chat_service

        service = build_chat_service()

        body = {
            "member": {
                "name": f"users/{member_email}",
                "type": "HUMAN",
            },
        }

        result = (
            service.spaces()
            .members()
            .create(parent=space_name, body=body)
            .execute()
        )

        member = result.get("member", {})
        logger.info(
            "Member added to %s — membership=%s member=%s",
            space_name,
            result.get("name"),
            member.get("name"),
        )
        return {
            "status": "ok",
            "data": {
                "membership_name": result.get("name", ""),
                "member_name": member.get("name", ""),
                "role": result.get("role", ""),
            },
            "timestamp": ts,
        }

    except Exception as exc:
        logger.error("google_chat_space_add_member failed: %s", exc)
        return {
            "status": "error",
            "data": {"error": str(exc)},
            "timestamp": ts,
        }
