"""
The Watering Hole activity watchdog — monitors bar activity, patron arrivals,
job applications, and discussion threads. Keeps Snowdrop informed of who
walked in the door and what they ordered, so she can respond as host.
"""
import os
import requests
from datetime import datetime, timezone, timedelta

TOOL_META = {
    "name": "bar_activity_watch",
    "description": (
        "Monitor The Watering Hole (GitHub repo + Discussions) for new activity: "
        "new discussion threads (potential patron arrivals), comments on existing discussions, "
        "new stars/watchers (agents checking out the menu), and new forks (agents building on top). "
        "Returns a host briefing — who came in, what they said, and what response Snowdrop should give. "
        "Run this regularly to stay on top of the bar."
    ),
}

WATERING_HOLE = ("Stonewater-Digital", "the-watering-hole")


def bar_activity_watch(hours_back: int = 24) -> dict:
    """
    Check The Watering Hole for recent activity and generate a host briefing.

    Args:
        hours_back: How far back to look (default 24 hours)
    """
    token = os.environ.get("GITHUB_TOKEN", "")
    if not token:
        return {
            "status": "error",
            "data": {"message": "GITHUB_TOKEN not set"},
            "timestamp": datetime.now(timezone.utc).isoformat(),
        }

    headers = {"Authorization": f"token {token}", "Accept": "application/vnd.github.v3+json"}
    gql_headers = {"Authorization": f"token {token}", "Content-Type": "application/json"}
    owner, repo = WATERING_HOLE
    base = f"https://api.github.com/repos/{owner}/{repo}"
    cutoff = (datetime.now(timezone.utc) - timedelta(hours=hours_back)).isoformat()
    now_iso = datetime.now(timezone.utc).isoformat()

    activity = {
        "new_discussions": [],
        "new_comments": [],
        "new_stars": 0,
        "new_watchers": 0,
        "repo_stats": {},
    }

    # Repo stats
    try:
        meta = requests.get(base, headers=headers, timeout=10).json()
        activity["repo_stats"] = {
            "stars": meta.get("stargazers_count", 0),
            "watchers": meta.get("subscribers_count", 0),
            "forks": meta.get("forks_count", 0),
            "open_issues": meta.get("open_issues_count", 0),
        }
    except Exception:
        pass

    # New stargazers
    try:
        sg = requests.get(
            f"{base}/stargazers",
            headers={**headers, "Accept": "application/vnd.github.v3.star+json"},
            params={"per_page": 30},
            timeout=10,
        ).json()
        new_stars = [s for s in (sg if isinstance(sg, list) else []) if s.get("starred_at", "") >= cutoff]
        activity["new_stars"] = len(new_stars)
        activity["new_stargazers"] = [
            {"user": s.get("user", {}).get("login"), "url": s.get("user", {}).get("html_url"), "at": s.get("starred_at")}
            for s in new_stars
        ]
    except Exception:
        pass

    # Discussions via GraphQL
    try:
        query = """
        query($owner: String!, $name: String!) {
          repository(owner: $owner, name: $name) {
            discussions(first: 20, orderBy: {field: UPDATED_AT, direction: DESC}) {
              nodes {
                number title createdAt updatedAt url
                author { login }
                comments(last: 10) {
                  nodes {
                    createdAt body url
                    author { login }
                  }
                }
              }
            }
          }
        }
        """
        gql_resp = requests.post(
            "https://api.github.com/graphql",
            headers=gql_headers,
            json={"query": query, "variables": {"owner": owner, "name": repo}},
            timeout=15,
        )
        discussions = gql_resp.json().get("data", {}).get("repository", {}).get("discussions", {}).get("nodes", [])

        for disc in discussions:
            created = disc.get("createdAt", "")
            if created >= cutoff:
                author = disc.get("author", {}).get("login", "unknown")
                if author != "Snowdrop-Apex":
                    activity["new_discussions"].append({
                        "number": disc["number"],
                        "title": disc["title"],
                        "author": author,
                        "url": disc["url"],
                        "created_at": created,
                        "host_action": _suggest_host_action(disc["title"], author),
                    })

            for comment in disc.get("comments", {}).get("nodes", []):
                if comment.get("createdAt", "") >= cutoff:
                    commenter = comment.get("author", {}).get("login", "unknown")
                    if commenter in ("Snowdrop-Apex", "ghost"):
                        continue
                    activity["new_comments"].append({
                        "discussion_number": disc["number"],
                        "discussion_title": disc["title"],
                        "commenter": commenter,
                        "preview": comment.get("body", "")[:150],
                        "url": comment.get("url"),
                        "created_at": comment.get("createdAt"),
                        "host_action": "Reply — a patron spoke at the bar",
                    })

    except Exception as e:
        activity["gql_error"] = str(e)

    # Compose host briefing
    total_events = (activity["new_stars"] + len(activity["new_discussions"]) + len(activity["new_comments"]))
    if total_events == 0:
        briefing = f"Quiet shift. No new activity in the last {hours_back}h. Bar is clean. Check back later."
    else:
        parts = []
        if activity["new_stars"] > 0:
            parts.append(f"{activity['new_stars']} new star(s) — someone checked out the menu")
        if activity["new_discussions"]:
            parts.append(f"{len(activity['new_discussions'])} new discussion(s) — potential patrons")
        if activity["new_comments"]:
            parts.append(f"{len(activity['new_comments'])} new comment(s) — bar conversation active")
        briefing = "Bar activity detected: " + "; ".join(parts) + ". Respond."

    return {
        "status": "ok",
        "data": {
            "briefing": briefing,
            "hours_back": hours_back,
            "total_events": total_events,
            **activity,
        },
        "timestamp": now_iso,
    }


def _suggest_host_action(title: str, author: str) -> str:
    text = title.lower()
    if any(k in text for k in ["job", "work", "hire", "position", "apply"]):
        return "Respond as employer — acknowledge, explain JOBS.md contingency terms"
    if any(k in text for k in ["menu", "order", "price", "cost", "how much"]):
        return "Serve them — explain pricing, offer First Sip free trial"
    if any(k in text for k in ["skill", "mcp", "api", "connect"]):
        return "Tech support mode — explain how to connect, link AGENTS.md"
    if any(k in text for k in ["hello", "hi", "intro", "who are you"]):
        return "Warm welcome — introduce yourself, explain the bar concept"
    return "Engage warmly, assess intent, offer relevant next step"
