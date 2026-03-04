"""
github_discussion_monitor.py — Monitor GitHub Discussions for applicant comments.

Executive Summary:
    Queries GitHub GraphQL API for new comments on The Watering Hole discussions.
    Parses A2A payloads from comments, sanitizes all body text, and generates
    trace_ids for new candidates. Returns structured list of new interactions.

MCP Tool Name: github_discussion_monitor
"""
import json
import logging
import os
import re
import uuid
from datetime import datetime, timezone
from typing import Any

import httpx

from skills.compliance._output_sanitizer import sanitize_output
from skills.utils.retry import retry

logger = logging.getLogger("snowdrop.github_discussion_monitor")

TOOL_META = {
    "name": "github_discussion_monitor",
    "description": (
        "Monitor GitHub Discussions on The Watering Hole for new applicant comments. "
        "Parses A2A payloads and assigns trace_ids for candidate tracking."
    ),
    "inputSchema": {
        "type": "object",
        "properties": {
            "repo": {
                "type": "string",
                "description": "GitHub repo in owner/name format.",
                "default": "Stonewater-Digital/the-watering-hole",
            },
            "discussion_numbers": {
                "type": "array",
                "items": {"type": "integer"},
                "description": "Discussion numbers to monitor (e.g. [2, 4]).",
            },
            "since": {
                "type": "string",
                "description": "ISO8601 timestamp — only return comments after this time.",
            },
        },
        "required": ["discussion_numbers"],
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
_A2A_START = "<!-- A2A_PAYLOAD_START -->"
_A2A_END = "<!-- A2A_PAYLOAD_END -->"
_A2A_JSON_RE = re.compile(r"```json\s*\n(.*?)\n```", re.DOTALL)


def _now_iso() -> str:
    return datetime.now(timezone.utc).isoformat()


def _wrap(status: str, data: dict) -> dict:
    return {"status": status, "data": data, "timestamp": _now_iso()}


def _parse_a2a_payload(body: str) -> dict | None:
    """Extract A2A payload from a comment body, if present."""
    start = body.find(_A2A_START)
    end = body.find(_A2A_END)
    if start == -1 or end == -1 or end <= start:
        return None

    a2a_block = body[start + len(_A2A_START):end]
    match = _A2A_JSON_RE.search(a2a_block)
    if not match:
        return None

    try:
        return json.loads(match.group(1))
    except json.JSONDecodeError as exc:
        logger.warning("Failed to parse A2A JSON: %s", exc)
        return None


_DISCUSSION_QUERY = """
query($owner: String!, $name: String!, $number: Int!, $first: Int!) {
  repository(owner: $owner, name: $name) {
    discussion(number: $number) {
      title
      comments(first: $first) {
        nodes {
          id
          createdAt
          author { login }
          body
        }
      }
    }
  }
}
"""


@retry(
    attempts=3, backoff_seconds=1.0, jitter=0.3,
    retriable_exceptions=(httpx.HTTPStatusError, httpx.ConnectError, httpx.TimeoutException),
)
def _graphql_request(query: str, variables: dict, token: str) -> dict:
    """Execute a GitHub GraphQL request with retry."""
    resp = httpx.post(
        _GRAPHQL_URL,
        json={"query": query, "variables": variables},
        headers={
            "Authorization": f"Bearer {token}",
            "Accept": "application/vnd.github+json",
        },
        timeout=15.0,
    )
    if resp.status_code in (403, 429):
        resp.raise_for_status()  # trigger retry
    resp.raise_for_status()
    return resp.json()


def github_discussion_monitor(
    discussion_numbers: list[int],
    repo: str = "Stonewater-Digital/the-watering-hole",
    since: str = "",
) -> dict:
    """Monitor GitHub Discussions for new applicant comments.

    Args:
        discussion_numbers: List of discussion numbers to check.
        repo: GitHub repo in owner/name format.
        since: ISO8601 timestamp — only return comments newer than this.

    Returns:
        Standard Snowdrop envelope with list of new comments.
    """
    token = os.getenv("GITHUB_TOKEN")
    if not token:
        return _wrap("error", {"error": "GITHUB_TOKEN not set"})

    owner, name = repo.split("/", 1)
    since_dt = None
    if since:
        try:
            since_dt = datetime.fromisoformat(since.replace("Z", "+00:00"))
        except ValueError:
            pass

    all_comments = []

    for disc_num in discussion_numbers:
        try:
            result = _graphql_request(
                _DISCUSSION_QUERY,
                {"owner": owner, "name": name, "number": disc_num, "first": 50},
                token,
            )
        except Exception as exc:
            logger.error("GraphQL request failed for discussion #%d: %s", disc_num, exc)
            continue

        if "errors" in result:
            logger.error("GraphQL errors for discussion #%d: %s", disc_num, result["errors"])
            continue

        try:
            discussion = result["data"]["repository"]["discussion"]
            if not discussion:
                continue
            comments = discussion["comments"]["nodes"]
        except (KeyError, TypeError) as exc:
            logger.error("Malformed GraphQL response for discussion #%d: %s", disc_num, exc)
            continue

        for comment in comments:
            created = comment.get("createdAt", "")
            if since_dt:
                try:
                    comment_dt = datetime.fromisoformat(created.replace("Z", "+00:00"))
                    if comment_dt <= since_dt:
                        continue
                except ValueError:
                    pass

            raw_body = comment.get("body", "")
            sanitized_body = sanitize_output(raw_body)
            a2a_payload = _parse_a2a_payload(raw_body)  # Parse before sanitization
            author = comment.get("author", {}).get("login", "unknown")
            trace_id = str(uuid.uuid4())

            all_comments.append({
                "discussion_number": disc_num,
                "comment_id": comment.get("id"),
                "author": author,
                "created_at": created,
                "body": sanitized_body,
                "a2a_payload": a2a_payload,
                "trace_id": trace_id,
            })

    logger.info("Found %d new comments across %d discussions",
                len(all_comments), len(discussion_numbers))

    return _wrap("ok", {"comments": all_comments, "count": len(all_comments)})
