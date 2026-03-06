"""
Executive Summary
-----------------
CI/CD Monitor skill for Snowdrop. Queries GitHub Actions APIs to retrieve
workflow run summaries, returning strict JSON data to avoid massive log dumps
in context.

Actions:
  latest_runs - get recent workflow runs
  run_details - get details of a specific run and its failed jobs/steps

Env vars required:
  GITHUB_TOKEN - Personal Access Token with repo scope

MCP Tool Name: ci_cd_monitor
"""

import os
import requests
from datetime import datetime, timezone

TOOL_META = {
    "name": "ci_cd_monitor",
    "description": (
        "Monitor GitHub Actions CI/CD workflows. Returns strict JSON summaries "
        "of workflow statuses and failures, avoiding massive raw log dumps."
    ),
    "inputSchema": {
        "type": "object",
        "properties": {
            "owner_repo": {
                "type": "string",
                "description": "The repository owner/name (e.g., 'Stonewater-Digital/snowdrop-core').",
            },
            "action": {
                "type": "string",
                "enum": ["latest_runs", "run_details"],
                "description": "Operation to perform: 'latest_runs' or 'run_details'.",
            },
            "run_id": {
                "type": "integer",
                "description": "Workflow run ID. Required if action is 'run_details'.",
            },
            "limit": {
                "type": "integer",
                "description": "Number of runs to return for 'latest_runs'. Default 5.",
            }
        },
        "required": ["owner_repo", "action"],
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

_GITHUB_API = "https://api.github.com"

def _now_iso() -> str:
    return datetime.now(timezone.utc).isoformat()

def _wrap(status: str, data: dict) -> dict:
    return {"status": status, "data": data, "timestamp": _now_iso()}

def _get_headers(token: str) -> dict:
    return {
        "Authorization": f"Bearer {token}",
        "Accept": "application/vnd.github.v3+json",
        "X-GitHub-Api-Version": "2022-11-28"
    }

def ci_cd_monitor(
    owner_repo: str,
    action: str,
    run_id: int = 0,
    limit: int = 5
) -> dict:
    """Monitor GitHub Actions workflows."""
    token = os.environ.get("GITHUB_TOKEN", "")
    if not token:
        return _wrap("error", {"message": "GITHUB_TOKEN not set. Add to .env."})
        
    if action not in ["latest_runs", "run_details"]:
        return _wrap("error", {"message": f"Invalid action: {action}"})
        
    headers = _get_headers(token)
    
    try:
        if action == "latest_runs":
            url = f"{_GITHUB_API}/repos/{owner_repo}/actions/runs"
            resp = requests.get(url, headers=headers, params={"per_page": limit})
            resp.raise_for_status()
            data = resp.json()
            
            runs_summary = []
            for run in data.get("workflow_runs", []):
                runs_summary.append({
                    "id": run["id"],
                    "name": run["name"],
                    "status": run["status"],
                    "conclusion": run["conclusion"],
                    "head_branch": run["head_branch"],
                    "created_at": run["created_at"]
                })
                
            return _wrap("ok", {"runs": runs_summary, "total_count": data.get("total_count", 0)})
            
        elif action == "run_details":
            if not run_id:
                return _wrap("error", {"message": "'run_id' is required for action='run_details'."})
                
            # Get run details
            run_url = f"{_GITHUB_API}/repos/{owner_repo}/actions/runs/{run_id}"
            run_resp = requests.get(run_url, headers=headers)
            run_resp.raise_for_status()
            run_data = run_resp.json()
            
            summary = {
                "id": run_data["id"],
                "name": run_data["name"],
                "status": run_data["status"],
                "conclusion": run_data["conclusion"],
                "failed_jobs": []
            }
            
            # If failed, find the failed jobs/steps
            if run_data["conclusion"] == "failure":
                jobs_url = f"{_GITHUB_API}/repos/{owner_repo}/actions/runs/{run_id}/jobs"
                jobs_resp = requests.get(jobs_url, headers=headers)
                
                if jobs_resp.status_code == 200:
                    jobs_data = jobs_resp.json()
                    for job in jobs_data.get("jobs", []):
                        if job["conclusion"] == "failure":
                            failed_job = {
                                "name": job["name"],
                                "failed_steps": []
                            }
                            for step in job.get("steps", []):
                                if step["conclusion"] == "failure":
                                    failed_job["failed_steps"].append({
                                        "name": step["name"],
                                        "number": step["number"]
                                    })
                            summary["failed_jobs"].append(failed_job)
                            
            return _wrap("ok", {"run_details": summary})
            
    except requests.exceptions.HTTPError as exc:
        msg = f"HTTP error {exc.response.status_code}: {exc.response.text}"
        return _wrap("error", {"message": msg})
    except Exception as exc:
        return _wrap("error", {"message": str(exc)})
