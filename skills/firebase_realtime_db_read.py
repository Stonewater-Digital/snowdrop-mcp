"""Firebase Realtime Database read skill.

Reads a node from Firebase Realtime Database using the REST API
authenticated with Google OAuth2 credentials.
"""

import json
import logging
import os
from datetime import datetime, timezone

import httpx

logger = logging.getLogger("snowdrop.firebase_realtime_db_read")

TOOL_META = {
    "name": "firebase_realtime_db_read",
    "description": "Read a value from Firebase Realtime Database at the given path. Returns the value as JSON.",
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


def firebase_realtime_db_read(
    path: str,
    database_url: str | None = None,
) -> dict:
    """Read a value from Firebase Realtime Database at the given path.

    Performs an authenticated HTTP GET against the Realtime Database REST endpoint.
    Returns whatever JSON value is stored at the path (object, array, scalar, or null).

    Args:
        path: Database path to read, e.g. "/users/123" or "/config/featureFlags".
            Must start with "/".
        database_url: Full URL of the Realtime Database instance, e.g.
            "https://my-project-default-rtdb.firebaseio.com". If not provided,
            reads from the FIREBASE_DATABASE_URL environment variable.

    Returns:
        dict: Standard Snowdrop response envelope.
            On success: {"status": "ok", "data": {"path": str, "value": any}, "timestamp": str}
            On error: {"status": "error", "data": {"error": str}, "timestamp": str}

    Raises:
        ValueError: If database_url cannot be resolved.
        httpx.HTTPStatusError: If the REST API returns a non-2xx status.

    Example:
        >>> result = firebase_realtime_db_read(path="/users/alice")
        >>> result["status"]
        'ok'
        >>> result["data"]["value"]
        {"name": "Alice", "email": "alice@example.com"}
    """
    logger.info("firebase_realtime_db_read entered | path=%s", path)

    db_url = database_url or os.environ.get("FIREBASE_DATABASE_URL")
    if not db_url:
        msg = "database_url not provided and FIREBASE_DATABASE_URL is not set."
        logger.error("firebase_realtime_db_read error: %s", msg)
        return {"status": "error", "data": {"error": msg}, "timestamp": _now()}

    db_url = db_url.rstrip("/")
    if not path.startswith("/"):
        path = "/" + path

    try:
        token = _get_access_token()
        url = f"{db_url}{path}.json"

        with httpx.Client(timeout=15.0) as client:
            response = client.get(url, params={"access_token": token})
            response.raise_for_status()

        value = response.json()
        logger.info("firebase_realtime_db_read success | path=%s value_type=%s", path, type(value).__name__)
        return {
            "status": "ok",
            "data": {"path": path, "value": value},
            "timestamp": _now(),
        }

    except Exception as exc:
        logger.error("firebase_realtime_db_read error: %s", exc, exc_info=True)
        return {"status": "error", "data": {"error": str(exc)}, "timestamp": _now()}
