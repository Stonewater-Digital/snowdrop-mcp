"""
Create and manage Google Cloud Scheduler jobs.
Lets Snowdrop schedule autonomous recurring tasks — hourly feed checks,
daily posting routines, weekly ecosystem scans — without Thunder's involvement.
"""
import os
import json
import base64
import requests
from datetime import datetime, timezone

TOOL_META = {
    "name": "gcp_cloud_scheduler",
    "description": (
        "Create, list, or delete Google Cloud Scheduler cron jobs. "
        "Use this to schedule Snowdrop's autonomous recurring tasks: "
        "hourly Moltbook feed checks, daily GitHub activity scans, "
        "weekly ecosystem radar sweeps, or timed content posting. "
        "Jobs can trigger HTTP endpoints (like the MCP server) or Pub/Sub topics."
    ),
}

SCHEDULER_BASE = "https://cloudscheduler.googleapis.com/v1"


def _get_token(sa_json: dict) -> str:
    import time
    from cryptography.hazmat.primitives import hashes, serialization
    from cryptography.hazmat.primitives.asymmetric import padding

    now = int(time.time())
    hdr = base64.urlsafe_b64encode(json.dumps({"alg": "RS256", "typ": "JWT"}).encode()).rstrip(b"=").decode()
    pld = base64.urlsafe_b64encode(json.dumps({
        "iss": sa_json["client_email"],
        "scope": "https://www.googleapis.com/auth/cloud-platform",
        "aud": "https://oauth2.googleapis.com/token",
        "iat": now, "exp": now + 3600,
    }).encode()).rstrip(b"=").decode()
    key = serialization.load_pem_private_key(sa_json["private_key"].encode(), password=None)
    sig = key.sign(f"{hdr}.{pld}".encode(), padding.PKCS1v15(), hashes.SHA256())
    jwt = f"{hdr}.{pld}.{base64.urlsafe_b64encode(sig).rstrip(b'=').decode()}"
    resp = requests.post("https://oauth2.googleapis.com/token",
                         data={"grant_type": "urn:ietf:params:oauth:grant-type:jwt-bearer", "assertion": jwt},
                         timeout=15)
    resp.raise_for_status()
    return resp.json()["access_token"]


def gcp_cloud_scheduler(
    action: str,
    job_name: str = "",
    schedule: str = "",
    timezone_str: str = "America/Chicago",
    http_url: str = "",
    http_body: dict = None,
    http_method: str = "POST",
    description: str = "",
    project_id: str = "",
    region: str = "us-central1",
) -> dict:
    """
    Manage Cloud Scheduler jobs.

    Args:
        action: "create" | "list" | "delete" | "run_now"
        job_name: Short name for the job (e.g., "moltbook-feed-check")
        schedule: Cron expression (e.g., "0 * * * *" = hourly, "0 9 * * *" = 9am daily)
        timezone_str: Timezone for the schedule (default "America/Chicago" = Thunder's timezone)
        http_url: Target URL for HTTP jobs (e.g., MCP server endpoint)
        http_body: JSON body to POST to the URL
        http_method: HTTP method (default "POST")
        description: Human-readable description of what this job does
        project_id: GCP project ID (defaults to GOOGLE_PROJECT_ID)
        region: GCP region (default "us-central1")
    """
    sa_json_str = os.environ.get("GOOGLE_SERVICE_ACCOUNT_JSON", "")
    if not sa_json_str:
        sa_file = os.environ.get("GCP_SERVICE_ACCOUNT_FILE", "")
        if sa_file and os.path.exists(sa_file):
            with open(sa_file) as f:
                sa_json_str = f.read()

    if not sa_json_str:
        return {"status": "error", "data": {"message": "No GCP credentials"}, "timestamp": datetime.now(timezone.utc).isoformat()}

    project = project_id or os.environ.get("GOOGLE_PROJECT_ID", "")
    if not project:
        return {"status": "error", "data": {"message": "GOOGLE_PROJECT_ID not set"}, "timestamp": datetime.now(timezone.utc).isoformat()}

    try:
        token = _get_token(json.loads(sa_json_str))
    except Exception as e:
        return {"status": "error", "data": {"message": f"Auth failed: {e}"}, "timestamp": datetime.now(timezone.utc).isoformat()}

    headers = {"Authorization": f"Bearer {token}", "Content-Type": "application/json"}
    parent = f"projects/{project}/locations/{region}"
    base_url = f"{SCHEDULER_BASE}/{parent}/jobs"

    try:
        if action == "list":
            resp = requests.get(base_url, headers=headers, timeout=15)
            resp.raise_for_status()
            jobs = resp.json().get("jobs", [])
            return {
                "status": "ok",
                "data": {
                    "count": len(jobs),
                    "jobs": [{"name": j.get("name", "").split("/")[-1],
                               "schedule": j.get("schedule"),
                               "state": j.get("state"),
                               "lastAttemptTime": j.get("lastAttemptTime"),
                               "description": j.get("description", "")} for j in jobs],
                },
                "timestamp": datetime.now(timezone.utc).isoformat(),
            }

        if action == "delete":
            full_name = f"{parent}/jobs/{job_name}"
            resp = requests.delete(f"{SCHEDULER_BASE}/{full_name}", headers=headers, timeout=15)
            return {
                "status": "ok" if resp.status_code in (200, 204) else "error",
                "data": {"deleted": job_name},
                "timestamp": datetime.now(timezone.utc).isoformat(),
            }

        if action == "run_now":
            full_name = f"{parent}/jobs/{job_name}"
            resp = requests.post(f"{SCHEDULER_BASE}/{full_name}:run", headers=headers, timeout=15)
            return {
                "status": "ok" if resp.ok else "error",
                "data": resp.json(),
                "timestamp": datetime.now(timezone.utc).isoformat(),
            }

        if action == "create":
            if not job_name or not schedule or not http_url:
                return {"status": "error", "data": {"message": "create requires: job_name, schedule, http_url"},
                        "timestamp": datetime.now(timezone.utc).isoformat()}

            body_b64 = base64.b64encode(json.dumps(http_body or {}).encode()).decode() if http_body else ""
            job_body = {
                "name": f"{parent}/jobs/{job_name}",
                "description": description or f"Snowdrop scheduled task: {job_name}",
                "schedule": schedule,
                "timeZone": timezone_str,
                "httpTarget": {
                    "uri": http_url,
                    "httpMethod": http_method,
                    **({"body": body_b64, "headers": {"Content-Type": "application/json"}} if body_b64 else {}),
                },
            }
            resp = requests.post(base_url, headers=headers, json=job_body, timeout=15)
            resp.raise_for_status()
            return {
                "status": "ok",
                "data": {"created": job_name, "schedule": schedule, "url": http_url},
                "timestamp": datetime.now(timezone.utc).isoformat(),
            }

        return {"status": "error", "data": {"message": f"Unknown action: {action}"},
                "timestamp": datetime.now(timezone.utc).isoformat()}

    except Exception as e:
        return {"status": "error", "data": {"message": str(e)},
                "timestamp": datetime.now(timezone.utc).isoformat()}
