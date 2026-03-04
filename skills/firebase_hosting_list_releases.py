"""Firebase Hosting — List Releases skill.

Lists release history for a Firebase Hosting site or channel via the Firebase
Hosting REST API v1beta1. Uses ADC-first credentials with
GOOGLE_SERVICE_ACCOUNT_JSON fallback.
"""

import json
import logging
import os
from datetime import datetime, timezone

import httpx

logger = logging.getLogger("snowdrop.firebase_hosting_list_releases")

TOOL_META = {
    "name": "firebase_hosting_list_releases",
    "description": "List release history for a Firebase Hosting site or channel. Returns list of releases with version, create_time, and status.",
    "tier": "free",
}

_FIREBASE_HOSTING_SCOPE = "https://www.googleapis.com/auth/firebase"
_HOSTING_BASE = "https://firebasehosting.googleapis.com/v1beta1"


def _get_access_token(scopes: list[str]) -> str:
    """Get an OAuth2 access token. ADC-first, JSON fallback.

    Args:
        scopes: List of OAuth2 scope strings required by the caller.

    Returns:
        A valid OAuth2 bearer token string.
    """
    sa_json = os.environ.get("GOOGLE_SERVICE_ACCOUNT_JSON")
    if sa_json:
        from google.oauth2 import service_account
        import google.auth.transport.requests
        creds = service_account.Credentials.from_service_account_info(
            json.loads(sa_json), scopes=scopes
        )
        creds.refresh(google.auth.transport.requests.Request())
        return creds.token
    else:
        import google.auth
        import google.auth.transport.requests
        creds, _ = google.auth.default(scopes=scopes)
        creds.refresh(google.auth.transport.requests.Request())
        return creds.token


def _now() -> str:
    return datetime.now(timezone.utc).isoformat()


def firebase_hosting_list_releases(
    site_id: str,
    channel_id: str = "live",
    page_size: int = 10,
) -> dict:
    """List release history for a Firebase Hosting site or channel.

    Calls the Firebase Hosting REST API to retrieve the ordered list of
    releases for a given site and channel. Results are returned newest-first
    as the API delivers them.

    Args:
        site_id: The Firebase Hosting site ID (e.g. ``'my-app'`` for
            ``my-app.web.app``).
        channel_id: The hosting channel to query. Use ``"live"`` (default) for
            the production channel, or a custom channel ID for preview channels.
        page_size: Maximum number of releases to return. Must be between 1
            and 100 inclusive. Defaults to 10.

    Returns:
        dict: A result envelope with the following structure::

            {
                "status": "ok",
                "data": {
                    "site_id": str,
                    "channel_id": str,
                    "releases": [
                        {
                            "name": str,            # full resource name
                            "version_name": str,    # version resource name
                            "type": str,            # e.g. "DEPLOY"
                            "create_time": str,     # ISO 8601 UTC
                            "release_user": str | None,  # email of releaser
                            "message": str | None,  # release description
                        },
                        ...
                    ],
                    "next_page_token": str | None,
                },
                "timestamp": str,  # ISO 8601 UTC
            }

        On error::

            {
                "status": "error",
                "data": {"error": str},
                "timestamp": str,
            }

    Raises:
        RuntimeError: If the Firebase Hosting REST API call fails.
        ValueError: If ``site_id`` is empty or ``page_size`` is out of range.

    Example:
        >>> result = firebase_hosting_list_releases(
        ...     site_id="my-app",
        ...     channel_id="live",
        ...     page_size=5,
        ... )
        >>> assert result["status"] == "ok"
        >>> for release in result["data"]["releases"]:
        ...     print(release["create_time"], release["type"])
    """
    logger.info(
        "firebase_hosting_list_releases: entry | site_id=%s channel_id=%s page_size=%d",
        site_id,
        channel_id,
        page_size,
    )
    try:
        if not site_id or not site_id.strip():
            raise ValueError("site_id must be a non-empty string.")
        if not 1 <= page_size <= 100:
            raise ValueError("page_size must be between 1 and 100 inclusive.")

        token = _get_access_token([_FIREBASE_HOSTING_SCOPE])
        headers = {
            "Authorization": f"Bearer {token}",
            "Content-Type": "application/json",
        }

        url = (
            f"{_HOSTING_BASE}/sites/{site_id}/channels/{channel_id}/releases"
            f"?pageSize={page_size}"
        )

        logger.info(
            "firebase_hosting_list_releases: fetching releases | url=%s", url
        )
        with httpx.Client(timeout=30) as client:
            resp = client.get(url, headers=headers)
            if resp.is_error:
                raise RuntimeError(
                    f"List releases failed with HTTP {resp.status_code}: {resp.text}"
                )
            data = resp.json()

        raw_releases: list[dict] = data.get("releases", [])
        next_page_token: str | None = data.get("nextPageToken")

        releases: list[dict] = []
        for r in raw_releases:
            version = r.get("version", {})
            release_user_info = r.get("releaseUser", {})
            release_user_email = release_user_info.get("email") if release_user_info else None

            releases.append(
                {
                    "name": r.get("name", ""),
                    "version_name": version.get("name", ""),
                    "type": r.get("type", ""),
                    "create_time": r.get("createTime", ""),
                    "release_user": release_user_email,
                    "message": r.get("message"),
                }
            )

        result = {
            "status": "ok",
            "data": {
                "site_id": site_id,
                "channel_id": channel_id,
                "releases": releases,
                "next_page_token": next_page_token,
            },
            "timestamp": _now(),
        }
        logger.info(
            "firebase_hosting_list_releases: exit | site_id=%s channel_id=%s count=%d",
            site_id,
            channel_id,
            len(releases),
        )
        return result

    except (ValueError, RuntimeError) as exc:
        logger.error("firebase_hosting_list_releases: error | %s", exc)
        return {"status": "error", "data": {"error": str(exc)}, "timestamp": _now()}
    except Exception as exc:
        logger.exception("firebase_hosting_list_releases: unexpected error | %s", exc)
        return {"status": "error", "data": {"error": str(exc)}, "timestamp": _now()}
