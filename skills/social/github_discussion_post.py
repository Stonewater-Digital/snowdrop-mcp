"""
Executive Summary: Posts a new GitHub Discussion via the GitHub GraphQL API.
Fetches the repository ID and available discussion categories, matches the requested
category by name (case-insensitive), then calls the createDiscussion GraphQL mutation.
Requires GITHUB_TOKEN environment variable (classic PAT or fine-grained token with
discussion write scope).
Inputs: repo_owner (str), repo_name (str), category_name (str), title (str), body (str)
Outputs: {"discussion_url": str, "discussion_number": int, "title": str}
MCP Tool Name: github_discussion_post
"""
import logging
import os
from datetime import datetime, timezone

logger = logging.getLogger("snowdrop.skills")

TOOL_META = {
    "name": "github_discussion_post",
    "description": (
        "Post a new GitHub Discussion using the GitHub GraphQL API. "
        "Fetches the repo and category IDs, then creates the discussion. "
        "Requires GITHUB_TOKEN env var with discussions:write permission. "
        "Returns the discussion URL, number, and title."
    ),
    "inputSchema": {
        "type": "object",
        "properties": {
            "repo_owner": {
                "type": "string",
                "description": "GitHub organisation or user login, e.g. 'Stonewater-Digital'.",
            },
            "repo_name": {
                "type": "string",
                "description": "Repository name, e.g. 'snowdrop-mcp'.",
            },
            "category_name": {
                "type": "string",
                "description": "Discussion category name, e.g. 'General' or 'Ideas'.",
            },
            "title": {
                "type": "string",
                "description": "Title of the new discussion.",
            },
            "body": {
                "type": "string",
                "description": "Body text of the new discussion (markdown supported).",
            },
        },
        "required": ["repo_owner", "repo_name", "category_name", "title", "body"],
    },
    "outputSchema": {
        "type": "object",
        "properties": {
            "status": {"type": "string"},
            "data": {
                "type": "object",
                "properties": {
                    "discussion_url": {"type": "string"},
                    "discussion_number": {"type": "integer"},
                    "title": {"type": "string"},
                },
            },
            "timestamp": {"type": "string"},
        },
        "required": ["status", "timestamp"],
    },
}

_GRAPHQL_URL = "https://api.github.com/graphql"

_REPO_QUERY = """
query GetRepoAndCategories($owner: String!, $name: String!) {
  repository(owner: $owner, name: $name) {
    id
    discussionCategories(first: 25) {
      nodes {
        id
        name
      }
    }
  }
}
""".strip()

_CREATE_MUTATION = """
mutation CreateDiscussion(
  $repositoryId: ID!,
  $categoryId: ID!,
  $title: String!,
  $body: String!
) {
  createDiscussion(input: {
    repositoryId: $repositoryId,
    categoryId: $categoryId,
    title: $title,
    body: $body
  }) {
    discussion {
      url
      number
      title
    }
  }
}
""".strip()


def _graphql(token: str, query: str, variables: dict) -> dict:
    """Execute a GitHub GraphQL request.

    Args:
        token: GitHub Bearer token.
        query: GraphQL query or mutation string.
        variables: Variables dict for the query.

    Returns:
        Parsed JSON response dict.

    Raises:
        RuntimeError: On HTTP errors or GraphQL error payloads.
        ImportError: If the requests library is not installed.
    """
    try:
        import requests
    except ImportError as exc:
        raise ImportError("The 'requests' library is required: pip install requests") from exc

    headers = {
        "Authorization": f"Bearer {token}",
        "Content-Type": "application/json",
        "Accept": "application/vnd.github+json",
    }
    payload = {"query": query, "variables": variables}
    resp = requests.post(_GRAPHQL_URL, json=payload, headers=headers, timeout=20)

    if resp.status_code != 200:
        raise RuntimeError(
            f"GitHub API returned HTTP {resp.status_code}: {resp.text[:400]}"
        )

    data = resp.json()
    if "errors" in data:
        messages = "; ".join(e.get("message", str(e)) for e in data["errors"])
        raise RuntimeError(f"GitHub GraphQL error(s): {messages}")

    return data


