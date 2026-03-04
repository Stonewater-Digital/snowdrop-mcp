"""Firebase Hosting — Deploy skill.

Deploys files to a Firebase Hosting site or channel via the Firebase Hosting
REST API v1beta1. Implements the full multi-step flow: create version,
populate files, upload each file, finalize version, and create a release.
Uses ADC-first credentials with GOOGLE_SERVICE_ACCOUNT_JSON fallback.
"""

import base64
import hashlib
import json
import logging
import os
from datetime import datetime, timezone

import httpx

logger = logging.getLogger("snowdrop.firebase_hosting_deploy")

TOOL_META = {
    "name": "firebase_hosting_deploy",
    "description": "Deploy files to a Firebase Hosting site or channel via the Firebase Hosting REST API. Returns the channel URL and release version.",
    "tier": "free",
}

_FIREBASE_HOSTING_SCOPE = "https://www.googleapis.com/auth/firebase"
_HOSTING_BASE = "https://firebasehosting.googleapis.com/v1beta1"
_UPLOAD_BASE = "https://upload.firebasehosting.googleapis.com/upload/v1beta1"


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


def _sha256_of_base64(b64_content: str) -> str:
    """Return the SHA-256 hex digest of the decoded base64 content.

    Args:
        b64_content: Base64-encoded file content string.

    Returns:
        Lowercase hex SHA-256 digest of the decoded bytes.
    """
    raw = base64.b64decode(b64_content)
    return hashlib.sha256(raw).hexdigest()


