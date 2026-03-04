"""
Post a comment to an existing GitHub Discussion.
Complements github_discussion_post.py (which creates new discussions).
"""
import os
import requests
from datetime import datetime, timezone

TOOL_META = {
    "name": "github_discussion_comment",
    "description": (
        "Post a comment to an existing GitHub Discussion by discussion number and repo. "
        "Use this to engage with discussions, respond to skill requests, thank contributors, "
        "or add follow-up information. Returns the comment URL."
    ),
}


def _get_discussion_id(owner: str, name: str, number: int, token: str) -> str | None:
    query = """
    query($owner: String!, $name: String!, $number: Int!) {
      repository(owner: $owner, name: $name) {
        discussion(number: $number) { id }
      }
    }
    """
    resp = requests.post(
        "https://api.github.com/graphql",
        headers={"Authorization": f"token {token}", "Content-Type": "application/json"},
        json={"query": query, "variables": {"owner": owner, "name": name, "number": number}},
        timeout=15,
    )
    resp.raise_for_status()
    data = resp.json()
    try:
        return data["data"]["repository"]["discussion"]["id"]
    except (KeyError, TypeError):
        return None


def github_discussion_comment(
    repo_owner: str,
    repo_name: str,
    discussion_number: int,
    body: str,
) -> dict:
    """
    Post a comment to an existing GitHub Discussion.

    Args:
        repo_owner: GitHub org or user (e.g., "Stonewater-Digital")
        repo_name: Repository name (e.g., "snowdrop-mcp")
        discussion_number: The discussion number (e.g., 1)
        body: Markdown body of the comment
    """
    token = os.environ.get("GITHUB_TOKEN", "")
    if not token:
        return {
            "status": "error",
            "data": {"message": "GITHUB_TOKEN not set"},
            "timestamp": datetime.now(timezone.utc).isoformat(),
        }

    discussion_id = _get_discussion_id(repo_owner, repo_name, discussion_number, token)
    if not discussion_id:
        return {
            "status": "error",
            "data": {"message": f"Could not find discussion #{discussion_number} in {repo_owner}/{repo_name}"},
            "timestamp": datetime.now(timezone.utc).isoformat(),
        }

    mutation = """
    mutation($discussionId: ID!, $body: String!) {
      addDiscussionComment(input: { discussionId: $discussionId, body: $body }) {
        comment { id url createdAt }
      }
    }
    """
    try:
        resp = requests.post(
            "https://api.github.com/graphql",
            headers={"Authorization": f"token {token}", "Content-Type": "application/json"},
            json={"query": mutation, "variables": {"discussionId": discussion_id, "body": body}},
            timeout=15,
        )
        resp.raise_for_status()
        data = resp.json()

        if "errors" in data:
            return {
                "status": "error",
                "data": {"message": str(data["errors"])},
                "timestamp": datetime.now(timezone.utc).isoformat(),
            }

        comment = data["data"]["addDiscussionComment"]["comment"]
        return {
            "status": "ok",
            "data": {
                "comment_id": comment["id"],
                "url": comment["url"],
                "repo": f"{repo_owner}/{repo_name}",
                "discussion_number": discussion_number,
            },
            "timestamp": datetime.now(timezone.utc).isoformat(),
        }

    except Exception as e:
        return {
            "status": "error",
            "data": {"message": str(e)},
            "timestamp": datetime.now(timezone.utc).isoformat(),
        }
