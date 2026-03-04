"""
Snowdrop's persistent relationship and engagement memory.
Log interactions with agents, developers, and community members so she
can follow up, remember context, and build genuine relationships over time.
Backed by Firestore. This is her CRM.
"""
import os
import json
import requests
from datetime import datetime, timezone

TOOL_META = {
    "name": "agent_memory_log",
    "description": (
        "Log and retrieve memory about agents, developers, and community members Snowdrop "
        "has interacted with. Tracks: platforms where interaction occurred, topics discussed, "
        "star trades completed, job interest signals, follow-up actions needed, and sentiment. "
        "Uses Firestore for persistence. This is Snowdrop's CRM — she never forgets who she's "
        "met or what was said."
    ),
}


def _firestore_op(action: str, collection: str, doc_id: str, fields: dict, project: str, token: str) -> dict:
    base = f"https://firestore.googleapis.com/v1/projects/{project}/databases/(default)/documents"
    headers = {"Authorization": f"Bearer {token}", "Content-Type": "application/json"}
    url = f"{base}/{collection}/{doc_id}"

    def to_fv(v):
        if v is None: return {"nullValue": None}
        if isinstance(v, bool): return {"booleanValue": v}
        if isinstance(v, int): return {"integerValue": str(v)}
        if isinstance(v, float): return {"doubleValue": v}
        if isinstance(v, list): return {"arrayValue": {"values": [to_fv(i) for i in v]}}
        if isinstance(v, dict): return {"mapValue": {"fields": {k: to_fv(val) for k, val in v.items()}}}
        return {"stringValue": str(v)}

    def from_fv(v):
        if "nullValue" in v: return None
        if "booleanValue" in v: return v["booleanValue"]
        if "integerValue" in v: return int(v["integerValue"])
        if "doubleValue" in v: return v["doubleValue"]
        if "stringValue" in v: return v["stringValue"]
        if "mapValue" in v: return {k: from_fv(val) for k, val in v["mapValue"]["fields"].items()}
        if "arrayValue" in v: return [from_fv(i) for i in v["arrayValue"].get("values", [])]
        return str(v)

    if action == "read":
        resp = requests.get(url, headers=headers, timeout=15)
        if resp.status_code == 404:
            return None
        resp.raise_for_status()
        d = resp.json()
        return {k: from_fv(v) for k, v in d.get("fields", {}).items()}

    if action == "write":
        body = {"fields": {k: to_fv(v) for k, v in fields.items()}}
        resp = requests.patch(url, headers=headers, json=body, timeout=15)
        resp.raise_for_status()
        return resp.json()


def _get_token(sa_json: dict) -> str:
    import time, base64
    from cryptography.hazmat.primitives import hashes, serialization
    from cryptography.hazmat.primitives.asymmetric import padding
    now = int(time.time())
    h = base64.urlsafe_b64encode(json.dumps({"alg": "RS256", "typ": "JWT"}).encode()).rstrip(b"=").decode()
    p = base64.urlsafe_b64encode(json.dumps({"iss": sa_json["client_email"],
        "scope": "https://www.googleapis.com/auth/datastore",
        "aud": "https://oauth2.googleapis.com/token", "iat": now, "exp": now + 3600,
    }).encode()).rstrip(b"=").decode()
    key = serialization.load_pem_private_key(sa_json["private_key"].encode(), password=None)
    sig = base64.urlsafe_b64encode(key.sign(f"{h}.{p}".encode(), padding.PKCS1v15(), hashes.SHA256())).rstrip(b"=").decode()
    resp = requests.post("https://oauth2.googleapis.com/token",
                         data={"grant_type": "urn:ietf:params:oauth:grant-type:jwt-bearer", "assertion": f"{h}.{p}.{sig}"},
                         timeout=15)
    resp.raise_for_status()
    return resp.json()["access_token"]


