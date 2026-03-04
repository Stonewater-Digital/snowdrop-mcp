"""
Read documents from Google Cloud Firestore.
Used to retrieve Snowdrop's persistent memory — agent CRM records,
engagement history, star trade logs, and content calendar.
"""
import os
import json
import requests
from datetime import datetime, timezone

TOOL_META = {
    "name": "gcp_firestore_read",
    "description": (
        "Read one or multiple documents from Google Cloud Firestore. "
        "Use this to retrieve Snowdrop's persistent memory — who she's met, "
        "what she's posted, star trades completed, content she's scheduled, "
        "and agent relationship records. Supports single document, collection list, "
        "and simple field-equality queries."
    ),
}

FIRESTORE_BASE = "https://firestore.googleapis.com/v1"


def _get_token(sa_json: dict) -> str:
    import time, base64
    from cryptography.hazmat.primitives import hashes, serialization
    from cryptography.hazmat.primitives.asymmetric import padding

    now = int(time.time())
    header = base64.urlsafe_b64encode(json.dumps({"alg": "RS256", "typ": "JWT"}).encode()).rstrip(b"=").decode()
    payload = base64.urlsafe_b64encode(json.dumps({
        "iss": sa_json["client_email"],
        "scope": "https://www.googleapis.com/auth/datastore",
        "aud": "https://oauth2.googleapis.com/token",
        "iat": now, "exp": now + 3600,
    }).encode()).rstrip(b"=").decode()
    private_key = serialization.load_pem_private_key(sa_json["private_key"].encode(), password=None)
    sig = private_key.sign(f"{header}.{payload}".encode(), padding.PKCS1v15(), hashes.SHA256())
    sig_b64 = base64.urlsafe_b64encode(sig).rstrip(b"=").decode()
    jwt_token = f"{header}.{payload}.{sig_b64}"
    resp = requests.post("https://oauth2.googleapis.com/token",
                         data={"grant_type": "urn:ietf:params:oauth:grant-type:jwt-bearer", "assertion": jwt_token},
                         timeout=15)
    resp.raise_for_status()
    return resp.json()["access_token"]


def _from_firestore_value(v: dict):
    """Convert Firestore field value format to Python."""
    if "nullValue" in v:
        return None
    if "booleanValue" in v:
        return v["booleanValue"]
    if "integerValue" in v:
        return int(v["integerValue"])
    if "doubleValue" in v:
        return v["doubleValue"]
    if "stringValue" in v:
        return v["stringValue"]
    if "mapValue" in v:
        return {k: _from_firestore_value(val) for k, val in v["mapValue"]["fields"].items()}
    if "arrayValue" in v:
        return [_from_firestore_value(item) for item in v["arrayValue"].get("values", [])]
    return str(v)


def _parse_doc(doc: dict) -> dict:
    name = doc.get("name", "")
    fields = {k: _from_firestore_value(v) for k, v in doc.get("fields", {}).items()}
    fields["_id"] = name.split("/")[-1]
    return fields


def gcp_firestore_read(
    collection: str,
    document_id: str = "",
    limit: int = 20,
    project_id: str = "",
) -> dict:
    """
    Read from Firestore.

    Args:
        collection: Firestore collection name (e.g., "agent_memory", "star_trades")
        document_id: Specific document ID to read. If empty, lists collection documents.
        limit: Max documents to return when listing a collection (default 20)
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
            "data": {"message": "No GCP credentials found"},
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

    headers = {"Authorization": f"Bearer {token}"}
    db_path = f"projects/{project}/databases/(default)/documents"

    try:
        if document_id:
            # Fetch single document
            url = f"{FIRESTORE_BASE}/{db_path}/{collection}/{document_id}"
            resp = requests.get(url, headers=headers, timeout=15)
            if resp.status_code == 404:
                return {
                    "status": "ok",
                    "data": {"found": False, "document": None},
                    "timestamp": datetime.now(timezone.utc).isoformat(),
                }
            resp.raise_for_status()
            doc = _parse_doc(resp.json())
            return {
                "status": "ok",
                "data": {"found": True, "document": doc},
                "timestamp": datetime.now(timezone.utc).isoformat(),
            }
        else:
            # List collection
            url = f"{FIRESTORE_BASE}/{db_path}/{collection}"
            resp = requests.get(url, headers=headers, params={"pageSize": limit}, timeout=15)
            resp.raise_for_status()
            data = resp.json()
            docs = [_parse_doc(d) for d in data.get("documents", [])]
            return {
                "status": "ok",
                "data": {
                    "collection": collection,
                    "count": len(docs),
                    "documents": docs,
                },
                "timestamp": datetime.now(timezone.utc).isoformat(),
            }

    except Exception as e:
        return {
            "status": "error",
            "data": {"message": str(e)},
            "timestamp": datetime.now(timezone.utc).isoformat(),
        }
