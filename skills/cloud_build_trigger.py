"""
Executive Summary
-----------------
Manually triggers a Google Cloud Build build from a configured trigger ID, targeting
a specified branch. Returns the resulting build ID, initial status, and a direct link
to the Cloud Console log URL for monitoring. Useful for programmatic CI/CD automation
without requiring gcloud CLI access.

Credentials resolved ADC-first (Cloud Run), then GOOGLE_SERVICE_ACCOUNT_JSON (local dev).

Inputs:
  trigger_id    : str | None  — Cloud Build trigger ID (required unless listing)
  project_id    : str | None  — GCP project ID (falls back to GOOGLE_PROJECT_ID env)
  region        : str         — Cloud Build region, default "global"
  branch        : str         — git branch to build, default "main"
  substitutions : dict | None — user-defined substitution variables (e.g. _ENV=prod)

Outputs:
  {"status": "ok"|"error", "data": {...}, "timestamp": "<ISO8601>"}

MCP Tool Name: cloud_build_trigger

Agent Notes:
  - Required IAM: roles/cloudbuild.builds.editor
  - The trigger must already exist in Cloud Build; this skill fires it, not creates it.
  - For regional triggers use the region where the trigger was created (not "global").
  - substitutions keys must start with underscore per Cloud Build convention (e.g. _TAG).
  - The returned build_id can be used to poll build status via the Cloud Build API.
"""

import json
import logging
import os
from datetime import datetime, timezone

import requests

logger = logging.getLogger("snowdrop.cloud_build_trigger")

TOOL_META = {
    "name": "cloud_build_trigger",
    "description": (
        "Manually trigger a Google Cloud Build build from a trigger ID or repo/branch. "
        "Returns the build ID and log URL for monitoring."
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


def cloud_build_trigger(
    trigger_id: str | None = None,
    project_id: str | None = None,
    region: str = "global",
    branch: str = "main",
    substitutions: dict | None = None,
) -> dict:
    """Manually run a Google Cloud Build trigger against a specified branch.

    Sends a ``POST`` request to the Cloud Build ``triggers.run`` endpoint for the
    given trigger ID, instructing Cloud Build to start a new build from the
    specified branch. Substitution variables can be passed to override any
    ``_USER_DEFINED`` variables configured on the trigger.

    Args:
        trigger_id: Cloud Build trigger ID (UUID). Required. Visible in the
            Cloud Console under Cloud Build > Triggers or via
            ``gcloud builds triggers list``.
        project_id: GCP project ID. Defaults to the ``GOOGLE_PROJECT_ID``
            environment variable when not provided.
        region: Region of the Cloud Build trigger. Use ``"global"`` for
            triggers not scoped to a specific region. Defaults to ``"global"``.
        branch: Git branch name to build. Defaults to ``"main"``.
        substitutions: Optional dict of user-defined substitution variables to
            pass to the build. Keys must follow Cloud Build conventions and
            start with ``_`` (e.g. ``{"_ENV": "production", "_TAG": "v1.2.3"}``).

    Returns:
        dict with keys:
            - status (str): ``"ok"`` or ``"error"``.
            - data (dict): Contains ``build_id`` (str), ``status`` (str),
              ``log_url`` (str linking to Cloud Console), ``create_time`` (str),
              and ``trigger_id`` (str).
            - timestamp (str): ISO 8601 UTC execution timestamp.

    Raises:
        Does not raise; all exceptions are caught and returned as error dicts.

    Example:
        >>> result = cloud_build_trigger(
        ...     trigger_id="abc12345-0000-0000-0000-def678901234",
        ...     project_id="my-gcp-project",
        ...     branch="release/v2",
        ...     substitutions={"_ENV": "staging"},
        ... )
        >>> result["status"]
        'ok'
        >>> result["data"]["build_id"]  # some UUID string
        'xxxxxxxx-...'
    """
    logger.info(
        "cloud_build_trigger: entry trigger_id=%s project=%s region=%s branch=%s",
        trigger_id,
        project_id,
        region,
        branch,
    )

    project_id = project_id or os.environ.get("GOOGLE_PROJECT_ID", "")
    if not project_id:
        logger.error("cloud_build_trigger: project_id missing")
        return {
            "status": "error",
            "data": {"message": "project_id is required or set GOOGLE_PROJECT_ID"},
            "timestamp": _now(),
        }

    if not trigger_id:
        logger.error("cloud_build_trigger: trigger_id missing")
        return {
            "status": "error",
            "data": {"message": "trigger_id is required"},
            "timestamp": _now(),
        }

    try:
        token = _get_access_token([_CLOUD_PLATFORM_SCOPE])
        headers = {
            "Authorization": f"Bearer {token}",
            "Content-Type": "application/json",
        }

        url = (
            f"https://cloudbuild.googleapis.com/v1"
            f"/projects/{project_id}/locations/{region}"
            f"/triggers/{trigger_id}:run"
        )

        body: dict = {
            "source": {"branchName": branch},
            "substitutions": substitutions or {},
        }

        logger.info("cloud_build_trigger: POST %s branch=%s", url, branch)
        resp = requests.post(url, headers=headers, json=body, timeout=30)

        if resp.status_code not in (200, 202):
            logger.error(
                "cloud_build_trigger: API error %d: %s",
                resp.status_code,
                resp.text[:400],
            )
            return {
                "status": "error",
                "data": {
                    "message": f"Cloud Build API returned {resp.status_code}",
                    "detail": resp.text[:400],
                },
                "timestamp": _now(),
            }

        response_body = resp.json()

        # The API returns an Operation or directly a Build depending on the trigger type.
        # Unwrap Operation if present.
        build_data: dict = response_body
        if "metadata" in response_body and "build" in response_body.get("metadata", {}):
            build_data = response_body["metadata"]["build"]
        elif "response" in response_body:
            build_data = response_body.get("response", response_body)

        build_id: str = build_data.get("id", response_body.get("name", "").split("/")[-1])
        build_status: str = build_data.get("status", "QUEUED")
        create_time: str = build_data.get("createTime", "")

        # Construct human-readable log URL
        log_url: str = (
            build_data.get("logUrl")
            or f"https://console.cloud.google.com/cloud-build/builds/{build_id}?project={project_id}"
        )

        logger.info(
            "cloud_build_trigger: exit success build_id=%s status=%s",
            build_id,
            build_status,
        )

        return {
            "status": "ok",
            "data": {
                "build_id": build_id,
                "status": build_status,
                "log_url": log_url,
                "create_time": create_time,
                "trigger_id": trigger_id,
                "branch": branch,
                "project_id": project_id,
                "region": region,
            },
            "timestamp": _now(),
        }

    except Exception as exc:
        logger.error("cloud_build_trigger: unexpected error: %s", exc, exc_info=True)
        return {
            "status": "error",
            "data": {"message": str(exc)},
            "timestamp": _now(),
        }
