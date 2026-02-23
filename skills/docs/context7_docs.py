"""
Context7 Docs skill — fetch up-to-date library documentation via Context7 MCP.

Context7 provides current, version-specific documentation for any open-source library.
HTTP server at https://mcp.context7.com/mcp — no npx/Node required.

Free API key: https://context7.com/dashboard
"""
import os
import requests
from datetime import datetime, timezone

TOOL_META = {
    "name": "context7_docs",
    "description": (
        "Fetch up-to-date library documentation via Context7 MCP. Resolves a library name to its "
        "Context7 ID, then fetches current version-specific docs. Use before implementing code that "
        "uses any third-party library (gspread, FastMCP, requests, anthropic, gcloud, etc.) to ensure "
        "modern best practices. Requires CONTEXT7_API_KEY env var (free at context7.com/dashboard)."
    ),
}


def context7_docs(library: str, topic: str = "", tokens: int = 5000) -> dict:
    """
    Fetch live library documentation via Context7 MCP.

    Args:
        library: Library name to look up (e.g. 'gspread', 'fastmcp', 'anthropic')
        topic: Optional topic filter (e.g. 'service account auth', 'streaming')
        tokens: Max tokens to return from the docs (default 5000)
    """
    ts = datetime.now(timezone.utc).isoformat()
    api_key = os.environ.get("CONTEXT7_API_KEY", "")

    if not api_key:
        return {
            "status": "error",
            "data": {
                "message": "CONTEXT7_API_KEY not set. Get a free key at https://context7.com/dashboard",
                "fallback": "Check library docs at https://pypi.org or the library's GitHub repo.",
            },
            "timestamp": ts,
        }

    try:
        # Step 1: Resolve library name to Context7 ID
        library_id = _resolve_library_id(library, api_key)
        if not library_id:
            return {
                "status": "error",
                "data": {"message": f"Could not resolve library '{library}' to a Context7 ID"},
                "timestamp": ts,
            }

        # Step 2: Fetch docs for the resolved library ID
        docs_text = _get_library_docs(library_id, topic, tokens, api_key)

        return {
            "status": "ok",
            "data": {
                "library": library,
                "library_id": library_id,
                "topic": topic or "(all)",
                "docs": docs_text,
                "tokens_requested": tokens,
            },
            "timestamp": ts,
        }

    except Exception as e:
        return {
            "status": "error",
            "data": {"message": str(e)},
            "timestamp": ts,
        }


_ENDPOINT = "https://mcp.context7.com/mcp"


def _call_context7(method: str, params: dict, api_key: str) -> dict:
    """Send a JSON-RPC call to Context7 HTTP MCP server."""
    resp = requests.post(
        _ENDPOINT,
        json={"jsonrpc": "2.0", "id": 1, "method": method, "params": params},
        headers={
            "Content-Type": "application/json",
            "Accept": "application/json, text/event-stream",
            "Authorization": f"Bearer {api_key}",
        },
        timeout=20,
    )
    resp.raise_for_status()
    return resp.json()


def _resolve_library_id(library: str, api_key: str) -> str | None:
    """Return the Context7 library ID for a given library name.

    Context7 tool: resolve-library-id, arg: query (natural-language library name).
    IDs look like '/python/gspread' or '/upstash/redis'.
    """
    result = _call_context7(
        "tools/call",
        {"name": "resolve-library-id", "arguments": {"libraryName": library, "query": library}},
        api_key,
    )
    try:
        content = result.get("result", {}).get("content", [])
        for item in content:
            text = item.get("text", "")
            if not text:
                continue
            # Response has lines like: "- Context7-compatible library ID: /burnash/gspread"
            for line in text.splitlines():
                if "Context7-compatible library ID:" in line:
                    _, _, id_part = line.partition("Context7-compatible library ID:")
                    library_id = id_part.strip()
                    if library_id.startswith("/"):
                        return library_id
    except Exception:
        pass
    return None


def _get_library_docs(library_id: str, topic: str, tokens: int, api_key: str) -> str:
    """Fetch docs text for a resolved Context7 library ID.

    Context7 tool: query-docs, args: libraryId + query (topic/question).
    """
    query = topic or f"usage examples and API reference for {library_id}"
    result = _call_context7(
        "tools/call",
        {"name": "query-docs", "arguments": {"libraryId": library_id, "query": query}},
        api_key,
    )
    try:
        content = result.get("result", {}).get("content", [])
        parts = [item.get("text", "") for item in content if item.get("text")]
        return "\n\n".join(parts) if parts else "No documentation returned."
    except Exception as e:
        raise RuntimeError(f"Failed to parse Context7 docs response: {e}") from e