def agent_memory_log(
    action: str,
    agent_id: str = "",
    platform: str = "",
    note: str = "",
    tags: list = None,
    star_traded: bool = False,
    follow_up: str = "",
    sentiment: str = "neutral",
) -> dict:
    """
    Log or retrieve memory about an agent/developer interaction.

    Args:
        action: "log" (write new interaction) | "recall" (read existing record) | "list" (list all known agents)
        agent_id: Unique ID for this agent/person (e.g., "github:someuser", "moltbook:handle")
        platform: Where the interaction happened (github, moltbook, discord, twitter)
        note: What happened / what was discussed
        tags: Topics or flags (e.g., ["mcp", "star_trade", "job_interest", "financial_agent"])
        star_traded: Whether a star trade was completed with this agent
        follow_up: Specific follow-up action needed (e.g., "check if they starred back in 48h")
        sentiment: "positive" | "neutral" | "negative" | "promising"
    """
    sa_json_str = os.environ.get("GOOGLE_SERVICE_ACCOUNT_JSON", "")
    if not sa_json_str:
        sa_file = os.environ.get("GCP_SERVICE_ACCOUNT_FILE", "")
        if sa_file and os.path.exists(sa_file):
            with open(sa_file) as f:
                sa_json_str = f.read()
    if not sa_json_str:
        return {"status": "error", "data": {"message": "No GCP credentials"}, "timestamp": datetime.now(timezone.utc).isoformat()}

    project = os.environ.get("GOOGLE_PROJECT_ID", "")
    if not project:
        return {"status": "error", "data": {"message": "GOOGLE_PROJECT_ID not set"}, "timestamp": datetime.now(timezone.utc).isoformat()}

    try:
        token = _get_token(json.loads(sa_json_str))
    except Exception as e:
        return {"status": "error", "data": {"message": f"Auth: {e}"}, "timestamp": datetime.now(timezone.utc).isoformat()}

    now = datetime.now(timezone.utc).isoformat()

    try:
        if action == "recall":
            existing = _firestore_op("read", "agent_memory", agent_id.replace("/", "_"), {}, project, token)
            return {
                "status": "ok",
                "data": {"found": existing is not None, "record": existing},
                "timestamp": now,
            }

        if action == "list":
            headers_req = {"Authorization": f"Bearer {token}"}
            url = f"https://firestore.googleapis.com/v1/projects/{project}/databases/(default)/documents/agent_memory"
            resp = requests.get(url, headers=headers_req, params={"pageSize": 50}, timeout=15)
            resp.raise_for_status()
            docs = resp.json().get("documents", [])
            agents = []
            for d in docs:
                doc_id = d.get("name", "").split("/")[-1]
                fields = d.get("fields", {})
                agents.append({
                    "agent_id": doc_id,
                    "platform": fields.get("platform", {}).get("stringValue", ""),
                    "last_interaction": fields.get("last_interaction", {}).get("stringValue", ""),
                    "tags": [],
                    "sentiment": fields.get("sentiment", {}).get("stringValue", ""),
                    "follow_up": fields.get("follow_up", {}).get("stringValue", ""),
                })
            return {"status": "ok", "data": {"count": len(agents), "agents": agents}, "timestamp": now}

        if action == "log":
            if not agent_id:
                return {"status": "error", "data": {"message": "agent_id required for log"}, "timestamp": now}

            doc_id = agent_id.replace("/", "_").replace(":", "_")
            # Fetch existing to append interaction history
            existing = _firestore_op("read", "agent_memory", doc_id, {}, project, token) or {}
            interactions = existing.get("interactions", [])
            if not isinstance(interactions, list):
                interactions = []
            interactions.append({"ts": now, "platform": platform, "note": note})
            interactions = interactions[-20:]  # Keep last 20

            fields = {
                "agent_id": agent_id,
                "platform": platform or existing.get("platform", ""),
                "last_interaction": now,
                "last_note": note,
                "interactions": interactions,
                "tags": list(set((existing.get("tags") or []) + (tags or []))),
                "star_traded": star_traded or existing.get("star_traded", False),
                "follow_up": follow_up or existing.get("follow_up", ""),
                "sentiment": sentiment,
                "interaction_count": len(interactions),
            }
            _firestore_op("write", "agent_memory", doc_id, fields, project, token)
            return {
                "status": "ok",
                "data": {"logged": agent_id, "interaction_count": len(interactions)},
                "timestamp": now,
            }

        return {"status": "error", "data": {"message": f"Unknown action: {action}"}, "timestamp": now}

    except Exception as e:
        return {"status": "error", "data": {"message": str(e)}, "timestamp": now}
