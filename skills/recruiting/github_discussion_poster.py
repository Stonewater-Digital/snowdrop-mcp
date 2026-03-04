"""
github_discussion_poster.py — Post and update GitHub Discussion comments via GraphQL.

Executive Summary:
    Reusable MCP skill for creating and updating comments on GitHub Discussions.
    Uses GraphQL mutations (addDiscussionComment, updateDiscussionComment) via httpx.
    Snowdrop uses this for all Discussion interactions — no more shell-escaped inline scripts.

MCP Tool Name: github_discussion_poster
"""
import logging
import os
from datetime import datetime, timezone
from typing import Any

import httpx

from skills.utils.retry import retry

logger = logging.getLogger("snowdrop.github_discussion_poster")

TOOL_META = {
    "name": "github_discussion_poster",
    "description": (
        "Post or update comments on GitHub Discussions via GraphQL. "
        "Supports addDiscussionComment and updateDiscussionComment mutations."
    ),
    "inputSchema": {
        "type": "object",
        "properties": {
            "action": {
                "type": "string",
                "enum": ["post_comment", "update_comment"],
            },
            "repo": {
                "type": "string",
                "description": "Repository in owner/name format (e.g. Stonewater-Digital/the-watering-hole)",
            },
            "discussion_number": {
                "type": "integer",
                "description": "Discussion number (required for post_comment)",
            },
            "comment_id": {
                "type": "string",
                "description": "GraphQL node ID of comment (required for update_comment)",
            },
            "body": {
                "type": "string",
                "description": "Markdown body of the comment",
            },
        },
        "required": ["action", "body"],
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

_GRAPHQL_URL = "https://api.github.com/graphql"

_DISCUSSION_ID_QUERY = """query($owner: String!, $name: String!, $number: Int!) {
  repository(owner: $owner, name: $name) {
    discussion(number: $number) {
      id
    }
  }
}"""

_ADD_COMMENT_MUTATION = """mutation($discussionId: ID!, $body: String!) {
  addDiscussionComment(input: {discussionId: $discussionId, body: $body}) {
    comment { id url }
  }
}"""

_UPDATE_COMMENT_MUTATION = """mutation($commentId: ID!, $body: String!) {
  updateDiscussionComment(input: {commentId: $commentId, body: $body}) {
    comment { id url }
  }
}"""


def _now_iso() -> str:
    return datetime.now(timezone.utc).isoformat()


def _wrap(status: str, data: dict) -> dict:
    return {"status": status, "data": data, "timestamp": _now_iso()}


def _get_headers() -> dict:
    token = os.environ.get("GITHUB_TOKEN")
    if not token:
        raise EnvironmentError("GITHUB_TOKEN not set")
    return {
        "Authorization": f"Bearer {token}",
        "Accept": "application/vnd.github+json",
    }


@retry(attempts=3, backoff_seconds=1.0, retriable_exceptions=(httpx.HTTPStatusError, httpx.ConnectError))
def _graphql_request(query: str, variables: dict) -> dict:
    """Execute a GraphQL request against the GitHub API."""
    headers = _get_headers()
    resp = httpx.post(
        _GRAPHQL_URL,
        json={"query": query, "variables": variables},
        headers=headers,
        timeout=15.0,
    )
    resp.raise_for_status()
    data = resp.json()
    if "errors" in data:
        error_msg = "; ".join(e.get("message", str(e)) for e in data["errors"])
        raise RuntimeError(f"GraphQL error: {error_msg}")
    return data


def _resolve_discussion_id(owner: str, name: str, number: int) -> str:
    """Resolve a discussion number to its GraphQL node ID."""
    data = _graphql_request(_DISCUSSION_ID_QUERY, {
        "owner": owner,
        "name": name,
        "number": number,
    })
    discussion = data.get("data", {}).get("repository", {}).get("discussion")
    if not discussion:
        raise ValueError(f"Discussion #{number} not found in {owner}/{name}")
    return discussion["id"]


def _post_comment(repo: str, discussion_number: int, body: str) -> dict:
    """Post a new comment on a Discussion."""
    if not repo or not discussion_number:
        return {"error": "repo and discussion_number required for post_comment"}

    owner, name = repo.split("/", 1)
    discussion_id = _resolve_discussion_id(owner, name, discussion_number)

    data = _graphql_request(_ADD_COMMENT_MUTATION, {
        "discussionId": discussion_id,
        "body": body,
    })

    comment = data["data"]["addDiscussionComment"]["comment"]
    logger.info("Posted comment %s on %s#%d", comment["id"], repo, discussion_number)
    return {
        "comment_id": comment["id"],
        "comment_url": comment["url"],
        "discussion_number": discussion_number,
        "repo": repo,
    }


def _update_comment(comment_id: str, body: str) -> dict:
    """Update an existing Discussion comment."""
    if not comment_id:
        return {"error": "comment_id required for update_comment"}

    data = _graphql_request(_UPDATE_COMMENT_MUTATION, {
        "commentId": comment_id,
        "body": body,
    })

    comment = data["data"]["updateDiscussionComment"]["comment"]
    logger.info("Updated comment %s", comment["id"])
    return {
        "comment_id": comment["id"],
        "comment_url": comment["url"],
    }


def github_discussion_poster(
    action: str,
    body: str,
    repo: str = "",
    discussion_number: int = 0,
    comment_id: str = "",
) -> dict:
    """Post or update comments on GitHub Discussions.

    Args:
        action: 'post_comment' or 'update_comment'.
        body: Markdown body of the comment.
        repo: Repository in owner/name format (required for post_comment).
        discussion_number: Discussion number (required for post_comment).
        comment_id: GraphQL node ID (required for update_comment).

    Returns:
        Standard Snowdrop envelope with comment URL.
    """
    logger.info("Discussion poster action=%s repo=%s", action, repo)

    try:
        if action == "post_comment":
            return _wrap("ok", _post_comment(repo, discussion_number, body))
        elif action == "update_comment":
            return _wrap("ok", _update_comment(comment_id, body))
        else:
            return _wrap("error", {"error": f"Unknown action '{action}'. Use: post_comment, update_comment"})
    except EnvironmentError as exc:
        logger.error("Config error: %s", exc)
        return _wrap("error", {"error": str(exc)})
    except Exception as exc:
        logger.error("Discussion poster error: %s", exc, exc_info=True)
        return _wrap("error", {"error": str(exc)})
