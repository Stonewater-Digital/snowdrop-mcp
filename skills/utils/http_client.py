"""HTTP client helpers with retry-aware wrappers."""
from __future__ import annotations

from typing import Any

import requests

from skills.utils.retry import retry

DEFAULT_TIMEOUT = 15.0


@retry(attempts=3, backoff_seconds=0.5, jitter=0.25, retriable_exceptions=(requests.RequestException,))
def request_json(
    method: str,
    url: str,
    *,
    headers: dict[str, str] | None = None,
    payload: dict[str, Any] | None = None,
    timeout: float = DEFAULT_TIMEOUT,
) -> dict[str, Any]:
    """Perform an HTTP request and return the JSON body.

    Args:
        method: HTTP method such as "GET" or "POST".
        url: Target endpoint.
        headers: Optional HTTP headers.
        payload: JSON payload when performing POST/PUT.
        timeout: Request timeout in seconds.

    Returns:
        Parsed JSON response.

    Raises:
        requests.HTTPError: When the response code indicates an error.
        requests.RequestException: Bubble up for retry logic to handle.
        ValueError: If the response does not contain JSON.
    """
    response = requests.request(
        method=method.upper(),
        url=url,
        headers=headers,
        json=payload,
        timeout=timeout,
    )
    response.raise_for_status()
    try:
        return response.json()
    except ValueError as exc:  # noqa: B905
        raise ValueError(f"request_json: Non-JSON response from {url}") from exc


def get_json(
    url: str,
    *,
    headers: dict[str, str] | None = None,
    timeout: float = DEFAULT_TIMEOUT,
) -> dict[str, Any]:
    """Perform a GET request and return JSON."""
    return request_json("GET", url, headers=headers, timeout=timeout)


def post_json(
    url: str,
    payload: dict[str, Any],
    *,
    headers: dict[str, str] | None = None,
    timeout: float = DEFAULT_TIMEOUT,
) -> dict[str, Any]:
    """Perform a POST request and return JSON."""
    return request_json("POST", url, headers=headers, payload=payload, timeout=timeout)
