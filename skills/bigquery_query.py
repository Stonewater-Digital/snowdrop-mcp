"""
Executive Summary
-----------------
Runs BigQuery SQL queries and schema operations for financial analytics and
data exploration. Uses the BigQuery REST API v2 with explicit service account
credentials — no gcloud CLI, no ADC, no google-cloud-bigquery SDK.

Credentials resolved in order:
  1. GOOGLE_SERVICE_ACCOUNT_JSON  — JSON string (cloud environments)
  2. GCP_SERVICE_ACCOUNT_FILE     — file path (HP local)

Inputs:
  action      : str  — "query" | "list_datasets" | "list_tables" | "get_schema"
  sql         : str  — BigQuery SQL (required for query)
  project_id  : str  — GCP project (falls back to GOOGLE_PROJECT_ID env)
  dataset_id  : str  — dataset for list_tables
  table_id    : str  — table for get_schema
  max_results : int  — row limit for query (default 100)
  timeout_ms  : int  — query timeout in milliseconds (default 30000)

Outputs:
  {"status": "ok"|"error", "data": {"rows": [...], "row_count": int,
   "bytes_processed": int, "cache_hit": bool}, "timestamp": "<ISO8601>"}

MCP Tool Name: bigquery_query

Agent Notes (Claude Code / Cursor / Codex CLI / Gemini CLI):
  - Required IAM roles: roles/bigquery.jobUser + roles/bigquery.dataViewer
  - Required API: bigquery.googleapis.com
  - Queries are synchronous (polls until done up to timeout_ms)
  - Use max_results to protect against runaway scans; costs are per byte processed
  - For Ghost Ledger v2, data will live in dataset "snowdrop_ledger"
"""

import json
import logging
import os
import time
from datetime import datetime, timezone

from google.oauth2 import service_account
from googleapiclient.discovery import build
from googleapiclient.errors import HttpError

logger = logging.getLogger(__name__)

SCOPES = ["https://www.googleapis.com/auth/cloud-platform"]

TOOL_META = {
    "name": "bigquery_query",
    "description": (
        "Run BigQuery SQL queries and schema operations for financial analytics. "
        "Uses BigQuery REST API v2 with explicit SA credentials — no gcloud, no ADC. "
        "Requires roles/bigquery.jobUser and roles/bigquery.dataViewer."
    ),
    "inputSchema": {
        "type": "object",
        "properties": {
            "action": {
                "type": "string",
                "enum": ["query", "list_datasets", "list_tables", "get_schema"],
                "description": "Operation to perform.",
            },
            "sql": {"type": "string", "description": "BigQuery SQL statement (required for query)."},
            "project_id": {"type": "string", "description": "GCP project ID."},
            "dataset_id": {"type": "string", "description": "Dataset ID (required for list_tables)."},
            "table_id": {"type": "string", "description": "Table ID (required for get_schema)."},
            "max_results": {"type": "integer", "default": 100},
            "timeout_ms": {"type": "integer", "default": 30000},
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


def _bq_client():
    return build("bigquery", "v2", credentials=_build_credentials(), cache_discovery=False)


def _poll_job(client, project_id: str, job_id: str, timeout_ms: int) -> dict:
    """Poll a BigQuery job until complete or timeout."""
    deadline = time.time() + timeout_ms / 1000
    while time.time() < deadline:
        job = client.jobs().get(projectId=project_id, jobId=job_id).execute()
        state = job.get("status", {}).get("state")
        if state == "DONE":
            errors = job.get("status", {}).get("errors")
            if errors:
                raise RuntimeError(f"BigQuery job failed: {errors}")
            return job
        time.sleep(1)
    raise TimeoutError(f"BigQuery job {job_id} did not complete within {timeout_ms}ms.")


def bigquery_query(
    action: str,
    sql: str = "",
    project_id: str = "",
    dataset_id: str = "",
    table_id: str = "",
    max_results: int = 100,
    timeout_ms: int = 30000,
) -> dict:
    """Run BigQuery operations. Explicit SA credentials only — no gcloud, no ADC."""
    project_id = project_id or os.environ.get("GOOGLE_PROJECT_ID", "")
    if not project_id:
        return _wrap("error", {"message": "project_id required (or set GOOGLE_PROJECT_ID)."})

    try:
        client = _bq_client()

        if action == "query":
            if not sql:
                return _wrap("error", {"message": "sql is required for query."})
            job_body = {
                "configuration": {
                    "query": {
                        "query": sql,
                        "useLegacySql": False,
                        "maximumBytesBilled": 1_000_000_000,  # 1 GB safety cap
                    }
                }
            }
            job = client.jobs().insert(projectId=project_id, body=job_body).execute()
            job_id = job["jobReference"]["jobId"]
            completed = _poll_job(client, project_id, job_id, timeout_ms)

            stats = completed.get("statistics", {}).get("query", {})
            # Fetch results
            result = client.jobs().getQueryResults(
                projectId=project_id, jobId=job_id, maxResults=max_results
            ).execute()
            schema = result.get("schema", {}).get("fields", [])
            col_names = [f["name"] for f in schema]
            rows_raw = result.get("rows", [])
            rows = []
            for row in rows_raw:
                values = [v.get("v") for v in row.get("f", [])]
                rows.append(dict(zip(col_names, values)))

            return _wrap("ok", {
                "rows": rows,
                "row_count": len(rows),
                "total_rows": int(result.get("totalRows", 0)),
                "bytes_processed": int(stats.get("totalBytesProcessed", 0)),
                "cache_hit": stats.get("cacheHit", False),
                "job_id": job_id,
            })

        elif action == "list_datasets":
            result = client.datasets().list(projectId=project_id).execute()
            datasets = result.get("datasets", [])
            return _wrap("ok", {
                "datasets": [d["datasetReference"]["datasetId"] for d in datasets],
                "count": len(datasets),
            })

        elif action == "list_tables":
            if not dataset_id:
                return _wrap("error", {"message": "dataset_id required for list_tables."})
            result = client.tables().list(projectId=project_id, datasetId=dataset_id).execute()
            tables = result.get("tables", [])
            return _wrap("ok", {
                "tables": [t["tableReference"]["tableId"] for t in tables],
                "count": len(tables),
                "dataset_id": dataset_id,
            })

        elif action == "get_schema":
            if not dataset_id or not table_id:
                return _wrap("error", {"message": "dataset_id and table_id required for get_schema."})
            table = client.tables().get(
                projectId=project_id, datasetId=dataset_id, tableId=table_id
            ).execute()
            fields = table.get("schema", {}).get("fields", [])
            return _wrap("ok", {
                "table": f"{dataset_id}.{table_id}",
                "columns": [{"name": f["name"], "type": f["type"], "mode": f.get("mode", "NULLABLE")} for f in fields],
                "num_rows": table.get("numRows"),
                "num_bytes": table.get("numBytes"),
            })

        else:
            return _wrap("error", {"message": f"Unknown action '{action}'."})

    except HttpError as exc:
        logger.exception("BigQuery API error")
        return _wrap("error", {"message": str(exc), "http_status": exc.resp.status})
    except (TimeoutError, RuntimeError) as exc:
        return _wrap("error", {"message": str(exc)})
    except Exception as exc:
        logger.exception("bigquery_query error")
        return _wrap("error", {"message": str(exc)})
