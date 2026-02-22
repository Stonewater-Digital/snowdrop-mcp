"""
Context7 Docs skill — fetch up-to-date library documentation via Context7 MCP.

Context7 (upstash/context7-mcp) provides current, version-specific documentation
for any open-source library. Snowdrop and her subagents call this before writing
code that uses any third-party library to ensure modern API patterns.

Free API key: https://context7.com/dashboard
"""
import json
import os
import subprocess
import sys
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
        # Step 1: Resolve library name to Context7 ID via JSON-RPC over npx subprocess
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


def _call_context7(method: str, params: dict, api_key: str) -> dict:
    """Send a JSON-RPC call to Context7 via npx subprocess (stdio transport)."""
    rpc_request = {
        "jsonrpc": "2.0",
        "id": 1,
        "method": method,
        "params": params,
    }

    env = os.environ.copy()
    env["CONTEXT7_API_KEY"] = api_key

    # Try HTTP endpoint first (faster, no npx startup)
    try:
        import requests as req_lib
        resp = req_lib.post(
            "https://mcp.context7.com/mcp",
            json=rpc_request,
            headers={
                "Content-Type": "application/json",
                "Authorization": f"Bearer {api_key}",
            },
            timeout=20,
        )
        resp.raise_for_status()
        return resp.json()
    except Exception:
        pass

    # Fallback: subprocess stdio JSON-RPC via npx
    proc = subprocess.run(
        ["npx", "-y", "@upstash/context7-mcp@latest"],
        input=json.dumps(rpc_request),
        capture_output=True,
        text=True,
        timeout=30,
        env=env,
    )
    if proc.returncode != 0 and proc.stderr:
        raise RuntimeError(f"Context7 npx error: {proc.stderr[:500]}")

    for line in proc.stdout.splitlines():
        line = line.strip()
        if line.startswith("{"):
            try:
                return json.loads(line)
            except json.JSONDecodeError:
                continue

    raise RuntimeError("No valid JSON-RPC response from Context7")


def _resolve_library_id(library: str, api_key: str) -> str | None:
    """Return the Context7 library ID for a given library name."""
    result = _call_context7(
        "tools/call",
        {
            "name": "resolve-library-id",
            "arguments": {"libraryName": library},
        },
        api_key,
    )
    # Response content is in result["result"]["content"][0]["text"]
    try:
        content = result.get("result", {}).get("content", [])
        for item in content:
            text = item.get("text", "")
            if text and "/" in text:
                # Context7 IDs look like "/python/gspread" or "/upstash/redis"
                for token in text.split():
                    if token.startswith("/") and "/" in token[1:]:
                        return token
            # Try to find any library-id-like string
            if text:
                return text.strip().split("\n")[0].strip()
    except Exception:
        pass
    return None


def _get_library_docs(library_id: str, topic: str, tokens: int, api_key: str) -> str:
    """Fetch docs text for a resolved Context7 library ID."""
    args = {"context7CompatibleLibraryID": library_id, "tokens": tokens}
    if topic:
        args["topic"] = topic

    result = _call_context7(
        "tools/call",
        {"name": "get-library-docs", "arguments": args},
        api_key,
    )
    try:
        content = result.get("result", {}).get("content", [])
        parts = []
        for item in content:
            text = item.get("text", "")
            if text:
                parts.append(text)
        return "\n\n".join(parts) if parts else "No documentation returned."
    except Exception as e:
        raise RuntimeError(f"Failed to parse Context7 docs response: {e}") from e
