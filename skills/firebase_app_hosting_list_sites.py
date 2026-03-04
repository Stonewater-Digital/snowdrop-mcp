"""
Executive Summary
-----------------
Lists Firebase App Hosting backends for a GCP project using the Firebase App Hosting
REST API (v1beta). Firebase App Hosting is the framework-aware hosting service that
supports Next.js, Angular, and other modern web frameworks with CI/CD integration
directly from a connected source repository.

Returns backend identifiers, display names, connected repository URLs, live site URLs,
managed resource summaries, and lifecycle timestamps.

Credentials resolved ADC-first (Cloud Run), then GOOGLE_SERVICE_ACCOUNT_JSON (local dev).

Inputs:
  project_id : str | None — GCP project ID (falls back to GOOGLE_PROJECT_ID env)
  location   : str        — GCP region, default "us-central1"
  page_size  : int        — maximum backends to return, default 20

Outputs:
  {"status": "ok"|"error", "data": {...}, "timestamp": "<ISO8601>"}

MCP Tool Name: firebase_app_hosting_list_sites

Agent Notes:
  - Required IAM: roles/firebaseapphosting.viewer or roles/firebase.viewer
  - The API is currently in v1beta; field names may evolve.
  - Backends in CREATING or DELETING state are included in the response.
  - live_url may be absent for backends that have never completed a deploy.
"""

import json
import logging
import os
from datetime import datetime, timezone

import requests

logger = logging.getLogger("snowdrop.firebase_app_hosting_list_sites")

TOOL_META = {
    "name": "firebase_app_hosting_list_sites",
    "description": (
        "List Firebase App Hosting backends for a project. "
        "Returns backend ID, repository URL, deploy status, and live URL."
    ),
    "tier": "free",
}

_CLOUD_PLATFORM_SCOPE = "https://www.googleapis.com/auth/cloud-platform"


def _get_access_token(scopes: list[str]) -> str:
    """Get an OAuth2 access token. ADC-first (Cloud Run), JSON fallback (local dev).

    Args:
        scopes: List of OAuth2 scope strings to request.

    Returns:
        A valid Bearer token string.

    Raises:
        RuntimeError: If no credential source is available.
    """
    import google.auth.transport.requests

    sa_json = os.environ.get("GOOGLE_SERVICE_ACCOUNT_JSON")
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


def _now() -> str:
    """Return current UTC time as ISO 8601 string."""
    return datetime.now(timezone.utc).isoformat()


def _parse_backend(raw: dict) -> dict:
    """Extract a normalized summary from a raw Firebase App Hosting backend record.

    Args:
        raw: Raw backend dict from the Firebase App Hosting API response.

    Returns:
        Normalized dict with consistent, documented keys.
    """
    name: str = raw.get("name", "")
    # name format: projects/{project}/locations/{location}/backends/{backend_id}
    backend_id: str = name.split("/")[-1] if name else ""

    # Repository information may be nested under codebase or repository
    codebase = raw.get("codebase", {})
    repository: str = (
        codebase.get("repository", "")
        or raw.get("repository", "")
    )

    # Managed resources: list of associated GCP resource names
    managed_resources_raw = raw.get("managedResources", [])
    managed_resources: list[str] = [
        r.get("runService", {}).get("service", r.get("name", str(r)))
        if isinstance(r, dict)
        else str(r)
        for r in managed_resources_raw
    ]

    return {
        "backend_id": backend_id,
        "display_name": raw.get("displayName", ""),
        "repository": repository,
        "live_url": raw.get("uri", raw.get("liveUrl", raw.get("defaultUri", ""))),
        "state": raw.get("state", ""),
        "managed_resources": managed_resources,
        "create_time": raw.get("createTime", ""),
        "update_time": raw.get("updateTime", ""),
    }


def firebase_app_hosting_list_sites(
    project_id: str | None = None,
    location: str = "us-central1",
    page_size: int = 20,
) -> dict:
    """List Firebase App Hosting backends for a GCP project.

    Queries the Firebase App Hosting REST API (v1beta) for all backends
    under the specified project and location. Backends represent framework-aware
    hosting deployments backed by a source repository such as GitHub.

    Args:
        project_id: GCP project ID. Defaults to the ``GOOGLE_PROJECT_ID``
            environment variable when not provided.
        location: GCP region where the App Hosting backends are deployed.
            Defaults to ``"us-central1"``.
        page_size: Maximum number of backends to return in a single call.
            Defaults to 20. The API may return fewer results.

    Returns:
        dict with keys:
            - status (str): ``"ok"`` or ``"error"``.
            - data (dict): Contains ``backends`` (list of normalized backend
              dicts), ``count`` (int), ``location`` (str), and
              ``project_id`` (str).
            - timestamp (str): ISO 8601 UTC execution timestamp.

    Raises:
        Does not raise; all exceptions are caught and returned as error dicts.

    Example:
        >>> result = firebase_app_hosting_list_sites(project_id="my-gcp-project")
        >>> result["status"]
        'ok'
        >>> isinstance(result["data"]["backends"], list)
        True
    """
    logger.info(
        "firebase_app_hosting_list_sites: entry project=%s location=%s page_size=%d",
        project_id,
        location,
        page_size,
    )

    project_id = project_id or os.environ.get("GOOGLE_PROJECT_ID", "")
    if not project_id:
        logger.error("firebase_app_hosting_list_sites: project_id missing")
        return {
            "status": "error",
            "data": {"message": "project_id is required or set GOOGLE_PROJECT_ID"},
            "timestamp": _now(),
        }

    try:
        token = _get_access_token([_CLOUD_PLATFORM_SCOPE])
        headers = {
            "Authorization": f"Bearer {token}",
            "Content-Type": "application/json",
        }

        url = (
            f"https://firebaseapphosting.googleapis.com/v1beta"
            f"/projects/{project_id}/locations/{location}/backends"
        )
        params: dict = {"pageSize": page_size}

        logger.info("firebase_app_hosting_list_sites: GET %s", url)
        resp = requests.get(url, headers=headers, params=params, timeout=20)

        if resp.status_code != 200:
            logger.error(
                "firebase_app_hosting_list_sites: API error %d: %s",
                resp.status_code,
                resp.text[:400],
            )
            return {
                "status": "error",
                "data": {
                    "message": f"Firebase App Hosting API returned {resp.status_code}",
                    "detail": resp.text[:400],
                },
                "timestamp": _now(),
            }

        body = resp.json()
        raw_backends = body.get("backends", [])
        backends = [_parse_backend(b) for b in raw_backends]

        logger.info(
            "firebase_app_hosting_list_sites: exit success count=%d", len(backends)
        )
        return {
            "status": "ok",
            "data": {
                "backends": backends,
                "count": len(backends),
                "location": location,
                "project_id": project_id,
            },
            "timestamp": _now(),
        }

    except Exception as exc:
        logger.error(
            "firebase_app_hosting_list_sites: unexpected error: %s", exc, exc_info=True
        )
        return {
            "status": "error",
            "data": {"message": str(exc)},
            "timestamp": _now(),
        }