def _raise_for_status(response: httpx.Response, context: str) -> None:
    """Raise a RuntimeError with context if the HTTP response is an error.

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


def firebase_hosting_deploy(
    site_id: str,
    files: dict[str, str],
    channel_id: str = "live",
) -> dict:
    """Deploy files to a Firebase Hosting site or channel.

    Implements the full Firebase Hosting REST API deploy flow:

    1. Create a new version for the site.
    2. Populate the version with a SHA-256 hash manifest of all files.
    3. Upload any files that Firebase indicates are required.
    4. Finalize the version (set status to FINALIZED).
    5. Create a release pinned to the new version on the specified channel.

    Args:
        site_id: The Firebase Hosting site ID (e.g. ``'my-app'`` for
            ``my-app.web.app``).
        files: A mapping of site-relative URL paths to base64-encoded file
            content. Example::

                {
                    "/index.html": "<base64 string>",
                    "/app.js": "<base64 string>",
                }

        channel_id: The hosting channel to release to. Use ``"live"`` (the
            default) for the production channel, or a custom channel ID for
            preview deployments.

    Returns:
        dict: A result envelope with the following structure::

            {
                "status": "ok",
                "data": {
                    "version_name": str,   # projects/.../sites/.../versions/...
                    "channel_url": str,    # public URL of the channel
                    "release_name": str,   # full resource name of the release
                    "files_uploaded": int, # number of files actually uploaded
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
        RuntimeError: If any Firebase Hosting REST API call fails.
        ValueError: If ``site_id`` is empty or ``files`` is empty.

    Example:
        >>> import base64
        >>> html = base64.b64encode(b"<h1>Hello</h1>").decode()
        >>> result = firebase_hosting_deploy(
        ...     site_id="my-app",
        ...     files={"/index.html": html},
        ...     channel_id="live",
        ... )
        >>> assert result["status"] == "ok"
        >>> print(result["data"]["channel_url"])
    """
    logger.info(
        "firebase_hosting_deploy: entry | site_id=%s channel_id=%s file_count=%d",
        site_id,
        channel_id,
        len(files),
    )
    try:
        if not site_id or not site_id.strip():
            raise ValueError("site_id must be a non-empty string.")
        if not files:
            raise ValueError("files dict must contain at least one entry.")

        token = _get_access_token([_FIREBASE_HOSTING_SCOPE])
        headers = {
            "Authorization": f"Bearer {token}",
            "Content-Type": "application/json",
        }

        # Step 1: Create a new version
        logger.info("firebase_hosting_deploy: creating version for site=%s", site_id)
        create_url = f"{_HOSTING_BASE}/sites/{site_id}/versions"
        create_payload = {
            "config": {
                "headers": [{"glob": "**", "headers": {"Cache-Control": "max-age=3600"}}]
            }
        }
        with httpx.Client(timeout=30) as client:
            resp = client.post(create_url, headers=headers, json=create_payload)
            _raise_for_status(resp, "Create version")
            version_data = resp.json()

        version_name: str = version_data["name"]
        logger.info("firebase_hosting_deploy: version created | version_name=%s", version_name)

        # Build SHA-256 hash map: path -> sha256 of decoded content
        file_hashes: dict[str, str] = {
            path: _sha256_of_base64(b64) for path, b64 in files.items()
        }

        # Step 2: Populate files (send hash manifest, get back list of required uploads)
        logger.info("firebase_hosting_deploy: populating files | version=%s", version_name)
        populate_url = f"{_HOSTING_BASE}/{version_name}:populateFiles"
        populate_payload = {"files": file_hashes}
        with httpx.Client(timeout=30) as client:
            resp = client.post(populate_url, headers=headers, json=populate_payload)
            _raise_for_status(resp, "Populate files")
            populate_data = resp.json()

        upload_url: str = populate_data.get("uploadUrl", "")
        required_hashes: list[str] = populate_data.get("uploadRequiredHashes", [])
        logger.info(
            "firebase_hosting_deploy: %d files required for upload",
            len(required_hashes),
        )

        # Build a reverse map: sha256 -> (path, b64_content)
        hash_to_file: dict[str, tuple[str, str]] = {
            sha: (path, b64) for path, b64 in files.items()
            for sha in [file_hashes[path]]
        }

        # Step 3: Upload each required file
        files_uploaded = 0
        for file_hash in required_hashes:
            if file_hash not in hash_to_file:
                logger.warning(
                    "firebase_hosting_deploy: hash %s not found in local files, skipping",
                    file_hash,
                )
                continue
            _path, b64_content = hash_to_file[file_hash]
            raw_bytes = base64.b64decode(b64_content)
            file_upload_url = f"{upload_url}/{file_hash}"
            upload_headers = {
                "Authorization": f"Bearer {token}",
                "Content-Type": "application/octet-stream",
            }
            logger.info(
                "firebase_hosting_deploy: uploading file hash=%s path=%s",
                file_hash,
                _path,
            )
            with httpx.Client(timeout=60) as client:
                resp = client.post(file_upload_url, headers=upload_headers, content=raw_bytes)
                _raise_for_status(resp, f"Upload file {_path}")
            files_uploaded += 1

        # Step 4: Finalize the version
        logger.info("firebase_hosting_deploy: finalizing version=%s", version_name)
        patch_url = f"{_HOSTING_BASE}/{version_name}?updateMask=status"
        finalize_payload = {"status": "FINALIZED"}
        with httpx.Client(timeout=30) as client:
            resp = client.patch(patch_url, headers=headers, json=finalize_payload)
            _raise_for_status(resp, "Finalize version")

        # Step 5: Create a release on the specified channel
        logger.info(
            "firebase_hosting_deploy: creating release | site=%s channel=%s version=%s",
            site_id,
            channel_id,
            version_name,
        )
        release_url = (
            f"{_HOSTING_BASE}/sites/{site_id}/channels/{channel_id}/releases"
            f"?versionName={version_name}"
        )
        with httpx.Client(timeout=30) as client:
            resp = client.post(release_url, headers=headers, json={})
            _raise_for_status(resp, "Create release")
            release_data = resp.json()

        release_name: str = release_data.get("name", "")
        channel_url: str = release_data.get("channel", {}).get("url", "")
        if not channel_url:
            # Construct a sensible default URL when the API doesn't return one
            if channel_id == "live":
                channel_url = f"https://{site_id}.web.app"
            else:
                channel_url = f"https://{site_id}--{channel_id}.web.app"

        result = {
            "status": "ok",
            "data": {
                "version_name": version_name,
                "channel_url": channel_url,
                "release_name": release_name,
                "files_uploaded": files_uploaded,
            },
            "timestamp": _now(),
        }
        logger.info(
            "firebase_hosting_deploy: exit | version=%s channel_url=%s files_uploaded=%d",
            version_name,
            channel_url,
            files_uploaded,
        )
        return result

    except (ValueError, RuntimeError) as exc:
        logger.error("firebase_hosting_deploy: error | %s", exc)
        return {"status": "error", "data": {"error": str(exc)}, "timestamp": _now()}
    except Exception as exc:
        logger.exception("firebase_hosting_deploy: unexpected error | %s", exc)
        return {"status": "error", "data": {"error": str(exc)}, "timestamp": _now()}
