"""
Executive Summary
-----------------
Manages Google Cloud Secret Manager — create, read, rotate, list, and delete
secrets — using the Secret Manager REST API v1 with explicit service account
credentials. This module NEVER uses gcloud CLI or Application Default Credentials.

Credentials resolved in order:
  1. GOOGLE_SERVICE_ACCOUNT_JSON  — raw JSON string (for Railway / Cloud Run / Fly.io)
  2. GCP_SERVICE_ACCOUNT_FILE     — file path to JSON key (for HP local)

Inputs:
  action       : str  — "get" | "set" | "list" | "delete" | "rotate"  (required)
  secret_id    : str  — secret identifier (required for get/set/delete/rotate)
  secret_value : str  — plaintext value to store (required for set/rotate)
  project_id   : str  — GCP project ID (falls back to GOOGLE_PROJECT_ID env)
  version      : str  — secret version, default "latest" (for get)

Outputs:
  {"status": "ok"|"error", "data": {...}, "timestamp": "<ISO8601>"}

MCP Tool Name: gcp_secret_manager

Agent Notes (Claude Code / Cursor / Codex CLI / Gemini CLI):
  - Required IAM role: roles/secretmanager.admin (or secretAccessor for read-only)
  - Secret values are base64-encoded in transit; this skill handles encode/decode
  - Use "rotate" instead of "set" on existing secrets to preserve version history
  - NEVER log or print the secret_value field
"""

import base64
import json
import logging
import os
from datetime import datetime, timezone

from google.oauth2 import service_account
from googleapiclient.discovery import build
from googleapiclient.errors import HttpError

logger = logging.getLogger(__name__)

SCOPES = ["https://www.googleapis.com/auth/cloud-platform"]

TOOL_META = {
    "name": "gcp_secret_manager",
    "description": (
        "Create, read, rotate, list, or delete secrets in Google Cloud Secret Manager. "
        "Uses Secret Manager API v1 with explicit service account credentials — "
        "no gcloud CLI, no ADC. Requires roles/secretmanager.admin on the service account."
    ),
    "inputSchema": {
        "type": "object",
        "properties": {
            "action": {
                "type": "string",
                "enum": ["get", "set", "list", "delete", "rotate"],
                "description": "Operation to perform.",
            },
            "secret_id": {
                "type": "string",
                "description": "Secret identifier (required for get/set/delete/rotate).",
            },
            "secret_value": {
                "type": "string",
                "description": "Plaintext secret value (required for set/rotate). Never logged.",
            },
            "project_id": {
                "type": "string",
                "description": "GCP project ID (falls back to GOOGLE_PROJECT_ID env).",
            },
            "version": {
                "type": "string",
                "default": "latest",
                "description": "Secret version to retrieve (for get). Use 'latest' for current.",
            },
        },
        "required": ["action"],
    },
    "outputSchema": {
        "type": "object",
        "properties": {
            "status": {"type": "string", "enum": ["ok", "error"]},
            "data": {"type": "object"},
            "timestamp": {"type": "string"},
        },
        "required": ["status", "data", "timestamp"],
    },
}


def _now_iso() -> str:
    return datetime.now(timezone.utc).isoformat()


def _wrap(status: str, data: dict) -> dict:
    return {"status": status, "data": data, "timestamp": _now_iso()}


def _build_credentials() -> service_account.Credentials:
    raw_json = os.environ.get("GOOGLE_SERVICE_ACCOUNT_JSON")
    if raw_json:
        try:
            info = json.loads(raw_json)
            return service_account.Credentials.from_service_account_info(info, scopes=SCOPES)
        except (json.JSONDecodeError, ValueError):
            pass  # fall through to file-based auth
    key_file = os.environ.get("GCP_SERVICE_ACCOUNT_FILE")
    if key_file:
        return service_account.Credentials.from_service_account_file(key_file, scopes=SCOPES)
    raise RuntimeError(
        "No GCP credentials. Set GOOGLE_SERVICE_ACCOUNT_JSON or GCP_SERVICE_ACCOUNT_FILE."
    )


def _sm_client():
    creds = _build_credentials()
    return build("secretmanager", "v1", credentials=creds, cache_discovery=False)


def _project_path(project_id: str) -> str:
    return f"projects/{project_id}"


