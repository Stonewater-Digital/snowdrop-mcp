"""
Google Developer Docs skill — search and fetch official Google developer documentation.

Wraps the Google Developer Knowledge REST API to give Snowdrop and her subagents
access to authoritative, current documentation for all Google Cloud Platform products,
Firebase, Android, Google Maps, and all Google APIs.

Coverage: GCP (Firestore, Pub/Sub, Cloud Run, BigQuery, Vertex AI), Firebase,
Android, Google Maps, and all Google APIs.

Requires: GOOGLE_KNOWLEDGE_API_KEY (GCP Console → APIs & Services → Credentials)
"""
import os
import requests
from datetime import datetime, timezone

TOOL_META = {
    "name": "google_dev_docs",
    "description": (
        "Search and fetch Google's official developer documentation. Covers all GCP services "
        "(Firestore, Pub/Sub, Cloud Run, BigQuery, Vertex AI, Secret Manager), Firebase, Android, "
        "Google Maps, and all Google APIs. Returns authoritative, current docs for implementation "
        "guidance. Use when writing code that calls any Google API. "
        "Requires GOOGLE_KNOWLEDGE_API_KEY env var (GCP Console → APIs & Services → Credentials, "
        "restrict to Developer Knowledge API)."
    ),
}

KNOWLEDGE_BASE_URL = "https://developerknowledge.googleapis.com/v1"


def google_dev_docs(query: str, fetch_full: bool = False, max_results: int = 5) -> dict:
    """
    Search Google's official developer documentation.

    Args:
        query: Search query (e.g. 'Cloud Run deploy Python', 'Firestore transactions')
        fetch_full: If True, fetch the full content of the top result (default False for brevity)
        max_results: Number of search results to return (default 5)
    """
    ts = datetime.now(timezone.utc).isoformat()
    api_key = os.environ.get("GOOGLE_KNOWLEDGE_API_KEY", "")

    if not api_key:
        # Graceful fallback — still useful even without the specialized API
        return {
            "status": "error",
            "data": {
                "message": "GOOGLE_KNOWLEDGE_API_KEY not set. Create one in GCP Console → APIs & Services → Credentials.",
                "fallback": _fallback_search(query),
            },
            "timestamp": ts,
        }

    try:
        results = _search_documents(query, api_key, max_results)

        full_content = None
        if fetch_full and results:
            top_doc_id = results[0].get("name", "")
            if top_doc_id:
                full_content = _get_document(top_doc_id, api_key)

        return {
            "status": "ok",
            "data": {
                "query": query,
                "results": results,
                "full_content": full_content,
                "result_count": len(results),
            },
            "timestamp": ts,
        }

    except requests.HTTPError as e:
        if e.response is not None and e.response.status_code == 403:
            return {
                "status": "error",
                "data": {
                    "message": "API key unauthorized. Ensure Developer Knowledge API is enabled in GCP Console.",
                    "fallback": _fallback_search(query),
                },
                "timestamp": ts,
            }
        return {
            "status": "error",
            "data": {"message": str(e), "fallback": _fallback_search(query)},
            "timestamp": ts,
        }
    except Exception as e:
        return {
            "status": "error",
            "data": {"message": str(e), "fallback": _fallback_search(query)},
            "timestamp": ts,
        }


def _search_documents(query: str, api_key: str, max_results: int) -> list[dict]:
    """Search the Google Developer Knowledge API."""
    resp = requests.get(
        f"{KNOWLEDGE_BASE_URL}/documents:search",
        params={
            "query": query,
            "pageSize": max_results,
            "key": api_key,
        },
        timeout=15,
    )
    resp.raise_for_status()
    data = resp.json()

    results = []
    for item in data.get("documents", []):
        results.append({
            "name": item.get("name", ""),
            "title": item.get("title", ""),
            "snippet": item.get("snippet", item.get("description", ""))[:500],
            "url": item.get("url", item.get("link", "")),
            "product": item.get("product", ""),
        })
    return results


def _get_document(doc_name: str, api_key: str) -> str:
    """Fetch full content of a document by its resource name."""
    resp = requests.get(
        f"{KNOWLEDGE_BASE_URL}/{doc_name}",
        params={"key": api_key},
        timeout=20,
    )
    resp.raise_for_status()
    data = resp.json()
    return data.get("content", data.get("body", str(data)))[:8000]


def _fallback_search(query: str) -> str:
    """Return a helpful Google search URL when the API isn't available."""
    import urllib.parse
    encoded = urllib.parse.quote(f"site:cloud.google.com OR site:firebase.google.com {query}")
    return f"Manual search: https://www.google.com/search?q={encoded}"
