"""
Executive Summary
-----------------
Lists active Firebase In-App Messaging campaigns for a GCP project using the
Firebase In-App Messaging REST API v1alpha. Returns campaign name, title, body,
image URL, trigger conditions, and status. Credentials are resolved via ADC on
Cloud Run or via GOOGLE_SERVICE_ACCOUNT_JSON for local and Railway deployments.
Handles gracefully the case where the API is disabled or returns 404.

Credentials resolved in order:
  1. GOOGLE_SERVICE_ACCOUNT_JSON  — raw JSON string (Cloud Run / Railway / Fly.io)
  2. ADC (Application Default Credentials) — used automatically on Cloud Run

Inputs:
  project_id : str  — GCP project ID (falls back to GOOGLE_PROJECT_ID env)
  page_size  : int  — max campaigns to return (default 20)

Outputs:
  {"status": "ok"|"error", "data": {...}, "timestamp": "<ISO8601>"}

MCP Tool Name: firebase_in_app_messaging_list

Agent Notes (Claude Code / Cursor / Codex CLI / Gemini CLI):
  - Required IAM role: roles/firebase.viewer or roles/cloudplatform.viewer
  - The In-App Messaging API must be enabled in the Firebase project
  - If the API is not enabled a helpful error is returned, not a raw exception
  - Trigger types include: ON_FOREGROUND, ON_ANALYTICS_EVENT, MANUAL
"""

import json
import logging
import os
from datetime import datetime, timezone

import requests

logger = logging.getLogger("snowdrop.firebase_in_app_messaging_list")

TOOL_META = {
    "name": "firebase_in_app_messaging_list",
    "description": (
        "List active Firebase In-App Messaging campaigns for a project. "
        "Returns campaign names, trigger conditions, and message content."
    ),
    "tier": "free",
}

_FIAM_SCOPE = "https://www.googleapis.com/auth/cloud-platform"


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


def firebase_in_app_messaging_list(
    project_id: str | None = None,
    page_size: int = 20,
) -> dict:
    """List active Firebase In-App Messaging campaigns for a project.

    Args:
        project_id: GCP project ID. Falls back to GOOGLE_PROJECT_ID env var
            if not supplied.
        page_size: Maximum number of campaigns to return per page.
            Defaults to 20.

    Returns:
        dict: Standard Snowdrop envelope::

            {
                "status": "ok",
                "data": {
                    "campaigns": [
                        {
                            "name": str,
                            "title": str,
                            "body": str,
                            "image_url": str,
                            "trigger": str,
                            "status": str
                        },
                        ...
                    ],
                    "count": int,
                    "project_id": str
                },
                "timestamp": "<ISO8601>"
            }

    Raises:
        RuntimeError: If no GCP credentials are available.

    Example:
        >>> result = firebase_in_app_messaging_list(
        ...     project_id="my-firebase-project",
        ...     page_size=10,
        ... )
        >>> print(result["data"]["count"])
        2
    """
    logger.info(
        "firebase_in_app_messaging_list called: project_id=%s, page_size=%d",
        project_id,
        page_size,
    )

    project_id = project_id or os.environ.get("GOOGLE_PROJECT_ID", "")
    if not project_id:
        return _wrap(
            "error",
            {"message": "project_id is required (or set GOOGLE_PROJECT_ID)."},
        )

    page_size = min(max(1, page_size), 100)

    url = (
        f"https://firebaseinappmessaging.googleapis.com/v1/projects/"
        f"{project_id}/inAppMessages"
    )
    params: dict[str, object] = {"pageSize": page_size}

    try:
        token = _get_access_token([_FIAM_SCOPE])
        headers = {"Authorization": f"Bearer {token}"}

        resp = requests.get(url, params=params, headers=headers, timeout=30)

        # Graceful handling for API-not-enabled or project-not-found.
        if resp.status_code == 404:
            logger.warning(
                "Firebase In-App Messaging API returned 404 for project %s. "
                "Ensure the API is enabled: "
                "https://console.firebase.google.com/project/%s/inappmessaging",
                project_id,
                project_id,
            )
            return _wrap(
                "error",
                {
                    "message": (
                        "Firebase In-App Messaging API returned 404. "
                        "Ensure the Firebase In-App Messaging API is enabled for "
                        f"project '{project_id}' and that the project ID is correct. "
                        "Enable it at: "
                        f"https://console.firebase.google.com/project/{project_id}/inappmessaging"
                    ),
                    "http_status": 404,
                },
            )

        resp.raise_for_status()
        body = resp.json()

        raw_messages = body.get("inAppMessages", [])
        campaigns = []
        for msg in raw_messages:
            # Nested message content lives inside msg["messageConfig"]["messagePayload"]
            msg_config = msg.get("messageConfig", {})
            payload = msg_config.get("messagePayload", {})
            banner = payload.get("bannerMessage", {})
            modal = payload.get("modalMessage", {})
            card = payload.get("cardMessage", {})
            image_only = payload.get("imageOnlyMessage", {})

            # Prefer banner → modal → card → image_only for title/body extraction
            content = banner or modal or card or image_only
            action_url = (
                content.get("action", {}).get("actionUrl", "")
                if isinstance(content.get("action"), dict)
                else ""
            )

            trigger_raw = msg_config.get("trigger", {})
            trigger_type = (
                trigger_raw.get("firesOnEventType", "ON_FOREGROUND")
                if isinstance(trigger_raw, dict)
                else str(trigger_raw)
            )

            campaigns.append(
                {
                    "name": msg.get("name", ""),
                    "title": content.get("title", {}).get("text", ""),
                    "body": content.get("body", {}).get("text", ""),
                    "image_url": content.get("imageUrl", ""),
                    "action_url": action_url,
                    "trigger": trigger_type,
                    "status": msg.get("renderingConfig", {}).get(
                        "displayConfig", "ACTIVE"
                    ),
                }
            )

        logger.info(
            "firebase_in_app_messaging_list returned %d campaigns for project %s",
            len(campaigns),
            project_id,
        )
        return _wrap(
            "ok",
            {
                "campaigns": campaigns,
                "count": len(campaigns),
                "project_id": project_id,
            },
        )

    except requests.HTTPError as exc:
        status_code = exc.response.status_code if exc.response is not None else 0
        logger.error(
            "Firebase In-App Messaging API HTTP error %d: %s",
            status_code,
            exc,
        )
        return _wrap("error", {"message": str(exc), "http_status": status_code})
    except Exception as exc:
        logger.exception("Unexpected error in firebase_in_app_messaging_list")
        return _wrap("error", {"message": str(exc)})
