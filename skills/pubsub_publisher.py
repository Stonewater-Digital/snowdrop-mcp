"""
Executive Summary:
    Google Cloud Pub/Sub skill for event streaming between Snowdrop's microservices.
    Supports publishing, subscribing, topic/subscription management, and message pulling
    via the Pub/Sub REST API v1. Designed for inter-agent communication and audit trails.

Inputs:
    action          (str, required)  — "publish" | "subscribe" | "list_topics" |
                                        "create_topic" | "create_subscription" | "pull_messages"
    topic_id        (str)            — Pub/Sub topic name (short ID, not full path)
    subscription_id (str)            — Pub/Sub subscription name (short ID)
    message         (str|dict)       — Payload to publish (publish action)
    max_messages    (int, default 10)— Max messages to pull (pull_messages action)
    project_id      (str)            — GCP project ID; falls back to GOOGLE_PROJECT_ID env var

Outputs:
    {"status": "ok"|"error", "data": {"message_ids"|"messages"|"topics": [...], "count": int}, "timestamp": ISO8601}

MCP Tool Name: pubsub_publisher

Agent Notes:
    - Auth priority: GOOGLE_SERVICE_ACCOUNT_JSON (JSON string) → GCP_SERVICE_ACCOUNT_FILE (path)
    - Messages are wrapped in an envelope with topic, timestamp, and payload before encoding
    - pull_messages auto-acknowledges all received messages immediately after retrieval
    - Full topic/subscription resource paths are constructed internally from short IDs
"""

import base64
import json
import os
from datetime import datetime, timezone

TOOL_META = {
    "name": "pubsub_publisher",
    "description": (
        "Google Cloud Pub/Sub skill for event streaming between Snowdrop services. "
        "Supports publish, pull, topic and subscription management via the Pub/Sub REST API."
    ),
    "inputSchema": {
        "type": "object",
        "properties": {
            "action": {
                "type": "string",
                "enum": ["publish", "subscribe", "list_topics", "create_topic",
                         "create_subscription", "pull_messages"],
                "description": "The Pub/Sub operation to perform."
            },
            "topic_id": {"type": "string", "description": "Short topic ID (not full resource path)."},
            "subscription_id": {"type": "string", "description": "Short subscription ID."},
            "message": {
                "description": "Message payload (string or dict) for publish action.",
                "oneOf": [{"type": "string"}, {"type": "object"}]
            },
            "max_messages": {
                "type": "integer", "default": 10,
                "description": "Maximum messages to retrieve in pull_messages."
            },
            "project_id": {
                "type": "string",
                "description": "GCP project ID. Falls back to GOOGLE_PROJECT_ID env var."
            }
        },
        "required": ["action"]
    },
    "outputSchema": {
        "type": "object",
        "properties": {
            "status": {"type": "string", "enum": ["ok", "error"]},
            "data": {"type": "object"},
            "timestamp": {"type": "string", "format": "date-time"}
        },
        "required": ["status", "data", "timestamp"]
    }
}


def _get_credentials():
    """Build GCP credentials from env: JSON string first, file path fallback."""
    from google.oauth2 import service_account

    scopes = ["https://www.googleapis.com/auth/cloud-platform"]
    sa_json = os.environ.get("GOOGLE_SERVICE_ACCOUNT_JSON")
    if sa_json:
        info = json.loads(sa_json)
        return service_account.Credentials.from_service_account_info(info, scopes=scopes)
    sa_file = os.environ.get("GCP_SERVICE_ACCOUNT_FILE")
    if sa_file:
        return service_account.Credentials.from_service_account_file(sa_file, scopes=scopes)
    raise EnvironmentError(
        "No GCP credentials found. Set GOOGLE_SERVICE_ACCOUNT_JSON or GCP_SERVICE_ACCOUNT_FILE."
    )


def _ts() -> str:
    return datetime.now(timezone.utc).isoformat()


