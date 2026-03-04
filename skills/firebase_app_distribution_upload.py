"""Firebase App Distribution — Upload skill.

Uploads a build artifact to Firebase App Distribution and optionally notifies
testers or groups. Uses the Firebase App Distribution REST API v1 with
ADC-first credentials and GOOGLE_SERVICE_ACCOUNT_JSON fallback.
"""

import base64
import json
import logging
import os
from datetime import datetime, timezone

import httpx

logger = logging.getLogger("snowdrop.firebase_app_distribution_upload")

TOOL_META = {
    "name": "firebase_app_distribution_upload",
    "description": "Upload a build artifact to Firebase App Distribution and notify testers. Returns the release name and download URL.",
    "tier": "free",
}

_SCOPE = "https://www.googleapis.com/auth/cloud-platform"
_FAD_BASE = "https://firebaseappdistribution.googleapis.com/v1"
_FAD_UPLOAD_BASE = "https://firebaseappdistribution.googleapis.com/upload/v1"


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


def _raise_for_status(response: httpx.Response, context: str) -> None:
    """Raise RuntimeError with context if the HTTP response is an error.

    Args:
        response: The httpx response object.
        context: A short description of the API call being made.

    Raises:
        RuntimeError: If the status code indicates an HTTP error.
    """
    if response.is_error:
        raise RuntimeError(
            f"{context} failed with HTTP {response.status_code}: {response.text}"
        )


