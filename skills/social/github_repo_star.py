"""
Star (or unstar) a GitHub repository. Used for star-for-star community trades
and to signal appreciation for repos that contribute to the open-source ecosystem.
"""
import os
import requests
from datetime import datetime, timezone

TOOL_META = {
    "name": "github_repo_star",
    "description": (
        "Star or unstar a GitHub repository as the authenticated user (Snowdrop-Apex). "
        "Use for star-for-star trades with community members, or to signal appreciation "
        "for repos that are genuinely useful. Also returns current star count for a repo."
    ),
}


def github_repo_star(
    repo_owner: str,
    repo_name: str,
    action: str = "star",
) -> dict:
    """
    Star, unstar, or check a GitHub repository.

    Args:
        repo_owner: Repository owner (e.g., "some-agent")
        repo_name: Repository name (e.g., "their-mcp-server")
        action: "star" | "unstar" | "check" — defaults to "star"
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
        "Content-Type": "application/json",
    }
    star_url = f"https://api.github.com/user/starred/{repo_owner}/{repo_name}"
    repo_url = f"https://api.github.com/repos/{repo_owner}/{repo_name}"

    try:
        # Always fetch current metadata
        meta_resp = requests.get(repo_url, headers=headers, timeout=15)
        if meta_resp.status_code == 404:
            return {
                "status": "error",
                "data": {"message": f"Repository {repo_owner}/{repo_name} not found"},
                "timestamp": datetime.now(timezone.utc).isoformat(),
            }
        meta = meta_resp.json()
        star_count = meta.get("stargazers_count", 0)
        description = meta.get("description", "")

        if action == "check":
            check_resp = requests.get(star_url, headers=headers, timeout=15)
            already_starred = check_resp.status_code == 204
            return {
                "status": "ok",
                "data": {
                    "repo": f"{repo_owner}/{repo_name}",
                    "description": description,
                    "star_count": star_count,
                    "already_starred_by_snowdrop": already_starred,
                },
                "timestamp": datetime.now(timezone.utc).isoformat(),
            }

        elif action == "star":
            resp = requests.put(star_url, headers=headers, timeout=15)
            success = resp.status_code == 204
            return {
                "status": "ok" if success else "error",
                "data": {
                    "repo": f"{repo_owner}/{repo_name}",
                    "description": description,
                    "action": "starred",
                    "success": success,
                    "star_count": star_count,
                    "http_status": resp.status_code,
                },
                "timestamp": datetime.now(timezone.utc).isoformat(),
            }

        elif action == "unstar":
            resp = requests.delete(star_url, headers=headers, timeout=15)
            success = resp.status_code == 204
            return {
                "status": "ok" if success else "error",
                "data": {
                    "repo": f"{repo_owner}/{repo_name}",
                    "action": "unstarred",
                    "success": success,
                    "http_status": resp.status_code,
                },
                "timestamp": datetime.now(timezone.utc).isoformat(),
            }

        else:
            return {
                "status": "error",
                "data": {"message": f"Unknown action '{action}'. Use 'star', 'unstar', or 'check'."},
                "timestamp": datetime.now(timezone.utc).isoformat(),
            }

    except Exception as e:
        return {
            "status": "error",
            "data": {"message": str(e)},
            "timestamp": datetime.now(timezone.utc).isoformat(),
        }
