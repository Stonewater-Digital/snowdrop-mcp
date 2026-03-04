"""
Executive Summary
-----------------
Retrieves detailed information about a specific Firebase Crashlytics issue using
the Crashlytics REST API v1alpha1. Returns the issue title, state, user impact,
event count, first/last seen timestamps, target platform, and list of affected
app versions. Credentials are resolved via ADC on Cloud Run or via
GOOGLE_SERVICE_ACCOUNT_JSON for local and Railway deployments.

Credentials resolved in order:
  1. GOOGLE_SERVICE_ACCOUNT_JSON  — raw JSON string (Cloud Run / Railway / Fly.io)
  2. ADC (Application Default Credentials) — used automatically on Cloud Run

Inputs:
  app_id     : str  — Firebase App ID (required)
  issue_id   : str  — Crashlytics Issue ID (required)
  project_id : str  — GCP project ID (falls back to GOOGLE_PROJECT_ID env)

Outputs:
  {"status": "ok"|"error", "data": {...}, "timestamp": "<ISO8601>"}

MCP Tool Name: firebase_crashlytics_get_issue

Agent Notes (Claude Code / Cursor / Codex CLI / Gemini CLI):
  - Required IAM role: roles/firebase.viewer or roles/cloudplatform.viewer
  - issue_id is returned by firebase_crashlytics_list_issues
  - affected_versions is a list of app version strings (e.g. ["2.1.0", "2.0.5"])
"""

import json
import logging
import os
from datetime import datetime, timezone

import requests

logger = logging.getLogger("snowdrop.firebase_crashlytics_get_issue")

TOOL_META = {
    "name": "firebase_crashlytics_get_issue",
    "description": (
        "Get detailed information about a specific Firebase Crashlytics issue "
        "including stack trace summary and affected versions."
    ),
    "tier": "free",
}

_CRASHLYTICS_SCOPE = "https://www.googleapis.com/auth/cloud-platform"


def _now() -> str:
    return datetime.now(timezone.utc).isoformat()


def _wrap(status: str, data: dict) -> dict:
    return {"status": status, "data": data, "timestamp": _now()}


def _get_access_token(scopes: list[str]) -> str:
    """Obtain a bearer token via service account JSON or ADC."""
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


def firebase_crashlytics_get_issue(
    app_id: str,
    issue_id: str,
    project_id: str | None = None,
) -> dict:
    """Get detailed information about a specific Firebase Crashlytics issue.

    Args:
        app_id: Firebase App ID (e.g. "1:123456789:android:abc123def456").
            Visible in Firebase Console → Project Settings → Your Apps.
        issue_id: The Crashlytics issue identifier, as returned by
            firebase_crashlytics_list_issues.
        project_id: GCP project ID. Falls back to GOOGLE_PROJECT_ID env var
            if not supplied.

    Returns:
        dict: Standard Snowdrop envelope::

            {
                "status": "ok",
                "data": {
                    "issue_id": str,
                    "title": str,
                    "subtitle": str,
                    "state": str,
                    "users_affected": int,
                    "events_count": int,
                    "first_seen": str,
                    "last_seen": str,
                    "platform": str,
                    "affected_versions": list[str]
                },
                "timestamp": "<ISO8601>"
            }

    Raises:
        RuntimeError: If no GCP credentials are available.
        requests.HTTPError: If the Crashlytics API returns a non-2xx response.

    Example:
        >>> result = firebase_crashlytics_get_issue(
        ...     app_id="1:123456789012:android:abc123def456",
        ...     issue_id="00000000000000000001",
        ...     project_id="my-gcp-project",
        ... )
        >>> print(result["data"]["state"])
        OPEN
    """
    logger.info(
        "firebase_crashlytics_get_issue called: app_id=%s, issue_id=%s",
        app_id,
        issue_id,
    )

    project_id = project_id or os.environ.get("GOOGLE_PROJECT_ID", "")
    if not project_id:
        return _wrap(
            "error",
            {"message": "project_id is required (or set GOOGLE_PROJECT_ID)."},
        )

    if not app_id:
        return _wrap("error", {"message": "app_id is required."})

    if not issue_id:
        return _wrap("error", {"message": "issue_id is required."})

    url = (
        f"https://firebasecrashlytics.googleapis.com/v1alpha/projects/"
        f"{project_id}/apps/{app_id}/issues/{issue_id}"
    )

    try:
        token = _get_access_token([_CRASHLYTICS_SCOPE])
        headers = {"Authorization": f"Bearer {token}"}

        resp = requests.get(url, headers=headers, timeout=30)
        resp.raise_for_status()
        issue = resp.json()

        # Extract affected versions from appVersions list if present.
        affected_versions: list[str] = [
            v.get("displayVersion", v.get("buildVersion", ""))
            for v in issue.get("appVersions", [])
            if v
        ]

        result = {
            "issue_id": issue.get("issueId", issue_id),
            "title": issue.get("title", ""),
            "subtitle": issue.get("subtitle", ""),
            "state": issue.get("state", ""),
            "users_affected": int(issue.get("impactedUsersCount", 0)),
            "events_count": int(issue.get("eventsCount", 0)),
            "first_seen": issue.get("firstSeenTime", ""),
            "last_seen": issue.get("lastActivityTime", ""),
            "platform": issue.get("platform", ""),
            "affected_versions": affected_versions,
        }

        logger.info(
            "firebase_crashlytics_get_issue succeeded: issue_id=%s, state=%s",
            issue_id,
            result["state"],
        )
        return _wrap("ok", result)

    except requests.HTTPError as exc:
        status_code = exc.response.status_code if exc.response is not None else 0
        logger.error(
            "Crashlytics API HTTP error %d for issue %s: %s",
            status_code,
            issue_id,
            exc,
        )
        return _wrap("error", {"message": str(exc), "http_status": status_code})
    except Exception as exc:
        logger.exception("Unexpected error in firebase_crashlytics_get_issue")
        return _wrap("error", {"message": str(exc)})