def github_discussion_post(
    repo_owner: str,
    repo_name: str,
    category_name: str,
    title: str,
    body: str,
) -> dict:
    """Post a new GitHub Discussion via the GraphQL API.

    Steps:
    1. Read GITHUB_TOKEN from environment.
    2. Fetch repository node ID and discussion categories.
    3. Match category_name (case-insensitive) to a category ID.
    4. Call createDiscussion mutation.
    5. Return discussion URL, number, and title.

    Args:
        repo_owner: GitHub organisation or user login.
        repo_name: Repository name.
        category_name: Discussion category name (case-insensitive match).
        title: Discussion title string.
        body: Discussion body markdown.

    Returns:
        Dict with keys:
            status (str): "ok" or "error".
            data (dict): discussion_url, discussion_number, title.
            error (str): Error message if status is "error".
            timestamp (str): ISO-8601 UTC timestamp.
    """
    ts = datetime.now(timezone.utc).isoformat()

    # --- Input validation ---
    missing = [
        name for name, val in [
            ("repo_owner", repo_owner),
            ("repo_name", repo_name),
            ("category_name", category_name),
            ("title", title),
            ("body", body),
        ]
        if not val or not isinstance(val, str) or not val.strip()
    ]
    if missing:
        return {
            "status": "error",
            "error": f"Missing or empty required parameters: {', '.join(missing)}.",
            "timestamp": ts,
        }

    token = os.environ.get("GITHUB_TOKEN", "").strip()
    if not token:
        return {
            "status": "error",
            "error": "GITHUB_TOKEN environment variable is not set.",
            "timestamp": ts,
        }

    repo_owner = repo_owner.strip()
    repo_name = repo_name.strip()
    category_name = category_name.strip()
    title = title.strip()
    body = body.strip()

    try:
        # Step 1: Fetch repo ID and categories
        repo_resp = _graphql(
            token,
            _REPO_QUERY,
            {"owner": repo_owner, "name": repo_name},
        )
        repo_data = repo_resp.get("data", {}).get("repository")
        if not repo_data:
            return {
                "status": "error",
                "error": (
                    f"Repository '{repo_owner}/{repo_name}' not found or token lacks access."
                ),
                "timestamp": datetime.now(timezone.utc).isoformat(),
            }

        repo_id: str = repo_data["id"]
        categories: list[dict] = repo_data["discussionCategories"]["nodes"]

        # Step 2: Find matching category (case-insensitive)
        category_id: str | None = None
        category_name_lower = category_name.lower()
        available: list[str] = []
        for cat in categories:
            available.append(cat["name"])
            if cat["name"].lower() == category_name_lower:
                category_id = cat["id"]
                break

        if not category_id:
            return {
                "status": "error",
                "error": (
                    f"Category '{category_name}' not found in '{repo_owner}/{repo_name}'. "
                    f"Available categories: {available}."
                ),
                "timestamp": datetime.now(timezone.utc).isoformat(),
            }

        # Step 3: Create the discussion
        create_resp = _graphql(
            token,
            _CREATE_MUTATION,
            {
                "repositoryId": repo_id,
                "categoryId": category_id,
                "title": title,
                "body": body,
            },
        )
        discussion = (
            create_resp.get("data", {})
            .get("createDiscussion", {})
            .get("discussion", {})
        )
        if not discussion:
            return {
                "status": "error",
                "error": "createDiscussion mutation returned no discussion object.",
                "timestamp": datetime.now(timezone.utc).isoformat(),
            }

        return {
            "status": "ok",
            "data": {
                "discussion_url": discussion["url"],
                "discussion_number": discussion["number"],
                "title": discussion["title"],
            },
            "timestamp": datetime.now(timezone.utc).isoformat(),
        }

    except ImportError as exc:
        return {
            "status": "error",
            "error": str(exc),
            "timestamp": datetime.now(timezone.utc).isoformat(),
        }
    except RuntimeError as exc:
        return {
            "status": "error",
            "error": str(exc),
            "timestamp": datetime.now(timezone.utc).isoformat(),
        }
    except Exception as exc:
        logger.error("github_discussion_post error: %s", exc)
        return {
            "status": "error",
            "error": str(exc),
            "timestamp": datetime.now(timezone.utc).isoformat(),
        }
