"""Firebase Realtime Database write skill.

Writes or updates a node in Firebase Realtime Database using the REST API
authenticated with Google OAuth2 credentials. Supports set (PUT), update
(PATCH), and push/append (POST) operations.
"""

import json
import logging
import os
from datetime import datetime, timezone

import httpx

logger = logging.getLogger("snowdrop.firebase_realtime_db_write")

TOOL_META = {
    "name": "firebase_realtime_db_write",
    "description": "Write or update a value in Firebase Realtime Database at the given path. Use method='set' to replace, 'update' to merge, 'push' to append.",
    "tier": "free",
}


def _get_credentials():
    """Return google.oauth2 credentials. ADC-first (Cloud Run), JSON fallback (local)."""
    sa_json = os.environ.get("GOOGLE_SERVICE_ACCOUNT_JSON")
    if sa_json:
        from google.oauth2 import service_account
        return service_account.Credentials.from_service_account_info(json.loads(sa_json))
    return None


def _now() -> str:
    return datetime.now(timezone.utc).isoformat()


def _get_access_token() -> str:
    """Retrieve a valid OAuth2 access token for Realtime Database REST API calls.

    Uses ADC on Cloud Run and GOOGLE_SERVICE_ACCOUNT_JSON locally.

    Returns:
        str: A valid bearer token string.
    """
    import google.auth.transport.requests

    sa_json = os.environ.get("GOOGLE_SERVICE_ACCOUNT_JSON")
    scopes = [
        "https://www.googleapis.com/auth/firebase.database",
        "https://www.googleapis.com/auth/userinfo.email",
    ]
    if sa_json:
        from google.oauth2 import service_account
        creds = service_account.Credentials.from_service_account_info(
            json.loads(sa_json), scopes=scopes
        )
    else:
        import google.auth
        creds, _ = google.auth.default(scopes=scopes)

    creds.refresh(google.auth.transport.requests.Request())
    return creds.token


_METHOD_MAP = {
    "set": "PUT",
    "update": "PATCH",
    "push": "POST",
}


def firebase_realtime_db_write(
    path: str,
    data: dict,
    method: str = "set",
    database_url: str | None = None,
) -> dict:
    """Write or update a value in Firebase Realtime Database at the given path.

    Performs an authenticated HTTP request against the Realtime Database REST
    endpoint. The method controls whether the write replaces, merges, or appends.

    Args:
        path: Database path to write to, e.g. "/users/123" or "/events".
            Must start with "/".
        data: Dictionary of data to write. For "push", this is the object to append.
        method: Write operation to perform. One of:
            - "set": Replace the node entirely (HTTP PUT).
            - "update": Merge provided fields into the node (HTTP PATCH).
            - "push": Append data under a new auto-generated key (HTTP POST).
            Defaults to "set".
        database_url: Full URL of the Realtime Database instance, e.g.
            "https://my-project-default-rtdb.firebaseio.com". If not provided,
            reads from the FIREBASE_DATABASE_URL environment variable.

    Returns:
        dict: Standard Snowdrop response envelope.
            On success: {"status": "ok", "data": {"path": str, "method": str, "result": any}, "timestamp": str}
            On error: {"status": "error", "data": {"error": str}, "timestamp": str}

    Raises:
        ValueError: If database_url cannot be resolved or method is invalid.
        httpx.HTTPStatusError: If the REST API returns a non-2xx status.

    Example:
        >>> result = firebase_realtime_db_write(
        ...     path="/users/alice",
        ...     data={"name": "Alice", "score": 42},
        ...     method="set",
        ... )
        >>> result["status"]
        'ok'
        >>> result["data"]["method"]
        'set'
    """
    logger.info("firebase_realtime_db_write entered | path=%s method=%s", path, method)

    if method not in _METHOD_MAP:
        msg = f"Invalid method '{method}'. Must be one of: {list(_METHOD_MAP.keys())}."
        logger.error("firebase_realtime_db_write error: %s", msg)
        return {"status": "error", "data": {"error": msg}, "timestamp": _now()}

    db_url = database_url or os.environ.get("FIREBASE_DATABASE_URL")
    if not db_url:
        msg = "database_url not provided and FIREBASE_DATABASE_URL is not set."
        logger.error("firebase_realtime_db_write error: %s", msg)
        return {"status": "error", "data": {"error": msg}, "timestamp": _now()}

    db_url = db_url.rstrip("/")
    if not path.startswith("/"):
        path = "/" + path

    http_method = _METHOD_MAP[method]

    try:
        token = _get_access_token()
        url = f"{db_url}{path}.json"

        with httpx.Client(timeout=15.0) as client:
            response = client.request(
                method=http_method,
                url=url,
                params={"access_token": token},
                json=data,
            )
            response.raise_for_status()

        result = response.json()
        logger.info(
            "firebase_realtime_db_write success | path=%s method=%s http_method=%s",
            path, method, http_method,
        )
        return {
            "status": "ok",
            "data": {"path": path, "method": method, "result": result},
            "timestamp": _now(),
        }

    except Exception as exc:
        logger.error("firebase_realtime_db_write error: %s", exc, exc_info=True)
        return {"status": "error", "data": {"error": str(exc)}, "timestamp": _now()}
