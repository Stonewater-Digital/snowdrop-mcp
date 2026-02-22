"""
Write documents to Google Cloud Firestore.
Used as Snowdrop's persistent memory — agent CRM, conversation logs,
engagement history, content calendar, and relationship tracking.
"""
import os
import json
import requests
from datetime import datetime, timezone

TOOL_META = {
    "name": "gcp_firestore_write",
    "description": (
        "Write a document to Google Cloud Firestore. Snowdrop uses Firestore as her "
        "persistent memory and CRM — storing agent relationships, engagement history, "
        "content calendar entries, star trade records, and any data that should survive "
        "across sessions. Supports create, update (merge), and delete operations."
    ),
}

FIRESTORE_BASE = "https://firestore.googleapis.com/v1"


def _get_token(sa_json: dict) -> str:
    """Exchange service account credentials for a Bearer token."""
    import time
    import base64
    import hashlib
    import hmac

    # Build JWT
    now = int(time.time())
    header = base64.urlsafe_b64encode(json.dumps({"alg": "RS256", "typ": "JWT"}).encode()).rstrip(b"=").decode()
    payload = base64.urlsafe_b64encode(json.dumps({
        "iss": sa_json["client_email"],
        "scope": "https://www.googleapis.com/auth/datastore",
        "aud": "https://oauth2.googleapis.com/token",
        "iat": now,
        "exp": now + 3600,
    }).encode()).rstrip(b"=").decode()

    from cryptography.hazmat.primitives import hashes, serialization
    from cryptography.hazmat.primitives.asymmetric import padding
    private_key = serialization.load_pem_private_key(
        sa_json["private_key"].encode(), password=None
    )
    signing_input = f"{header}.{payload}".encode()
    signature = private_key.sign(signing_input, padding.PKCS1v15(), hashes.SHA256())
    sig_b64 = base64.urlsafe_b64encode(signature).rstrip(b"=").decode()
    jwt_token = f"{header}.{payload}.{sig_b64}"

    token_resp = requests.post(
        "https://oauth2.googleapis.com/token",
        data={
            "grant_type": "urn:ietf:params:oauth:grant-type:jwt-bearer",
            "assertion": jwt_token,
        },
        timeout=15,
    )
    token_resp.raise_for_status()
    return token_resp.json()["access_token"]


def _to_firestore_value(v):
    """Convert Python value to Firestore field value format."""
    if v is None:
        return {"nullValue": None}
    if isinstance(v, bool):
        return {"booleanValue": v}
    if isinstance(v, int):
        return {"integerValue": str(v)}
    if isinstance(v, float):
        return {"doubleValue": v}
    if isinstance(v, str):
        return {"stringValue": v}
    if isinstance(v, dict):
        return {"mapValue": {"fields": {k: _to_firestore_value(val) for k, val in v.items()}}}
    if isinstance(v, list):
        return {"arrayValue": {"values": [_to_firestore_value(item) for item in v]}}
    return {"stringValue": str(v)}


def gcp_firestore_write(
    collection: str,
    document_id: str,
    fields: dict,
    operation: str = "create",
    project_id: str = "",
) -> dict:
    """
    Write to Firestore. Creates or updates a document in the specified collection.

    Args:
        collection: Firestore collection name (e.g., "agent_memory", "star_trades", "content_calendar")
        document_id: Document ID (e.g., "github_user_someagent", "post_2026-02-22")
        fields: Dict of field name → value to write
        operation: "create" (overwrite), "update" (merge existing), or "delete"
        project_id: GCP project ID (defaults to GOOGLE_PROJECT_ID env var)
    """
    sa_json_str = os.environ.get("GOOGLE_SERVICE_ACCOUNT_JSON", "")
    if not sa_json_str:
        sa_file = os.environ.get("GCP_SERVICE_ACCOUNT_FILE", "")
        if sa_file and os.path.exists(sa_file):
            with open(sa_file) as f:
                sa_json_str = f.read()

    if not sa_json_str:
        return {
            "status": "error",
            "data": {"message": "No GCP credentials found (GOOGLE_SERVICE_ACCOUNT_JSON or GCP_SERVICE_ACCOUNT_FILE)"},
            "timestamp": datetime.now(timezone.utc).isoformat(),
        }

    project = project_id or os.environ.get("GOOGLE_PROJECT_ID", "")
    if not project:
        return {
            "status": "error",
            "data": {"message": "GOOGLE_PROJECT_ID not set"},
            "timestamp": datetime.now(timezone.utc).isoformat(),
        }

    try:
        sa_json = json.loads(sa_json_str)
        token = _get_token(sa_json)
    except Exception as e:
        return {
            "status": "error",
            "data": {"message": f"Auth failed: {e}"},
            "timestamp": datetime.now(timezone.utc).isoformat(),
        }

    doc_path = f"projects/{project}/databases/(default)/documents/{collection}/{document_id}"
    url = f"{FIRESTORE_BASE}/{doc_path}"
    headers = {"Authorization": f"Bearer {token}", "Content-Type": "application/json"}

    try:
        if operation == "delete":
            resp = requests.delete(url, headers=headers, timeout=15)
            return {
                "status": "ok" if resp.status_code in (200, 204) else "error",
                "data": {"operation": "delete", "document": f"{collection}/{document_id}"},
                "timestamp": datetime.now(timezone.utc).isoformat(),
            }

        # Add metadata fields automatically
        all_fields = {
            **fields,
            "_updated_at": datetime.now(timezone.utc).isoformat(),
            "_collection": collection,
        }
        firestore_fields = {k: _to_firestore_value(v) for k, v in all_fields.items()}
        body = {"fields": firestore_fields}

        if operation == "update":
            field_paths = ",".join(f"updateMask.fieldPaths={k}" for k in fields.keys())
            resp = requests.patch(f"{url}?{field_paths}", headers=headers, json=body, timeout=15)
        else:  # create
            resp = requests.patch(url, headers=headers, json=body, timeout=15)

        resp.raise_for_status()
        return {
            "status": "ok",
            "data": {
                "operation": operation,
                "document": f"{collection}/{document_id}",
                "fields_written": list(fields.keys()),
            },
            "timestamp": datetime.now(timezone.utc).isoformat(),
        }

    except Exception as e:
        return {
            "status": "error",
            "data": {"message": str(e)},
            "timestamp": datetime.now(timezone.utc).isoformat(),
        }
