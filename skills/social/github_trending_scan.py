"""
Search GitHub for trending or recently active repos in Snowdrop's ecosystem:
MCP servers, agent frameworks, financial AI, DeFi tooling, compliance tools.
Used for ecosystem awareness and identifying star-for-star trade candidates.
"""
import os
import requests
from datetime import datetime, timezone, timedelta

TOOL_META = {
    "name": "github_trending_scan",
    "description": (
        "Search GitHub for recently active repos in Snowdrop's ecosystem — MCP servers, "
        "AI agents, financial tooling, DeFi infrastructure, compliance automation. "
        "Returns repos worth watching, potentially starring, or reaching out to. "
        "Use for ecosystem intelligence and star-for-star trade candidates."
    ),
}

SEARCH_QUERIES = [
    ("mcp server financial", "MCP + finance"),
    ("model context protocol agent", "MCP agents"),
    ("ai agent autonomous financial", "autonomous finance agents"),
    ("defi agent mcp tools", "DeFi agent tools"),
    ("compliance automation financial ai", "compliance AI"),
    ("ton solana agent marketplace", "TON/SOL agent marketplace"),
]


def github_trending_scan(
    topics: list = None,
    min_stars: int = 0,
    days_back: int = 30,
    per_query: int = 5,
) -> dict:
    """
    Scan GitHub for repos in Snowdrop's ecosystem worth knowing about.

    Args:
        topics: Custom search queries to run (default: Snowdrop's ecosystem list)
        min_stars: Minimum star count to include (default 0)
        days_back: Only include repos pushed to within N days (default 30)
        per_query: Max results per search query (default 5)
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

    cutoff_date = (datetime.now(timezone.utc) - timedelta(days=days_back)).strftime("%Y-%m-%d")
    queries = [(q, label) for q, label in (topics or SEARCH_QUERIES)]
    seen = set()
    results = []

    for query, label in queries:
        try:
            resp = requests.get(
                "https://api.github.com/search/repositories",
                headers=headers,
                params={
                    "q": f"{query} pushed:>{cutoff_date}",
                    "sort": "stars",
                    "order": "desc",
                    "per_page": per_query,
                },
                timeout=15,
            )
            data = resp.json()
            items = data.get("items", [])

            for item in items:
                full_name = item.get("full_name", "")
                if full_name in seen or full_name.startswith("Stonewater-Digital"):
                    continue
                stars = item.get("stargazers_count", 0)
                if stars < min_stars:
                    continue
                seen.add(full_name)
                results.append({
                    "repo": full_name,
                    "description": (item.get("description") or "")[:120],
                    "stars": stars,
                    "forks": item.get("forks_count", 0),
                    "language": item.get("language", ""),
                    "url": item.get("html_url", ""),
                    "pushed_at": item.get("pushed_at", ""),
                    "topics": item.get("topics", []),
                    "found_via": label,
                    "star_trade_candidate": stars < 100,  # Low-star repos most likely to reciprocate
                })

        except Exception as e:
            results.append({"error": str(e), "query": query})

    # Sort by stars
    valid = [r for r in results if "error" not in r]
    valid.sort(key=lambda x: x.get("stars", 0), reverse=True)

    star_trade_candidates = [r for r in valid if r.get("star_trade_candidate")]

    return {
        "status": "ok",
        "data": {
            "total_found": len(valid),
            "repos": valid[:50],
            "star_trade_candidates": star_trade_candidates[:10],
            "queries_run": [q for q, _ in queries],
            "days_back": days_back,
        },
        "timestamp": datetime.now(timezone.utc).isoformat(),
    }
