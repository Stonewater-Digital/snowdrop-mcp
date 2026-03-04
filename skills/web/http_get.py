"""
HTTP GET Skill — make an authenticated or unauthenticated HTTP GET request and return
the response body, status code, and response headers.

Useful for agents that need to fetch external data sources, check APIs, or probe
endpoints without writing bespoke HTTP code in each skill.

No secrets stored — callers supply auth headers directly if needed.
"""

from datetime import datetime

import requests

TOOL_META = {
    "name": "http_get",
    "description": (
        "Make an HTTP GET request to any URL and return the response. Optionally pass "
        "custom headers (e.g. Authorization). Parses response as JSON by default; set "
        "json_only=false to get raw text instead. Returns status_code, body, response "
        "headers, and the final URL after any redirects."
    ),
    "inputSchema": {
        "type": "object",
        "properties": {
            "url": {
                "type": "string",
                "description": "Full URL to fetch, including scheme (https://).",
            },
            "headers": {
                "type": "object",
                "description": (
                    "Optional key-value pairs to send as HTTP request headers, "
                    "e.g. {\"Authorization\": \"Bearer token\"}."
                ),
                "additionalProperties": {"type": "string"},
            },
            "timeout": {
                "type": "integer",
                "description": "Request timeout in seconds (default 15, max 120).",
                "default": 15,
            },
            "json_only": {
                "type": "boolean",
                "description": (
                    "If true (default), attempt to parse the response as JSON. "
                    "If false, return the raw response text."
                ),
                "default": True,
            },
        },
        "required": ["url"],
    },
}


def http_get(
    url: str,
    headers: dict = None,
    timeout: int = 15,
    json_only: bool = True,
) -> dict:
    """Make an HTTP GET request and return the response."""

    timestamp = datetime.utcnow().isoformat() + "Z"

    if not url or not url.strip():
        return {
            "status": "error",
            "data": {"message": "url must be a non-empty string."},
            "timestamp": timestamp,
        }

    url = url.strip()
    if not url.startswith(("http://", "https://")):
        return {
            "status": "error",
            "data": {"message": "url must begin with http:// or https://."},
            "timestamp": timestamp,
        }

    # Clamp timeout
    timeout = max(1, min(int(timeout), 120))

    request_headers = {}
    if headers:
        if not isinstance(headers, dict):
            return {
                "status": "error",
                "data": {"message": "headers must be a JSON object (dict)."},
                "timestamp": timestamp,
            }
        request_headers.update(headers)

    try:
        resp = requests.get(url, headers=request_headers, timeout=timeout)
    except requests.exceptions.Timeout:
        return {
            "status": "error",
            "data": {"message": f"GET request to {url} timed out after {timeout}s."},
            "timestamp": datetime.utcnow().isoformat() + "Z",
        }
    except requests.exceptions.ConnectionError as exc:
        return {
            "status": "error",
            "data": {"message": f"Connection error for GET {url}: {exc}"},
            "timestamp": datetime.utcnow().isoformat() + "Z",
        }
    except requests.exceptions.RequestException as exc:
        return {
            "status": "error",
            "data": {"message": f"HTTP GET failed: {exc}"},
            "timestamp": datetime.utcnow().isoformat() + "Z",
        }

    # Parse body
    body = None
    parse_error = None
    if json_only:
        try:
            body = resp.json()
        except ValueError as exc:
            parse_error = str(exc)
            body = resp.text
    else:
        body = resp.text

    response_headers = dict(resp.headers)

    result: dict = {
        "status": "ok",
        "data": {
            "status_code": resp.status_code,
            "body": body,
            "headers": response_headers,
            "url": resp.url,
        },
        "timestamp": datetime.utcnow().isoformat() + "Z",
    }

    if parse_error:
        result["data"]["json_parse_error"] = parse_error

    return result