def _secret_path(project_id: str, secret_id: str) -> str:
    return f"projects/{project_id}/secrets/{secret_id}"


def _version_path(project_id: str, secret_id: str, version: str) -> str:
    return f"projects/{project_id}/secrets/{secret_id}/versions/{version}"


def gcp_secret_manager(
    action: str,
    secret_id: str = "",
    secret_value: str = "",
    project_id: str = "",
    version: str = "latest",
) -> dict:
    """
    Entry point for the gcp_secret_manager MCP tool.

    Uses Secret Manager API v1 with explicit service account credentials only.
    Safe to call from Claude Code, Cursor, Codex CLI, or Gemini CLI agents.
    """
    project_id = project_id or os.environ.get("GOOGLE_PROJECT_ID", "")
    if not project_id:
        return _wrap("error", {"message": "project_id is required (or set GOOGLE_PROJECT_ID)."})

    try:
        client = _sm_client()
        secrets = client.projects().secrets()
        versions = client.projects().secrets().versions()

        if action == "get":
            if not secret_id:
                return _wrap("error", {"message": "secret_id is required for get."})
            name = _version_path(project_id, secret_id, version)
            resp = versions.access(name=name).execute()
            payload = resp.get("payload", {}).get("data", "")
            decoded = base64.b64decode(payload).decode("utf-8") if payload else ""
            return _wrap("ok", {
                "secret_id": secret_id,
                "version": version,
                "value": decoded,
                "create_time": resp.get("createTime"),
            })

        elif action == "set":
            if not secret_id or not secret_value:
                return _wrap("error", {"message": "secret_id and secret_value are required for set."})
            # Create the secret if it doesn't exist.
            try:
                secrets.create(
                    parent=_project_path(project_id),
                    secretId=secret_id,
                    body={"replication": {"automatic": {}}},
                ).execute()
            except HttpError as exc:
                if exc.resp.status != 409:  # 409 = already exists, that's fine
                    raise
            # Add a new version.
            encoded = base64.b64encode(secret_value.encode("utf-8")).decode("utf-8")
            ver = secrets.addVersion(
                parent=_secret_path(project_id, secret_id),
                body={"payload": {"data": encoded}},
            ).execute()
            return _wrap("ok", {
                "secret_id": secret_id,
                "version_name": ver.get("name"),
                "action": "created_version",
            })

        elif action == "list":
            result = secrets.list(parent=_project_path(project_id)).execute()
            items = result.get("secrets", [])
            return _wrap("ok", {
                "secrets": [s.get("name", "").split("/")[-1] for s in items],
                "count": len(items),
            })

        elif action == "delete":
            if not secret_id:
                return _wrap("error", {"message": "secret_id is required for delete."})
            secrets.delete(name=_secret_path(project_id, secret_id)).execute()
            return _wrap("ok", {"secret_id": secret_id, "action": "deleted"})

        elif action == "rotate":
            if not secret_id or not secret_value:
                return _wrap("error", {"message": "secret_id and secret_value are required for rotate."})
            # Add new version.
            encoded = base64.b64encode(secret_value.encode("utf-8")).decode("utf-8")
            new_ver = secrets.addVersion(
                parent=_secret_path(project_id, secret_id),
                body={"payload": {"data": encoded}},
            ).execute()
            # Disable the previous "latest" (now second-latest).
            all_vers = versions.list(
                parent=_secret_path(project_id, secret_id),
                filter="state:ENABLED",
            ).execute()
            enabled = sorted(
                all_vers.get("versions", []),
                key=lambda v: v.get("createTime", ""),
            )
            if len(enabled) > 1:
                old_name = enabled[-2].get("name")
                versions.disable(name=old_name, body={}).execute()
                logger.info("Disabled old version: %s", old_name)
            return _wrap("ok", {
                "secret_id": secret_id,
                "new_version": new_ver.get("name"),
                "action": "rotated",
            })

        else:
            return _wrap("error", {"message": f"Unknown action '{action}'. Use: get, set, list, delete, rotate."})

    except HttpError as exc:
        logger.exception("Secret Manager API error")
        return _wrap("error", {"message": str(exc), "http_status": exc.resp.status})
    except Exception as exc:
        logger.exception("Unexpected error in gcp_secret_manager")
        return _wrap("error", {"message": str(exc)})