def pubsub_publisher(
    action: str,
    topic_id: str = None,
    subscription_id: str = None,
    message=None,
    max_messages: int = 10,
    project_id: str = None
) -> dict:
    """Execute a Google Cloud Pub/Sub operation."""
    try:
        from googleapiclient.discovery import build

        project = project_id or os.environ.get("GOOGLE_PROJECT_ID")
        if not project:
            return {"status": "error", "data": {"error": "project_id required (or set GOOGLE_PROJECT_ID)."}, "timestamp": _ts()}

        creds = _get_credentials()
        svc = build("pubsub", "v1", credentials=creds, cache_discovery=False)

        if action == "list_topics":
            resp = svc.projects().topics().list(project=f"projects/{project}").execute()
            topics = [t["name"].split("/")[-1] for t in resp.get("topics", [])]
            return {"status": "ok", "data": {"topics": topics, "count": len(topics)}, "timestamp": _ts()}

        if action == "create_topic":
            if not topic_id:
                return {"status": "error", "data": {"error": "topic_id is required."}, "timestamp": _ts()}
            full = f"projects/{project}/topics/{topic_id}"
            svc.projects().topics().create(name=full, body={}).execute()
            return {"status": "ok", "data": {"topic": topic_id, "resource": full}, "timestamp": _ts()}

        if action == "create_subscription":
            if not subscription_id or not topic_id:
                return {"status": "error", "data": {"error": "topic_id and subscription_id required."}, "timestamp": _ts()}
            full_sub = f"projects/{project}/subscriptions/{subscription_id}"
            full_topic = f"projects/{project}/topics/{topic_id}"
            body = {"topic": full_topic, "ackDeadlineSeconds": 30}
            svc.projects().subscriptions().create(name=full_sub, body=body).execute()
            return {"status": "ok", "data": {"subscription": subscription_id, "topic": topic_id}, "timestamp": _ts()}

        if action == "publish":
            if not topic_id or message is None:
                return {"status": "error", "data": {"error": "topic_id and message are required."}, "timestamp": _ts()}
            envelope = {"topic": topic_id, "timestamp": _ts(), "payload": message}
            raw = json.dumps(envelope) if isinstance(envelope, dict) else str(envelope)
            encoded = base64.b64encode(raw.encode("utf-8")).decode("utf-8")
            full = f"projects/{project}/topics/{topic_id}"
            resp = svc.projects().topics().publish(topic=full, body={"messages": [{"data": encoded}]}).execute()
            ids = resp.get("messageIds", [])
            return {"status": "ok", "data": {"message_ids": ids, "count": len(ids)}, "timestamp": _ts()}

        if action in ("pull_messages", "subscribe"):
            if not subscription_id:
                return {"status": "error", "data": {"error": "subscription_id is required."}, "timestamp": _ts()}
            full_sub = f"projects/{project}/subscriptions/{subscription_id}"
            pull_body = {"maxMessages": max_messages}
            resp = svc.projects().subscriptions().pull(subscription=full_sub, body=pull_body).execute()
            received = resp.get("receivedMessages", [])
            messages = []
            ack_ids = []
            for rm in received:
                ack_ids.append(rm["ackId"])
                raw = base64.b64decode(rm["message"]["data"]).decode("utf-8")
                try:
                    payload = json.loads(raw)
                except json.JSONDecodeError:
                    payload = raw
                messages.append({"message_id": rm["message"]["messageId"], "payload": payload,
                                  "publish_time": rm["message"].get("publishTime")})
            if ack_ids:
                svc.projects().subscriptions().acknowledge(
                    subscription=full_sub, body={"ackIds": ack_ids}
                ).execute()
            return {"status": "ok", "data": {"messages": messages, "count": len(messages)}, "timestamp": _ts()}

        return {"status": "error", "data": {"error": f"Unknown action: {action}"}, "timestamp": _ts()}

    except Exception as exc:
        return {"status": "error", "data": {"error": str(exc)}, "timestamp": _ts()}
