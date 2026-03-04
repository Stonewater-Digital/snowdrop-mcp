"""
Executive Summary
-----------------
Lists crash issues from Firebase Crashlytics for a given mobile app using the
Crashlytics REST API v1alpha1. Returns issue ID, title, impact (users affected),
event count, and last occurrence time. Credentials are resolved via ADC on Cloud
Run or via GOOGLE_SERVICE_ACCOUNT_JSON for local and Railway deployments.

Credentials resolved in order:
  1. GOOGLE_SERVICE_ACCOUNT_JSON  — raw JSON string (Cloud Run / Railway / Fly.io)
  2. ADC (Application Default Credentials) — used automatically on Cloud Run

Inputs:
  app_id      : str  — Firebase App ID (e.g. "1:123456789:android:abc123")  (required)
  project_id  : str  — GCP project ID (falls back to GOOGLE_PROJECT_ID env)
  page_size   : int  — max issues to return (default 20)
  state       : str  — "open" | "closed" (default "open")

Outputs:
  {"status": "ok"|"error", "data": {...}, "timestamp": "<ISO8601>"}

MCP Tool Name: firebase_crashlytics_list_issues

Agent Notes (Claude Code / Cursor / Codex CLI / Gemini CLI):
  - Required IAM role: roles/firebase.viewer or roles/cloudplatform.viewer
  - app_id is visible in Firebase Console → Project Settings → Your Apps
  - state filter is uppercased automatically before sending to the API
  - page_size max is 100 per Crashlytics API limits
"""

import json
import logging
import os
from datetime import datetime, timezone

import requests

logger = logging.getLogger("snowdrop.firebase_crashlytics_list_issues")

TOOL_META = {
    "name": "firebase_crashlytics_list_issues",
    "description": (
        "List crash issues from Firebase Crashlytics for a given app. "
        "Returns issue ID, title, impact (users affected), and last occurrence time."
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


def firebase_crashlytics_list_issues(
    app_id: str,
    project_id: str | None = None,
    page_size: int = 20,
    state: str = "open",
) -> dict:
    """List crash issues from Firebase Crashlytics for a specific app.

    Args:
        app_id: Firebase App ID (e.g. "1:123456789:android:abc123def456").
            Visible in Firebase Console → Project Settings → Your Apps.
        project_id: GCP project ID. Falls back to GOOGLE_PROJECT_ID env var
            if not supplied.
        page_size: Maximum number of issues to return. Capped at 100 by the
            Crashlytics API. Defaults to 20.
        state: Filter by issue state. One of "open" or "closed". The value is
            uppercased before being sent to the API. Defaults to "open".

    Returns:
        dict: Standard Snowdrop envelope::

            {
                "status": "ok",
                "data": {
                    "issues": [
                        {
                            "issue_id": str,
                            "title": str,
                            "subtitle": str,
                            "users_affected": int,
                            "events_count": int,
                            "last_activity_time": str,
                            "state": str
                        },
                        ...
                    ],
                    "count": int,
                    "app_id": str,
                    "project_id": str
                },
                "timestamp": "<ISO8601>"
            }

    Raises:
        RuntimeError: If no GCP credentials are available.
        requests.HTTPError: If the Crashlytics API returns a non-2xx response.

    Example:
        >>> result = firebase_crashlytics_list_issues(
        ...     app_id="1:123456789012:android:abc123def456",
        ...     project_id="my-gcp-project",
        ...     page_size=10,
        ...     state="open",
        ... )
        >>> print(result["data"]["count"])
        3
    """
    logger.info(
        "firebase_crashlytics_list_issues called: app_id=%s, state=%s, page_size=%d",
        app_id,
        state,
        page_size,
    )

    project_id = project_id or os.environ.get("GOOGLE_PROJECT_ID", "")
    if not project_id:
        return _wrap(
            "error",
            {"message": "project_id is required (or set GOOGLE_PROJECT_ID)."},
        )

    if not app_id:
        return _wrap("error", {"message": "app_id is required."})

    page_size = min(max(1, page_size), 100)
    state_filter = f'state="{state.upper()}"'

    url = (
        f"https://firebasecrashlytics.googleapis.com/v1alpha/projects/"
        f"{project_id}/apps/{app_id}/issues"
    )
    params: dict[str, object] = {
        "pageSize": page_size,
        "filter": state_filter,
    }

    try:
        token = _get_access_token([_CRASHLYTICS_SCOPE])
        headers = {"Authorization": f"Bearer {token}"}

        resp = requests.get(url, params=params, headers=headers, timeout=30)
        resp.raise_for_status()
        body = resp.json()

        raw_issues = body.get("issues", [])
        issues = []
        for issue in raw_issues:
            issues.append(
                {
                    "issue_id": issue.get("issueId", ""),
                    "title": issue.get("title", ""),
                    "subtitle": issue.get("subtitle", ""),
                    "users_affected": int(issue.get("impactedUsersCount", 0)),
                    "events_count": int(issue.get("eventsCount", 0)),
                    "last_activity_time": issue.get("lastActivityTime", ""),
                    "state": issue.get("state", ""),
                }
            )

        logger.info(
            "firebase_crashlytics_list_issues returned %d issues for app %s",
            len(issues),
            app_id,
        )
        return _wrap(
            "ok",
            {
                "issues": issues,
                "count": len(issues),
                "app_id": app_id,
                "project_id": project_id,
            },
        )

    except requests.HTTPError as exc:
        status_code = exc.response.status_code if exc.response is not None else 0
        logger.error(
            "Crashlytics API HTTP error %d for app %s: %s",
            status_code,
            app_id,
            exc,
        )
        return _wrap(
            "error",
            {"message": str(exc), "http_status": status_code},
        )
    except Exception as exc:
        logger.exception("Unexpected error in firebase_crashlytics_list_issues")
        return _wrap("error", {"message": str(exc)})
