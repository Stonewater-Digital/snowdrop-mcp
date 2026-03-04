"""
Executive Summary
-----------------
Manages Google Artifact Registry Docker repositories — lists images and tags,
deletes old tag versions to control storage costs, and cleans untagged layers.
Uses Artifact Registry API v1 with explicit service account credentials only.
Pair with docker_cleanup for complete image lifecycle management.

Credentials resolved in order:
  1. GOOGLE_SERVICE_ACCOUNT_JSON  — JSON string (cloud/Railway/Fly.io)
  2. GCP_SERVICE_ACCOUNT_FILE     — file path (HP local)

Inputs:
  action       : str  — "list_images" | "list_tags" | "delete_old_tags"
                        | "get_digest" | "clean_untagged"  (required)
  repository   : str  — Artifact Registry repo name (e.g. "snowdrop-images")
  location     : str  — GCP region (default "us-central1")
  project_id   : str  — GCP project (falls back to GOOGLE_PROJECT_ID env)
  keep_latest  : int  — number of newest tagged versions to keep (default 5)
  package_name : str  — specific image name within the repo (for list_tags/get_digest)

Outputs:
  {"status": "ok"|"error", "data": {...}, "timestamp": "<ISO8601>"}

MCP Tool Name: artifact_registry_manager

Agent Notes (Claude Code / Cursor / Codex CLI / Gemini CLI):
  - Required IAM role: roles/artifactregistry.admin
  - Run delete_old_tags with keep_latest=5 after each deployment to control costs
  - Run clean_untagged weekly alongside docker_cleanup
  - Default repo for Snowdrop: "snowdrop-images" in us-central1
"""

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
    "name": "artifact_registry_manager",
    "description": (
        "Manage Google Artifact Registry Docker images: list, clean old tags, "
        "remove untagged layers. Use after each deployment to keep storage costs low. "
        "Requires roles/artifactregistry.admin on the service account."
    ),
    "inputSchema": {
        "type": "object",
        "properties": {
            "action": {
                "type": "string",
                "enum": ["list_images", "list_tags", "delete_old_tags", "get_digest", "clean_untagged"],
                "description": "Operation to perform.",
            },
            "repository": {
                "type": "string",
                "description": "Artifact Registry repository name (e.g. 'snowdrop-images').",
            },
            "location": {"type": "string", "default": "us-central1"},
            "project_id": {"type": "string", "description": "GCP project ID."},
            "keep_latest": {
                "type": "integer",
                "default": 5,
                "description": "Number of most-recent tagged versions to keep (for delete_old_tags).",
            },
            "package_name": {
                "type": "string",
                "description": "Specific image name for list_tags/get_digest.",
            },
        },
        "required": ["action"],
    },
    "outputSchema": {
        "type": "object",
        "properties": {
            "status": {"type": "string"},
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
    raise RuntimeError("Set GOOGLE_SERVICE_ACCOUNT_JSON or GCP_SERVICE_ACCOUNT_FILE.")


def _ar_client():
    return build("artifactregistry", "v1", credentials=_build_credentials(), cache_discovery=False)


def _repo_path(project_id: str, location: str, repository: str) -> str:
    return f"projects/{project_id}/locations/{location}/repositories/{repository}"


def artifact_registry_manager(
    action: str,
    repository: str = "snowdrop-images",
    location: str = "us-central1",
    project_id: str = "",
    keep_latest: int = 5,
    package_name: str = "",
) -> dict:
    """Manage Artifact Registry images. Explicit SA credentials only — no gcloud."""
    project_id = project_id or os.environ.get("GOOGLE_PROJECT_ID", "")
    if not project_id:
        return _wrap("error", {"message": "project_id required (or set GOOGLE_PROJECT_ID)."})

    try:
        client = _ar_client()
        repo_path = _repo_path(project_id, location, repository)

        if action == "list_images":
            result = client.projects().locations().repositories().packages().list(
                parent=repo_path
            ).execute()
            pkgs = result.get("packages", [])
            return _wrap("ok", {
                "images": [{"name": p.get("name", "").split("/")[-1], "full": p.get("name")} for p in pkgs],
                "count": len(pkgs),
                "repository": repository,
            })

        elif action == "list_tags":
            if not package_name:
                return _wrap("error", {"message": "package_name required for list_tags."})
            pkg_path = f"{repo_path}/packages/{package_name}"
            result = client.projects().locations().repositories().packages().tags().list(
                parent=pkg_path
            ).execute()
            tags = result.get("tags", [])
            return _wrap("ok", {
                "tags": [{"name": t.get("name", "").split("/")[-1], "version": t.get("version")} for t in tags],
                "count": len(tags),
            })

        elif action == "delete_old_tags":
            if not package_name:
                return _wrap("error", {"message": "package_name required for delete_old_tags."})
            pkg_path = f"{repo_path}/packages/{package_name}"
            # List all versions sorted by creation time.
            ver_result = client.projects().locations().repositories().packages().versions().list(
                parent=pkg_path, orderBy="createTime desc"
            ).execute()
            all_versions = ver_result.get("versions", [])
            to_keep = all_versions[:keep_latest]
            to_delete = all_versions[keep_latest:]
            deleted = []
            for v in to_delete:
                ver_name = v.get("name")
                client.projects().locations().repositories().packages().versions().delete(
                    name=ver_name
                ).execute()
                deleted.append(ver_name.split("/")[-1])
            return _wrap("ok", {
                "kept": len(to_keep),
                "deleted": len(deleted),
                "deleted_versions": deleted,
                "package_name": package_name,
            })

        elif action == "get_digest":
            if not package_name:
                return _wrap("error", {"message": "package_name required for get_digest."})
            pkg_path = f"{repo_path}/packages/{package_name}"
            result = client.projects().locations().repositories().packages().versions().list(
                parent=pkg_path, orderBy="createTime desc"
            ).execute()
            versions = result.get("versions", [])
            latest = versions[0] if versions else {}
            return _wrap("ok", {
                "package_name": package_name,
                "latest_version": latest.get("name", "").split("/")[-1],
                "create_time": latest.get("createTime"),
                "metadata": latest.get("metadata", {}),
            })

        elif action == "clean_untagged":
            if not package_name:
                return _wrap("error", {"message": "package_name required for clean_untagged."})
            pkg_path = f"{repo_path}/packages/{package_name}"
            # Versions with no associated tags are "untagged" / dangling.
            ver_result = client.projects().locations().repositories().packages().versions().list(
                parent=pkg_path
            ).execute()
            all_versions = ver_result.get("versions", [])
            deleted = []
            for v in all_versions:
                if not v.get("relatedTags"):
                    ver_name = v.get("name")
                    client.projects().locations().repositories().packages().versions().delete(
                        name=ver_name
                    ).execute()
                    deleted.append(ver_name.split("/")[-1])
            return _wrap("ok", {
                "untagged_deleted": len(deleted),
                "deleted_versions": deleted,
                "package_name": package_name,
            })

        else:
            return _wrap("error", {"message": f"Unknown action '{action}'."})

    except HttpError as exc:
        logger.exception("Artifact Registry API error")
        return _wrap("error", {"message": str(exc), "http_status": exc.resp.status})
    except Exception as exc:
        logger.exception("artifact_registry_manager error")
        return _wrap("error", {"message": str(exc)})