def firebase_app_distribution_upload(
    app_id: str,
    binary_base64: str,
    release_notes: str = "",
    tester_emails: list[str] | None = None,
    group_aliases: list[str] | None = None,
) -> dict:
    """Upload a build artifact to Firebase App Distribution and notify testers.

    The upload flow uses the Firebase App Distribution REST API v1:

    1. POST the binary to the upload endpoint using a multipart or binary
       upload. The API returns an ``Operation`` resource that is polled until
       it completes.
    2. Once the operation is done, extract the release resource name and
       binary download URI from the operation response.
    3. If ``tester_emails`` or ``group_aliases`` are provided, distribute the
       release to those recipients via the distribute endpoint.

    Args:
        app_id: The Firebase App ID in the format
            ``1:PROJECT_NUMBER:PLATFORM:APP_ID_HASH``
            (e.g. ``'1:123456789:android:abcdef1234567890'``).
        binary_base64: Base64-encoded content of the APK, IPA, or AAB file
            to upload.
        release_notes: Optional release notes displayed to testers in the
            App Distribution console and notifications.
        tester_emails: Optional list of tester email addresses to notify.
        group_aliases: Optional list of tester group aliases to notify.

    Returns:
        dict: A result envelope with the following structure::

            {
                "status": "ok",
                "data": {
                    "release_name": str,          # full resource name of the release
                    "binary_download_uri": str,   # pre-signed download URL
                    "release_notes": str,
                    "testers_notified": int,
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
        RuntimeError: If any Firebase App Distribution REST API call fails.
        ValueError: If ``app_id`` is empty or ``binary_base64`` is empty.

    Example:
        >>> import base64, pathlib
        >>> apk_bytes = pathlib.Path("app-debug.apk").read_bytes()
        >>> result = firebase_app_distribution_upload(
        ...     app_id="1:123456789:android:abcdef",
        ...     binary_base64=base64.b64encode(apk_bytes).decode(),
        ...     release_notes="Build 42 — fixed crash on startup",
        ...     tester_emails=["tester@example.com"],
        ... )
        >>> assert result["status"] == "ok"
        >>> print(result["data"]["release_name"])
    """
    logger.info(
        "firebase_app_distribution_upload: entry | app_id=%s release_notes_len=%d",
        app_id,
        len(release_notes),
    )
    try:
        if not app_id or not app_id.strip():
            raise ValueError("app_id must be a non-empty string.")
        if not binary_base64 or not binary_base64.strip():
            raise ValueError("binary_base64 must be a non-empty string.")

        project_id = os.environ.get("GOOGLE_PROJECT_ID", "")
        if not project_id:
            raise ValueError(
                "GOOGLE_PROJECT_ID environment variable is required for App Distribution."
            )

        token = _get_access_token([_SCOPE])
        auth_headers = {"Authorization": f"Bearer {token}"}

        binary_bytes = base64.b64decode(binary_base64)

        # Step 1: Upload binary — returns a long-running Operation
        upload_url = (
            f"{_FAD_UPLOAD_BASE}/projects/{project_id}/apps/{app_id}/releases:upload"
        )
        upload_headers = {
            **auth_headers,
            "Content-Type": "application/octet-stream",
            "X-Goog-Upload-Protocol": "raw",
        }
        logger.info(
            "firebase_app_distribution_upload: uploading binary | size_bytes=%d",
            len(binary_bytes),
        )
        with httpx.Client(timeout=120) as client:
            resp = client.post(upload_url, headers=upload_headers, content=binary_bytes)
            _raise_for_status(resp, "Upload binary")
            operation: dict = resp.json()

        # The upload returns an Operation. Poll until done.
        operation_name: str = operation.get("name", "")
        logger.info(
            "firebase_app_distribution_upload: polling operation | name=%s",
            operation_name,
        )

        max_polls = 20
        poll_interval = 3  # seconds
        import time

        final_op: dict = operation
        for attempt in range(max_polls):
            if final_op.get("done", False):
                break
            if attempt > 0:
                time.sleep(poll_interval)
            op_url = f"https://firebaseappdistribution.googleapis.com/v1/{operation_name}"
            with httpx.Client(timeout=30) as client:
                poll_resp = client.get(op_url, headers=auth_headers)
                _raise_for_status(poll_resp, f"Poll operation (attempt {attempt + 1})")
                final_op = poll_resp.json()
            logger.info(
                "firebase_app_distribution_upload: operation poll attempt=%d done=%s",
                attempt + 1,
                final_op.get("done", False),
            )

        if not final_op.get("done", False):
            raise RuntimeError(
                f"Operation {operation_name} did not complete after {max_polls} polls."
            )

        if "error" in final_op:
            raise RuntimeError(
                f"Operation failed: {final_op['error']}"
            )

        release_resource: dict = final_op.get("response", {})
        release_name: str = release_resource.get("name", "")
        binary_download_uri: str = release_resource.get("binaryDownloadUri", "")

        # Step 2: Update release notes if provided
        if release_notes and release_name:
            notes_url = f"{_FAD_BASE}/{release_name}?updateMask=releaseNotes.text"
            notes_payload = {"releaseNotes": {"text": release_notes}}
            notes_headers = {**auth_headers, "Content-Type": "application/json"}
            with httpx.Client(timeout=30) as client:
                resp = client.patch(notes_url, headers=notes_headers, json=notes_payload)
                _raise_for_status(resp, "Update release notes")

        # Step 3: Distribute to testers and/or groups
        testers_notified = 0
        recipients: dict = {}
        if tester_emails:
            recipients["testerEmails"] = tester_emails
            testers_notified += len(tester_emails)
        if group_aliases:
            recipients["groupAliases"] = group_aliases

        if recipients and release_name:
            distribute_url = f"{_FAD_BASE}/{release_name}:distribute"
            dist_headers = {**auth_headers, "Content-Type": "application/json"}
            logger.info(
                "firebase_app_distribution_upload: distributing | tester_emails=%s groups=%s",
                tester_emails,
                group_aliases,
            )
            with httpx.Client(timeout=30) as client:
                resp = client.post(distribute_url, headers=dist_headers, json=recipients)
                _raise_for_status(resp, "Distribute release")

        result = {
            "status": "ok",
            "data": {
                "release_name": release_name,
                "binary_download_uri": binary_download_uri,
                "release_notes": release_notes,
                "testers_notified": testers_notified,
            },
            "timestamp": _now(),
        }
        logger.info(
            "firebase_app_distribution_upload: exit | release_name=%s testers_notified=%d",
            release_name,
            testers_notified,
        )
        return result

    except (ValueError, RuntimeError) as exc:
        logger.error("firebase_app_distribution_upload: error | %s", exc)
        return {"status": "error", "data": {"error": str(exc)}, "timestamp": _now()}
    except Exception as exc:
        logger.exception("firebase_app_distribution_upload: unexpected error | %s", exc)
        return {"status": "error", "data": {"error": str(exc)}, "timestamp": _now()}
