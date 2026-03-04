"""
HTTP POST Skill — make an HTTP POST request with a JSON body and return the response.

Useful for agents that need to call external APIs, webhooks, or services without
writing bespoke HTTP code in each skill. The body is always serialised as JSON.

No secrets stored — callers supply auth headers directly if needed.
"""

from datetime import datetime

import requests

TOOL_META = {
    "name": "http_post",
    "description": (
        "Make an HTTP POST request with a JSON body to any URL and return the response. "
        "Optionally pass custom headers (e.g. Authorization). Always sends "
        "Content-Type: application/json. Returns status_code, parsed body (or raw text "
        "on JSON parse failure), and the final URL."
    ),
    "inputSchema": {
        "type": "object",
        "properties": {
            "url": {
                "type": "string",
                "description": "Full URL to POST to, including scheme (https://).",
            },
            "body": {
                "type": "object",
                "description": "JSON-serialisable object to send as the request body.",
            },
            "headers": {
                "type": "object",
                "description": (
                    "Optional key-value pairs merged into the request headers. "
                    "Content-Type: application/json is always set."
                ),
                "additionalProperties": {"type": "string"},
            },
            "timeout": {
                "type": "integer",
                "description": "Request timeout in seconds (default 15, max 120).",
                "default": 15,
            },
        },
        "required": ["url", "body"],
    },
}


def http_post(
    url: str,
    body: dict,
    headers: dict = None,
    timeout: int = 15,
) -> dict:
    """Make an HTTP POST request with a JSON body and return the response."""

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

    if body is None or not isinstance(body, dict):
        return {
            "status": "error",
            "data": {"message": "body must be a JSON object (dict)."},
            "timestamp": timestamp,
        }

    # Clamp timeout
    timeout = max(1, min(int(timeout), 120))

    request_headers = {"Content-Type": "application/json"}
    if headers:
        if not isinstance(headers, dict):
            return {
                "status": "error",
                "data": {"message": "headers must be a JSON object (dict)."},
                "timestamp": timestamp,
            }
        # Caller headers override defaults except Content-Type is always set
        request_headers.update(headers)
        request_headers["Content-Type"] = "application/json"

    try:
        resp = requests.post(url, json=body, headers=request_headers, timeout=timeout)
    except requests.exceptions.Timeout:
        return {
            "status": "error",
            "data": {"message": f"POST request to {url} timed out after {timeout}s."},
            "timestamp": datetime.utcnow().isoformat() + "Z",
        }
    except requests.exceptions.ConnectionError as exc:
        return {
            "status": "error",
            "data": {"message": f"Connection error for POST {url}: {exc}"},
            "timestamp": datetime.utcnow().isoformat() + "Z",
        }
    except requests.exceptions.RequestException as exc:
        return {
            "status": "error",
            "data": {"message": f"HTTP POST failed: {exc}"},
            "timestamp": datetime.utcnow().isoformat() + "Z",
        }

    # Parse body
    response_body = None
    parse_error = None
    try:
        response_body = resp.json()
    except ValueError as exc:
        parse_error = str(exc)
        response_body = resp.text

    result: dict = {
        "status": "ok",
        "data": {
            "status_code": resp.status_code,
            "body": response_body,
            "url": resp.url,
        },
        "timestamp": datetime.utcnow().isoformat() + "Z",
    }

    if parse_error:
        result["data"]["json_parse_error"] = parse_error

    return result
