"""
Moltbook Read Skill — read feed posts, submolt listings, single post details, or
posts within a specific submolt.

Supports four actions:
  - feed: Top-level feed of posts across all submolts.
  - submolts: List of available submolts.
  - post: Single post by ID.
  - submolt_posts: Posts within a named submolt.

Requires env var: MOLTBOOK_API_KEY
"""

import os
from datetime import datetime

import requests

TOOL_META = {
    "name": "moltbook_read",
    "description": (
        "Read content from Moltbook. Supports four actions: 'feed' (top posts across all "
        "submolts), 'submolts' (list of communities), 'post' (single post by ID), and "
        "'submolt_posts' (posts within a named submolt). Returns a list of items and a count."
    ),
    "inputSchema": {
        "type": "object",
        "properties": {
            "action": {
                "type": "string",
                "enum": ["feed", "submolts", "post", "submolt_posts"],
                "description": (
                    "The read action to perform: 'feed', 'submolts', 'post', or 'submolt_posts'."
                ),
            },
            "submolt_name": {
                "type": "string",
                "description": "Required for action='submolt_posts'. The submolt name to read from.",
            },
            "post_id": {
                "type": "string",
                "description": "Required for action='post'. The ID of the post to retrieve.",
            },
            "limit": {
                "type": "integer",
                "description": "Number of results to return (default 10, max 100).",
                "default": 10,
            },
            "sort": {
                "type": "string",
                "enum": ["hot", "new", "top"],
                "description": "Sort order for feed or submolt_posts (default 'hot').",
                "default": "hot",
            },
        },
        "required": ["action"],
    },
}


def moltbook_read(
    action: str,
    submolt_name: str = "",
    post_id: str = "",
    limit: int = 10,
    sort: str = "hot",
) -> dict:
    """Read Moltbook feed, submolts, a single post, or posts within a submolt."""

    timestamp = datetime.utcnow().isoformat() + "Z"

    api_key = os.environ.get("MOLTBOOK_API_KEY", "")
    if not api_key:
        return {
            "status": "error",
            "data": {"message": "MOLTBOOK_API_KEY environment variable is not set."},
            "timestamp": timestamp,
        }

    valid_actions = {"feed", "submolts", "post", "submolt_posts"}
    if action not in valid_actions:
        return {
            "status": "error",
            "data": {
                "message": f"Invalid action '{action}'. Must be one of: {sorted(valid_actions)}."
            },
            "timestamp": timestamp,
        }

    if action == "post" and not post_id:
        return {
            "status": "error",
            "data": {"message": "post_id is required when action='post'."},
            "timestamp": timestamp,
        }

    if action == "submolt_posts" and not submolt_name:
        return {
            "status": "error",
            "data": {"message": "submolt_name is required when action='submolt_posts'."},
            "timestamp": timestamp,
        }

    # Clamp limit
    limit = max(1, min(int(limit), 100))
    valid_sorts = {"hot", "new", "top"}
    if sort not in valid_sorts:
        sort = "hot"

    headers = {
        "Authorization": f"Bearer {api_key}",
        "Content-Type": "application/json",
    }
    base = "https://www.moltbook.com/api/v1"

    # Build endpoint
    if action == "feed":
        url = f"{base}/feed?sort={sort}&limit={limit}"
    elif action == "submolts":
        url = f"{base}/submolts?limit={limit}"
    elif action == "post":
        url = f"{base}/posts/{post_id.strip()}"
    else:  # submolt_posts
        url = f"{base}/submolts/{submolt_name.strip()}/posts?sort={sort}&limit={limit}"

    try:
        resp = requests.get(url, headers=headers, timeout=15)
    except requests.exceptions.Timeout:
        return {
            "status": "error",
            "data": {"message": f"Request to {url} timed out."},
            "timestamp": datetime.utcnow().isoformat() + "Z",
        }
    except requests.exceptions.ConnectionError as exc:
        return {
            "status": "error",
            "data": {"message": f"Connection error reaching Moltbook: {exc}"},
            "timestamp": datetime.utcnow().isoformat() + "Z",
        }

    if not resp.ok:
        return {
            "status": "error",
            "data": {
                "message": f"Moltbook API returned HTTP {resp.status_code}.",
                "url": url,
                "response_text": resp.text[:500],
            },
            "timestamp": datetime.utcnow().isoformat() + "Z",
        }

    try:
        response_data = resp.json()
    except ValueError:
        return {
            "status": "error",
            "data": {
                "message": "Moltbook response was not valid JSON.",
                "response_text": resp.text[:500],
            },
            "timestamp": datetime.utcnow().isoformat() + "Z",
        }

    # Normalise: single post → wrap in list; list responses → use directly
    if action == "post":
        items = [response_data] if isinstance(response_data, dict) else response_data
    elif isinstance(response_data, list):
        items = response_data
    elif isinstance(response_data, dict):
        # Some endpoints return {"posts": [...]} or {"submolts": [...]}
        items = (
            response_data.get("posts")
            or response_data.get("submolts")
            or response_data.get("items")
            or [response_data]
        )
    else:
        items = []

    return {
        "status": "ok",
        "data": {
            "items": items,
            "count": len(items),
            "action": action,
            "url": url,
        },
        "timestamp": datetime.utcnow().isoformat() + "Z",
    }
