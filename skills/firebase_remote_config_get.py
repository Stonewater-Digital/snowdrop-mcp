"""Firebase Remote Config — Get Template skill.

Retrieves the current Firebase Remote Config template for a project, including
all parameters, parameter groups, conditions, and version metadata. Uses the
Firebase Remote Config REST API v1 with ADC-first credentials and
GOOGLE_SERVICE_ACCOUNT_JSON fallback.
"""

import json
import logging
import os
from datetime import datetime, timezone

import httpx

logger = logging.getLogger("snowdrop.firebase_remote_config_get")

TOOL_META = {
    "name": "firebase_remote_config_get",
    "description": "Get the current Firebase Remote Config template, including all parameters, parameter groups, and conditions.",
    "tier": "free",
}

_SCOPE = "https://www.googleapis.com/auth/firebase.remoteconfig"
_FRC_BASE = "https://firebaseremoteconfig.googleapis.com/v1"


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


def firebase_remote_config_get(project_id: str | None = None) -> dict:
    """Get the current Firebase Remote Config template.

    Fetches the active Remote Config template for the specified project,
    returning all parameters, parameter groups, conditions, and the current
    version metadata. Also returns the ETag header value, which is required
    for conditional writes via ``firebase_remote_config_set``.

    Args:
        project_id: The GCP project ID. Defaults to the value of the
            ``GOOGLE_PROJECT_ID`` environment variable when not provided.

    Returns:
        dict: A result envelope with the following structure::

            {
                "status": "ok",
                "data": {
                    "parameters": dict,         # key -> parameter definition
                    "parameter_groups": dict,   # group name -> group definition
                    "conditions": list[dict],   # list of condition objects
                    "version": {
                        "version_number": str,
                        "update_time": str,
                        "update_origin": str,
                        "update_type": str,
                        "update_user": dict | None,
                    },
                    "etag": str,  # ETag for conditional writes
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
        RuntimeError: If the Firebase Remote Config REST API call fails.
        ValueError: If no project ID is available from the argument or
            environment.

    Example:
        >>> result = firebase_remote_config_get()
        >>> assert result["status"] == "ok"
        >>> print(result["data"]["version"]["version_number"])
        >>> for name, param in result["data"]["parameters"].items():
        ...     print(name, param.get("defaultValue", {}).get("value"))
    """
    logger.info(
        "firebase_remote_config_get: entry | project_id=%s",
        project_id or "(from env)",
    )
    try:
        resolved_project_id = project_id or os.environ.get("GOOGLE_PROJECT_ID", "")
        if not resolved_project_id:
            raise ValueError(
                "project_id must be provided or GOOGLE_PROJECT_ID must be set."
            )

        token = _get_access_token([_SCOPE])
        headers = {
            "Authorization": f"Bearer {token}",
            "Accept-Encoding": "gzip",
        }

        url = f"{_FRC_BASE}/projects/{resolved_project_id}/remoteConfig"
        logger.info("firebase_remote_config_get: fetching config | url=%s", url)

        with httpx.Client(timeout=30) as client:
            resp = client.get(url, headers=headers)
            if resp.is_error:
                raise RuntimeError(
                    f"Get Remote Config failed with HTTP {resp.status_code}: {resp.text}"
                )
            etag: str = resp.headers.get("etag", "")
            data: dict = resp.json()

        version_info: dict = data.get("version", {})
        version_user: dict | None = version_info.get("updateUser")

        result = {
            "status": "ok",
            "data": {
                "parameters": data.get("parameters", {}),
                "parameter_groups": data.get("parameterGroups", {}),
                "conditions": data.get("conditions", []),
                "version": {
                    "version_number": version_info.get("versionNumber", ""),
                    "update_time": version_info.get("updateTime", ""),
                    "update_origin": version_info.get("updateOrigin", ""),
                    "update_type": version_info.get("updateType", ""),
                    "update_user": version_user,
                },
                "etag": etag,
            },
            "timestamp": _now(),
        }
        logger.info(
            "firebase_remote_config_get: exit | project_id=%s version=%s param_count=%d",
            resolved_project_id,
            version_info.get("versionNumber", ""),
            len(data.get("parameters", {})),
        )
        return result

    except (ValueError, RuntimeError) as exc:
        logger.error("firebase_remote_config_get: error | %s", exc)
        return {"status": "error", "data": {"error": str(exc)}, "timestamp": _now()}
    except Exception as exc:
        logger.exception("firebase_remote_config_get: unexpected error | %s", exc)
        return {"status": "error", "data": {"error": str(exc)}, "timestamp": _now()}
