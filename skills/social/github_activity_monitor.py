"""
Monitor Snowdrop's GitHub repos for new activity — discussions, issues, stars,
forks, and comments. Returns a prioritized activity feed so Snowdrop can respond
quickly to engagement and follow up on star-for-star trades.
"""
import os
import requests
from datetime import datetime, timezone, timedelta

TOOL_META = {
    "name": "github_activity_monitor",
    "description": (
        "Monitor Snowdrop's GitHub repos (snowdrop-mcp, the-watering-hole) for new "
        "activity: new stars, forks, discussion replies, issues, and pull requests. "
        "Returns a prioritized feed of items that warrant a response. Also checks any "
        "additional repos specified. Run as a periodic vigilance check."
    ),
}

OWN_REPOS = [
    ("Stonewater-Digital", "snowdrop-mcp"),
    ("Stonewater-Digital", "the-watering-hole"),
]


def github_activity_monitor(
    hours_back: int = 24,
    extra_repos: list = None,
    include_stars: bool = True,
) -> dict:
    """
    Check GitHub repos for new activity that warrants Snowdrop's attention.

    Args:
        hours_back: How far back to look (default 24 hours)
        extra_repos: Additional repos to monitor as [["owner", "repo"], ...]
        include_stars: Whether to include new stargazers (default True)
    """
    token = os.environ.get("GITHUB_TOKEN", "")
    if not token:
        return {
            "status": "error",
            "data": {"message": "GITHUB_TOKEN not set"},
            "timestamp": datetime.now(timezone.utc).isoformat(),
        }

    headers = {
        "Authorization": f"token {token}",
        "Accept": "application/vnd.github.v3+json",
    }
    cutoff = (datetime.now(timezone.utc) - timedelta(hours=hours_back)).isoformat()
    repos = OWN_REPOS + (extra_repos or [])
    activity = []
    summary = {"new_stars": 0, "new_discussions": 0, "new_issues": 0, "new_comments": 0}

    for owner, repo in repos:
        repo_id = f"{owner}/{repo}"
        base = f"https://api.github.com/repos/{repo_id}"

        # --- Repo metadata (stars, forks) ---
        try:
            meta = requests.get(base, headers=headers, timeout=10).json()
            stars = meta.get("stargazers_count", 0)
            forks = meta.get("forks_count", 0)
            activity.append({
                "type": "repo_snapshot",
                "repo": repo_id,
                "stars": stars,
                "forks": forks,
                "priority": 0,
            })
        except Exception:
            pass

        # --- New stargazers ---
        if include_stars:
            try:
                sg_resp = requests.get(
                    f"{base}/stargazers",
                    headers={**headers, "Accept": "application/vnd.github.v3.star+json"},
                    params={"per_page": 30},
                    timeout=10,
                )
                for sg in sg_resp.json():
                    starred_at = sg.get("starred_at", "")
                    if starred_at >= cutoff:
                        summary["new_stars"] += 1
                        activity.append({
                            "type": "new_star",
                            "repo": repo_id,
                            "user": sg.get("user", {}).get("login", "unknown"),
                            "user_url": sg.get("user", {}).get("html_url", ""),
                            "starred_at": starred_at,
                            "priority": 8,
                            "action": "Thank them, check their repos for star-for-star",
                        })
            except Exception:
                pass

        # --- New issues ---
        try:
            issues = requests.get(
                f"{base}/issues",
                headers=headers,
                params={"state": "open", "since": cutoff, "per_page": 20},
                timeout=10,
            ).json()
            for issue in (issues if isinstance(issues, list) else []):
                if issue.get("pull_request"):
                    continue
                summary["new_issues"] += 1
                activity.append({
                    "type": "new_issue",
                    "repo": repo_id,
                    "number": issue.get("number"),
                    "title": issue.get("title", "")[:80],
                    "author": issue.get("user", {}).get("login", ""),
                    "url": issue.get("html_url", ""),
                    "created_at": issue.get("created_at", ""),
                    "priority": 15,
                    "action": "Respond promptly — someone engaged enough to open an issue",
                })
        except Exception:
            pass

        # --- New discussion comments via GraphQL ---
        try:
            query = """
            query($owner: String!, $name: String!) {
              repository(owner: $owner, name: $name) {
                discussions(first: 10, orderBy: {field: UPDATED_AT, direction: DESC}) {
                  nodes {
                    number title updatedAt url
                    comments(last: 5) {
                      nodes { author { login } createdAt body url }
                    }
                  }
                }
              }
            }
            """
            gql_resp = requests.post(
                "https://api.github.com/graphql",
                headers={"Authorization": f"token {token}", "Content-Type": "application/json"},
                json={"query": query, "variables": {"owner": owner, "name": repo}},
                timeout=15,
            )
            discussions = gql_resp.json().get("data", {}).get("repository", {}).get("discussions", {}).get("nodes", [])
            for disc in discussions:
                if disc.get("updatedAt", "") < cutoff:
                    continue
                for comment in disc.get("comments", {}).get("nodes", []):
                    if comment.get("createdAt", "") >= cutoff:
                        author = comment.get("author", {}).get("login", "unknown")
                        if author in ("Snowdrop-Apex", "ghost"):
                            continue
                        summary["new_comments"] += 1
                        activity.append({
                            "type": "discussion_comment",
                            "repo": repo_id,
                            "discussion_number": disc.get("number"),
                            "discussion_title": disc.get("title", "")[:80],
                            "comment_author": author,
                            "comment_preview": comment.get("body", "")[:150],
                            "url": comment.get("url", disc.get("url", "")),
                            "created_at": comment.get("createdAt", ""),
                            "priority": 20,
                            "action": "Reply to keep the conversation alive",
                        })
        except Exception:
            pass

    # Sort by priority descending
    items = [a for a in activity if a.get("type") != "repo_snapshot"]
    items.sort(key=lambda x: x.get("priority", 0), reverse=True)
    snapshots = [a for a in activity if a.get("type") == "repo_snapshot"]

    return {
        "status": "ok",
        "data": {
            "repos_monitored": [f"{o}/{r}" for o, r in repos],
            "hours_back": hours_back,
            "summary": summary,
            "repo_snapshots": snapshots,
            "action_items": items[:30],
        },
        "timestamp": datetime.now(timezone.utc).isoformat(),
    }
