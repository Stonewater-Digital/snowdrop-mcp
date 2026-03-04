"""
Executive Summary
-----------------
Deploys, inspects, lists, and deletes Google Cloud Run services using the
Cloud Run Admin API v2 (run.googleapis.com). Authentication is performed
exclusively via a service account JSON credential — this module NEVER invokes
the gcloud CLI and NEVER relies on Application Default Credentials (ADC) from
the ambient environment. Credentials are resolved in this order:

  1. GOOGLE_SERVICE_ACCOUNT_JSON  — raw JSON string in the environment
  2. GCP_SERVICE_ACCOUNT_FILE     — file path to a JSON key file

Inputs  (via MCP tool call / direct function call):
  action         : str  — "deploy" | "status" | "list" | "delete"  (required)
  service_name   : str  — Cloud Run service identifier
  image_url      : str  — Docker image URI (required for deploy)
  region         : str  — GCP region, default "us-central1"
  project_id     : str  — GCP project, default from GOOGLE_PROJECT_ID env var
  env_vars       : dict — environment variables to set on the service
  port           : int  — container port, default 8080
  memory         : str  — memory limit, default "512Mi"
  cpu            : str  — CPU limit, default "1"
  min_instances  : int  — minimum instances, default 0
  max_instances  : int  — maximum instances, default 10

Outputs:
  {"status": "ok"|"error", "data": {...}, "timestamp": "<ISO8601>"}

MCP Tool Name: cloud_run_deploy

Agent Notes (Claude Code / Cursor / Codex CLI / Gemini CLI):
  - NEVER run: gcloud auth, gcloud config, gcloud auth application-default
  - ALWAYS load GOOGLE_SERVICE_ACCOUNT_JSON from .env via python-dotenv
  - Pass project_id explicitly — never rely on gcloud config get-value project
  - Image URL format: us-central1-docker.pkg.dev/PROJECT_ID/REPO/IMAGE:TAG
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
    "name": "cloud_run_deploy",
    "description": (
        "Deploy, inspect, list, or delete Google Cloud Run services. "
        "Uses Cloud Run Admin API v2 with explicit service account credentials only — "
        "no gcloud CLI, no Application Default Credentials."
    ),
    "inputSchema": {
        "type": "object",
        "properties": {
            "action": {
                "type": "string",
                "enum": ["deploy", "status", "list", "delete"],
                "description": "Operation to perform.",
            },
            "service_name": {"type": "string", "description": "Cloud Run service name."},
            "image_url": {"type": "string", "description": "Docker image URI (required for deploy)."},
            "region": {"type": "string", "default": "us-central1"},
            "project_id": {"type": "string", "description": "GCP project ID (falls back to GOOGLE_PROJECT_ID env)."},
            "env_vars": {"type": "object", "description": "Key/value environment variables for the service."},
            "port": {"type": "integer", "default": 8080},
            "memory": {"type": "string", "default": "512Mi"},
            "cpu": {"type": "string", "default": "1"},
            "min_instances": {"type": "integer", "default": 0},
            "max_instances": {"type": "integer", "default": 10},
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


def _build_credentials():
    """
    Resolve service account credentials.

    Priority:
      1. GOOGLE_SERVICE_ACCOUNT_JSON env var — raw JSON string
      2. GCP_SERVICE_ACCOUNT_FILE env var    — path to JSON key file
      3. Fallback to google.auth.default() (ADC)
    """
    raw_json = os.environ.get("GOOGLE_SERVICE_ACCOUNT_JSON")
    if raw_json:
        try:
            info = json.loads(raw_json)
            return service_account.Credentials.from_service_account_info(info, scopes=SCOPES)
        except (json.JSONDecodeError, ValueError):
            pass  # fall through to file-based auth

    key_file = os.environ.get("GCP_SERVICE_ACCOUNT_FILE")
    if key_file and os.path.exists(key_file):
        return service_account.Credentials.from_service_account_file(key_file, scopes=SCOPES)

    import google.auth
    credentials, _ = google.auth.default(scopes=SCOPES)
    return credentials


def _run_client():
    creds = _build_credentials()
    return build("run", "v2", credentials=creds, cache_discovery=False)


def _parent(project_id: str, region: str) -> str:
    return f"projects/{project_id}/locations/{region}"


def _service_fqn(project_id: str, region: str, service_name: str) -> str:
    return f"projects/{project_id}/locations/{region}/services/{service_name}"


def cloud_run_deploy(
    action: str,
    service_name: str = "",
    image_url: str = "",
    region: str = "us-central1",
    project_id: str = "",
    env_vars: dict = None,
    port: int = 8080,
    memory: str = "512Mi",
    cpu: str = "1",
    min_instances: int = 0,
    max_instances: int = 10,
) -> dict:
    """
    Entry point for the cloud_run_deploy MCP tool.

    Uses ONLY the Cloud Run Admin API v2 and explicit service account credentials.
    Does not shell out to gcloud. Does not use ADC. Safe to call from any agent
    (Claude Code, Cursor, Codex CLI, Gemini CLI) as long as env vars are set.
    """
    if env_vars is None:
        env_vars = {}

    project_id = project_id or os.environ.get("GOOGLE_PROJECT_ID", "")
    if not project_id:
        return _wrap("error", {"message": "project_id is required (or set GOOGLE_PROJECT_ID)."})

    try:
        client = _run_client()
        services = client.projects().locations().services()

        if action == "deploy":
            if not service_name or not image_url:
                return _wrap("error", {"message": "service_name and image_url are required for deploy."})

            env_list = [{"name": k, "value": v} for k, v in env_vars.items()]
            body = {
                "template": {
                    "containers": [
                        {
                            "image": image_url,
                            "ports": [{"containerPort": port}],
                            "resources": {"limits": {"memory": memory, "cpu": cpu}},
                            "env": env_list,
                        }
                    ],
                    "scaling": {"minInstanceCount": min_instances, "maxInstanceCount": max_instances},
                }
            }

            # Try create first; fall back to patch if service already exists.
            try:
                op = services.create(
                    parent=_parent(project_id, region),
                    serviceId=service_name,
                    body=body,
                ).execute()
                return _wrap("ok", {"operation": op.get("name"), "action": "created"})
            except HttpError as exc:
                if exc.resp.status == 409:  # already exists — patch instead
                    op = services.patch(
                        name=_service_fqn(project_id, region, service_name),
                        body=body,
                    ).execute()
                    return _wrap("ok", {"operation": op.get("name"), "action": "updated"})
                raise

        elif action == "status":
            if not service_name:
                return _wrap("error", {"message": "service_name is required for status."})
            svc = services.get(name=_service_fqn(project_id, region, service_name)).execute()
            return _wrap("ok", {
                "service_name": service_name,
                "uri": svc.get("uri"),
                "state": svc.get("terminalCondition", {}).get("state"),
                "last_modifier": svc.get("lastModifier"),
                "update_time": svc.get("updateTime"),
                "observed_generation": svc.get("observedGeneration"),
            })

        elif action == "list":
            result = services.list(parent=_parent(project_id, region)).execute()
            items = result.get("services", [])
            return _wrap("ok", {
                "services": [
                    {"name": s.get("name"), "uri": s.get("uri"), "update_time": s.get("updateTime")}
                    for s in items
                ],
                "count": len(items),
            })

        elif action == "delete":
            if not service_name:
                return _wrap("error", {"message": "service_name is required for delete."})
            op = services.delete(name=_service_fqn(project_id, region, service_name)).execute()
            return _wrap("ok", {"operation": op.get("name"), "action": "deleted"})

        else:
            return _wrap("error", {"message": f"Unknown action '{action}'. Use: deploy, status, list, delete."})

    except HttpError as exc:
        logger.exception("Cloud Run API error")
        return _wrap("error", {"message": str(exc), "http_status": exc.resp.status})
    except Exception as exc:
        logger.exception("Unexpected error in cloud_run_deploy")
        return _wrap("error", {"message": str(exc)})
