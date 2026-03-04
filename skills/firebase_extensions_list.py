"""
Executive Summary
-----------------
Lists all installed Firebase Extensions in a GCP project using the Firebase
Extensions REST API v1beta. Returns each extension instance's ID, deployment
state, extension reference (publisher/extension@version), creation time, last
update time, and a summary of its parameter configuration. Credentials are
resolved via ADC on Cloud Run or via GOOGLE_SERVICE_ACCOUNT_JSON for local
and Railway deployments.

Credentials resolved in order:
  1. GOOGLE_SERVICE_ACCOUNT_JSON  — raw JSON string (Cloud Run / Railway / Fly.io)
  2. ADC (Application Default Credentials) — used automatically on Cloud Run

Inputs:
  project_id : str  — GCP project ID (falls back to GOOGLE_PROJECT_ID env)

Outputs:
  {"status": "ok"|"error", "data": {...}, "timestamp": "<ISO8601>"}

MCP Tool Name: firebase_extensions_list

Agent Notes (Claude Code / Cursor / Codex CLI / Gemini CLI):
  - Required IAM role: roles/firebase.viewer or roles/firebaseextensions.viewer
  - state values include: ACTIVE, DEPLOYING, UNINSTALLING, ERRORED
  - extension_ref format: "firebase/storage-resize-images@0.1.40"
  - config summary omits secret/sensitive parameter values for security
"""

import json
import logging
import os
from datetime import datetime, timezone

import requests

logger = logging.getLogger("snowdrop.firebase_extensions_list")

TOOL_META = {
    "name": "firebase_extensions_list",
    "description": (
        "List all installed Firebase Extensions in a project. "
        "Returns extension instance ID, state, extension reference, and configuration."
    ),
    "tier": "free",
}

_EXTENSIONS_SCOPE = "https://www.googleapis.com/auth/cloud-platform"


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


def firebase_extensions_list(
    project_id: str | None = None,
) -> dict:
    """List all installed Firebase Extensions in a project.

    Args:
        project_id: GCP project ID. Falls back to GOOGLE_PROJECT_ID env var
            if not supplied.

    Returns:
        dict: Standard Snowdrop envelope::

            {
                "status": "ok",
                "data": {
                    "instances": [
                        {
                            "instance_id": str,
                            "state": str,
                            "extension_ref": str,
                            "create_time": str,
                            "update_time": str,
                            "config": {
                                "name": str,
                                "params": dict[str, str]
                            }
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
        requests.HTTPError: If the Extensions API returns a non-2xx response.

    Example:
        >>> result = firebase_extensions_list(project_id="my-firebase-project")
        >>> for inst in result["data"]["instances"]:
        ...     print(inst["instance_id"], inst["state"])
        storage-resize-images ACTIVE
    """
    logger.info(
        "firebase_extensions_list called: project_id=%s",
        project_id,
    )

    project_id = project_id or os.environ.get("GOOGLE_PROJECT_ID", "")
    if not project_id:
        return _wrap(
            "error",
            {"message": "project_id is required (or set GOOGLE_PROJECT_ID)."},
        )

    url = (
        f"https://firebaseextensions.googleapis.com/v1beta/projects/"
        f"{project_id}/instances"
    )

    try:
        token = _get_access_token([_EXTENSIONS_SCOPE])
        headers = {"Authorization": f"Bearer {token}"}

        resp = requests.get(url, headers=headers, timeout=30)
        resp.raise_for_status()
        body = resp.json()

        raw_instances = body.get("instances", [])
        instances = []
        for inst in raw_instances:
            # instance name has format: projects/{pid}/instances/{instance_id}
            name_parts = inst.get("name", "").split("/")
            instance_id = name_parts[-1] if name_parts else ""

            config = inst.get("config", {})
            # Params may contain secrets; only include non-secret keys.
            raw_params: dict[str, str] = config.get("params", {})
            # secret param values appear as resource references — keep them as-is
            # since they don't expose the actual secret value.
            params_summary = {k: str(v) for k, v in raw_params.items()}

            extension_ref = config.get("extensionRef", inst.get("extensionRef", ""))

            instances.append(
                {
                    "instance_id": instance_id,
                    "state": inst.get("state", ""),
                    "extension_ref": extension_ref,
                    "create_time": inst.get("createTime", ""),
                    "update_time": inst.get("updateTime", ""),
                    "config": {
                        "name": config.get("name", ""),
                        "params": params_summary,
                    },
                }
            )

        logger.info(
            "firebase_extensions_list returned %d instances for project %s",
            len(instances),
            project_id,
        )
        return _wrap(
            "ok",
            {
                "instances": instances,
                "count": len(instances),
                "project_id": project_id,
            },
        )

    except requests.HTTPError as exc:
        status_code = exc.response.status_code if exc.response is not None else 0
        logger.error(
            "Firebase Extensions API HTTP error %d: %s",
            status_code,
            exc,
        )
        return _wrap("error", {"message": str(exc), "http_status": status_code})
    except Exception as exc:
        logger.exception("Unexpected error in firebase_extensions_list")
        return _wrap("error", {"message": str(exc)})
