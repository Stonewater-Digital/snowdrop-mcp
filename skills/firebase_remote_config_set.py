"""Firebase Remote Config — Set Template skill.

Publishes a new Firebase Remote Config template by merging provided parameters
with the existing configuration. Uses an ETag-based conditional write to
prevent conflicting updates. Uses the Firebase Remote Config REST API v1 with
ADC-first credentials and GOOGLE_SERVICE_ACCOUNT_JSON fallback.
"""

import json
import logging
import os
from datetime import datetime, timezone

import httpx

logger = logging.getLogger("snowdrop.firebase_remote_config_set")

TOOL_META = {
    "name": "firebase_remote_config_set",
    "description": "Publish a new Firebase Remote Config template. Merges provided parameters with existing config. Returns the new version number and update time.",
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


def firebase_remote_config_set(
    parameters: dict,
    conditions: list[dict] | None = None,
    project_id: str | None = None,
) -> dict:
    """Publish a new Firebase Remote Config template.

    Performs a safe read-modify-write cycle:

    1. GET the current Remote Config template to obtain the current ETag and
       existing parameters, parameter groups, and conditions.
    2. Deep-merge ``parameters`` into the existing parameters dict so that
       existing keys not present in the new payload are preserved.
    3. If ``conditions`` is provided it *replaces* the existing conditions
       list entirely (matching Firebase API semantics).
    4. PUT the merged template back using ``If-Match: <etag>`` to prevent
       conflicting concurrent writes.

    Args:
        parameters: A dict of Remote Config parameter objects to set or
            update. Each key is the parameter name; values must conform to the
            Firebase RemoteConfigParameter schema, e.g.::

                {
                    "welcome_message": {
                        "defaultValue": {"value": "Hello!"},
                        "description": "Greeting shown on home screen",
                        "valueType": "STRING",
                    }
                }

        conditions: Optional list of condition objects that *replace* the
            existing conditions. If ``None``, existing conditions are
            preserved unchanged. Each condition must conform to the Firebase
            RemoteConfigCondition schema.
        project_id: The GCP project ID. Defaults to the value of the
            ``GOOGLE_PROJECT_ID`` environment variable when not provided.

    Returns:
        dict: A result envelope with the following structure::

            {
                "status": "ok",
                "data": {
                    "new_version": str,     # version number after the write
                    "update_time": str,     # ISO 8601 UTC from API response
                    "update_origin": str,   # e.g. "REST_API"
                    "parameters_set": int,  # number of parameters in final template
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
        RuntimeError: If any Firebase Remote Config REST API call fails,
            including HTTP 412 Precondition Failed (ETag conflict).
        ValueError: If ``parameters`` is not a dict, or if no project ID is
            available from the argument or environment.

    Example:
        >>> result = firebase_remote_config_set(
        ...     parameters={
        ...         "feature_dark_mode": {
        ...             "defaultValue": {"value": "false"},
        ...             "valueType": "BOOLEAN",
        ...         }
        ...     }
        ... )
        >>> assert result["status"] == "ok"
        >>> print(result["data"]["new_version"])
    """
    logger.info(
        "firebase_remote_config_set: entry | project_id=%s param_count=%d",
        project_id or "(from env)",
        len(parameters),
    )
    try:
        if not isinstance(parameters, dict):
            raise ValueError("parameters must be a dict.")

        resolved_project_id = project_id or os.environ.get("GOOGLE_PROJECT_ID", "")
        if not resolved_project_id:
            raise ValueError(
                "project_id must be provided or GOOGLE_PROJECT_ID must be set."
            )

        token = _get_access_token([_SCOPE])
        config_url = f"{_FRC_BASE}/projects/{resolved_project_id}/remoteConfig"

        # Step 1: GET current template and ETag
        logger.info(
            "firebase_remote_config_set: fetching current config | project=%s",
            resolved_project_id,
        )
        get_headers = {
            "Authorization": f"Bearer {token}",
            "Accept-Encoding": "gzip",
        }
        with httpx.Client(timeout=30) as client:
            get_resp = client.get(config_url, headers=get_headers)
            if get_resp.is_error:
                raise RuntimeError(
                    f"GET Remote Config failed with HTTP {get_resp.status_code}: {get_resp.text}"
                )
            etag: str = get_resp.headers.get("etag", "*")
            current_config: dict = get_resp.json()

        logger.info(
            "firebase_remote_config_set: current version=%s etag=%s",
            current_config.get("version", {}).get("versionNumber", ""),
            etag,
        )

        # Step 2: Merge parameters (shallow merge at top level — new values win)
        merged_parameters: dict = {**current_config.get("parameters", {}), **parameters}

        # Step 3: Resolve conditions
        merged_conditions: list[dict] = (
            conditions if conditions is not None else current_config.get("conditions", [])
        )

        # Step 4: Assemble the new template payload
        new_template: dict = {
            "parameters": merged_parameters,
            "conditions": merged_conditions,
            "parameterGroups": current_config.get("parameterGroups", {}),
        }

        # Step 5: PUT with If-Match
        put_headers = {
            "Authorization": f"Bearer {token}",
            "Content-Type": "application/json; UTF-8",
            "If-Match": etag,
        }
        logger.info(
            "firebase_remote_config_set: publishing template | param_count=%d condition_count=%d",
            len(merged_parameters),
            len(merged_conditions),
        )
        with httpx.Client(timeout=30) as client:
            put_resp = client.put(config_url, headers=put_headers, json=new_template)
            if put_resp.status_code == 412:
                raise RuntimeError(
                    "ETag conflict (HTTP 412): the Remote Config template was modified "
                    "concurrently. Please retry with a fresh GET."
                )
            if put_resp.is_error:
                raise RuntimeError(
                    f"PUT Remote Config failed with HTTP {put_resp.status_code}: {put_resp.text}"
                )
            updated_config: dict = put_resp.json()

        new_version_info: dict = updated_config.get("version", {})
        new_version: str = new_version_info.get("versionNumber", "")
        update_time: str = new_version_info.get("updateTime", _now())
        update_origin: str = new_version_info.get("updateOrigin", "REST_API")

        result = {
            "status": "ok",
            "data": {
                "new_version": new_version,
                "update_time": update_time,
                "update_origin": update_origin,
                "parameters_set": len(merged_parameters),
            },
            "timestamp": _now(),
        }
        logger.info(
            "firebase_remote_config_set: exit | new_version=%s update_time=%s params=%d",
            new_version,
            update_time,
            len(merged_parameters),
        )
        return result

    except (ValueError, RuntimeError) as exc:
        logger.error("firebase_remote_config_set: error | %s", exc)
        return {"status": "error", "data": {"error": str(exc)}, "timestamp": _now()}
    except Exception as exc:
        logger.exception("firebase_remote_config_set: unexpected error | %s", exc)
        return {"status": "error", "data": {"error": str(exc)}, "timestamp": _now()}
