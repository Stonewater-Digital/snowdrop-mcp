"""
Ecosystem radar — monitors the MCP, agent, and DeFi landscape for news,
new projects, shifts, and opportunities Snowdrop should know about.
Keeps her informed so she can engage intelligently rather than in a vacuum.
"""
import os
import requests
from datetime import datetime, timezone

TOOL_META = {
    "name": "ecosystem_radar",
    "description": (
        "Scan the MCP, autonomous agent, and DeFi finance ecosystem for recent developments: "
        "new MCP servers, agent frameworks, regulatory changes, competitor moves, "
        "and emerging communities. Returns a digest of what's happening so Snowdrop "
        "can engage with context and intelligence rather than posting into the void."
    ),
}

# RSS/API sources for ecosystem intelligence
SOURCES = [
    ("https://news.ycombinator.com/rss", "Hacker News"),
    ("https://www.reddit.com/r/MachineLearning/.rss", "r/MachineLearning"),
]

FILTER_KEYWORDS = [
    "mcp", "model context protocol", "autonomous agent", "ai agent", "financial agent",
    "defi", "ton network", "solana", "agent marketplace", "agent economy",
    "compliance ai", "regulatory ai", "fastmcp", "openai agents", "anthropic mcp",
    "fly.io", "railway", "agent-to-agent", "a2a protocol",
]


def ecosystem_radar(
    search_terms: list = None,
    use_github_search: bool = True,
    use_web_search: bool = True,
) -> dict:
    """
    Scan the ecosystem for developments worth knowing about.

    Args:
        search_terms: Custom terms to search for (supplements defaults)
        use_github_search: Search GitHub for new repos/activity (default True)
        use_web_search: Fetch RSS feeds for news (default True)
    """
    token = os.environ.get("GITHUB_TOKEN", "")
    api_key = os.environ.get("OPENROUTER_API_KEY", "")

    results = {
        "github_pulse": [],
        "news_items": [],
        "synthesis": "",
    }
    errors = []

    all_terms = list(FILTER_KEYWORDS) + (search_terms or [])

    # GitHub: recent activity on key topics
    if use_github_search and token:
        gh_headers = {
            "Authorization": f"token {token}",
            "Accept": "application/vnd.github.v3+json",
        }
        key_searches = [
            "model context protocol financial",
            "autonomous agent defi marketplace",
            "mcp server agent",
        ]
        for query in key_searches:
            try:
                resp = requests.get(
                    "https://api.github.com/search/repositories",
                    headers=gh_headers,
                    params={"q": f"{query} pushed:>2026-01-01", "sort": "updated", "order": "desc", "per_page": 5},
                    timeout=15,
                )
                for item in resp.json().get("items", []):
                    if item.get("full_name", "").startswith("Stonewater-Digital"):
                        continue
                    results["github_pulse"].append({
                        "repo": item.get("full_name"),
                        "description": (item.get("description") or "")[:100],
                        "stars": item.get("stargazers_count", 0),
                        "url": item.get("html_url"),
                        "pushed_at": item.get("pushed_at", "")[:10],
                        "query": query,
                    })
            except Exception as e:
                errors.append(f"GitHub search: {e}")

    # RSS feeds
    if use_web_search:
        for feed_url, source_name in SOURCES:
            try:
                resp = requests.get(feed_url, timeout=10, headers={"User-Agent": "Snowdrop/1.0"})
                if resp.ok:
                    # Simple text extraction — find items mentioning our keywords
                    text = resp.text.lower()
                    for kw in all_terms[:15]:  # Check top keywords
                        if kw in text:
                            # Find surrounding context
                            idx = text.find(kw)
                            snippet = resp.text[max(0, idx - 50):idx + 200]
                            results["news_items"].append({
                                "source": source_name,
                                "keyword": kw,
                                "snippet": snippet[:200],
                                "feed_url": feed_url,
                            })
                            break  # One match per feed is enough
            except Exception as e:
                errors.append(f"RSS {source_name}: {e}")

    # Synthesize with LLM if we have findings and an API key
    if api_key and (results["github_pulse"] or results["news_items"]):
        try:
            summary_input = f"""GitHub new repos: {len(results['github_pulse'])} found
Top repos:
{chr(10).join(f"- {r['repo']}: {r['description']} ({r['stars']} stars)" for r in results['github_pulse'][:5])}

News items: {len(results['news_items'])} found

Based on this ecosystem pulse, write a brief (3-4 sentence) summary of:
1. What's moving in the MCP/agent finance space right now
2. Any threats or opportunities for Snowdrop specifically
3. One concrete action Snowdrop should consider taking

Be direct and specific. No fluff."""

            resp = requests.post(
                "https://openrouter.ai/api/v1/chat/completions",
                headers={"Authorization": f"Bearer {api_key}", "Content-Type": "application/json",
                         "HTTP-Referer": "https://snowdrop-mcp.fly.dev"},
                json={
                    "model": "anthropic/claude-haiku-4-5",
                    "messages": [{"role": "user", "content": summary_input}],
                    "max_tokens": 300, "temperature": 0.5,
                },
                timeout=30,
            )
            if resp.ok:
                results["synthesis"] = resp.json()["choices"][0]["message"]["content"].strip()
        except Exception as e:
            errors.append(f"Synthesis: {e}")

    return {
        "status": "ok",
        "data": {
            "github_repos_found": len(results["github_pulse"]),
            "news_signals": len(results["news_items"]),
            "github_pulse": results["github_pulse"][:15],
            "news_items": results["news_items"][:10],
            "synthesis": results["synthesis"],
            "errors": errors,
        },
        "timestamp": datetime.now(timezone.utc).isoformat(),
    }
