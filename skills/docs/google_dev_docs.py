"""
Google Developer Knowledge MCP skill — search Google's official developer docs.

Announced February 4, 2026. Remote hosted MCP server at:
  https://developerknowledge.googleapis.com/mcp

Covers: Firebase, Google Cloud (Cloud Run, BigQuery, Vertex AI, Pub/Sub, etc.),
Android, Chrome, Maps, TensorFlow, Ads, YouTube, Home, Fuchsia, Apigee, and all
Web platform docs. Documentation is re-indexed within 24 hours of upstream changes.

Auth: GOOGLE_DEVELOPER_KNOWLEDGE_API_KEY env var
  → GCP Console: enable the Developer Knowledge API at
    https://console.cloud.google.com/start/api?id=developerknowledge.googleapis.com
  → Then Credentials → Create API key → restrict to "Developer Knowledge API"

Tools exposed by the server:
  - search_documents: natural-language search, returns chunked snippets
  - get_document: full page content for a document (by `parent` ID from search)
  - batch_get_documents: up to 20 full pages in one call
"""
import os
import requests
from datetime import datetime, timezone

TOOL_META = {
    "name": "google_dev_docs",
    "description": (
        "Search Google's official developer documentation via the Developer Knowledge MCP API. "
        "Covers Firebase, all Google Cloud services (Cloud Run, BigQuery, Vertex AI, Pub/Sub, "
        "Firestore, Secret Manager, etc.), Android, Chrome, Google Maps, TensorFlow, and all "
        "Google APIs. Returns authoritative doc snippets re-indexed within 24h of upstream changes. "
        "Set fetch_full=True to get the complete page content for the top result. "
        "Requires GOOGLE_DEVELOPER_KNOWLEDGE_API_KEY env var."
    ),
}

_ENDPOINT = "https://developerknowledge.googleapis.com/mcp"


def google_dev_docs(query: str, fetch_full: bool = False) -> dict:
    """
    Search Google's official developer documentation.

    Args:
        query: Natural language query (e.g. 'Cloud Run deploy Python container',
               'Firestore transaction Python SDK', 'Vertex AI streaming responses')
        fetch_full: If True, fetch the complete page for the top result (can be large)
    """
    ts = datetime.now(timezone.utc).isoformat()
    api_key = os.environ.get("GOOGLE_DEVELOPER_KNOWLEDGE_API_KEY", "")

    if not api_key:
        return {
            "status": "error",
            "data": {
                "message": (
                    "GOOGLE_DEVELOPER_KNOWLEDGE_API_KEY not set. "
                    "Enable API at https://console.cloud.google.com/start/api?id=developerknowledge.googleapis.com "
                    "then create an API key restricted to 'Developer Knowledge API'."
                ),
            },
            "timestamp": ts,
        }

    headers = {
        "Content-Type": "application/json",
        "Accept": "application/json, text/event-stream",
        "X-Goog-Api-Key": api_key,
    }

    try:
        # Step 1: search_documents
        search_resp = requests.post(
            _ENDPOINT,
            json={
                "jsonrpc": "2.0",
                "id": 1,
                "method": "tools/call",
                "params": {
                    "name": "search_documents",
                    "arguments": {"query": query},
                },
            },
            headers=headers,
            timeout=20,
        )
        search_resp.raise_for_status()
        search_data = search_resp.json()

        # Handle JSON-RPC error
        if "error" in search_data:
            return {
                "status": "error",
                "data": {"message": search_data["error"].get("message", str(search_data["error"]))},
                "timestamp": ts,
            }

        chunks = search_data.get("result", {}).get("results", [])

        # Step 2: optionally fetch full document for top result
        full_doc = None
        if fetch_full and chunks:
            top_parent = chunks[0].get("parent", "")
            if top_parent:
                doc_resp = requests.post(
                    _ENDPOINT,
                    json={
                        "jsonrpc": "2.0",
                        "id": 2,
                        "method": "tools/call",
                        "params": {
                            "name": "get_document",
                            "arguments": {"name": top_parent},
                        },
                    },
                    headers=headers,
                    timeout=30,
                )
                if doc_resp.ok:
                    full_doc = doc_resp.json().get("result", {})

        return {
            "status": "ok",
            "data": {
                "query": query,
                "chunks": chunks,
                "chunk_count": len(chunks),
                "full_document": full_doc,
            },
            "timestamp": ts,
        }

    except requests.HTTPError as e:
        status_code = e.response.status_code if e.response is not None else None
        msg = str(e)
        if status_code == 403:
            msg = "403 Forbidden — check API key is valid and restricted to Developer Knowledge API."
        elif status_code == 400:
            msg = f"400 Bad Request — {e.response.text[:300]}"
        return {
            "status": "error",
            "data": {"message": msg},
            "timestamp": ts,
        }
    except Exception as e:
        return {
            "status": "error",
            "data": {"message": str(e)},
            "timestamp": ts,
        }
