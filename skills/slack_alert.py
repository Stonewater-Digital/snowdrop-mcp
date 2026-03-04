"""
Executive Summary
-----------------
Slack alert skill for Snowdrop. Sends messages to a Slack channel using the
Slack Web API (chat.postMessage). Used for real-time alerts to Thunder while
Telegram is pending (+888 number unlock ~Feb 24).

Actions:
  send    — post a plain text or markdown message to a channel
  ping    — send a test "I'm alive" message to verify connectivity

Env vars required:
  SLACK_BOT_TOKEN   — xoxb-... token from Slack App → OAuth & Permissions
  SLACK_CHANNEL_ID  — Channel ID (not name) e.g. C08XXXXXXXX

MCP Tool Name: slack_alert
"""

import os
import logging
from datetime import datetime, timezone

import requests

logger = logging.getLogger(__name__)

TOOL_META = {
    "name": "slack_alert",
    "description": (
        "Send a message to Snowdrop's Slack channel. Used for real-time alerts "
        "to Thunder: price moves, audit results, integrity alerts, status updates. "
        "Actions: send (post message), ping (connectivity test)."
    ),
    "inputSchema": {
        "type": "object",
        "properties": {
            "action": {
                "type": "string",
                "enum": ["send", "ping"],
                "description": "Operation: 'send' to post a message, 'ping' for connectivity test.",
            },
            "message": {
                "type": "string",
                "description": "Message text (plain text or Slack mrkdwn). Required for 'send'.",
            },
            "channel_id": {
                "type": "string",
                "description": "Slack channel ID (falls back to SLACK_CHANNEL_ID env var).",
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

_SLACK_API = "https://slack.com/api/chat.postMessage"


def _now_iso() -> str:
    return datetime.now(timezone.utc).isoformat()


def _wrap(status: str, data: dict) -> dict:
    return {"status": status, "data": data, "timestamp": _now_iso()}


def _post_message(token: str, channel: str, text: str) -> dict:
    resp = requests.post(
        _SLACK_API,
        headers={"Authorization": f"Bearer {token}", "Content-Type": "application/json"},
        json={"channel": channel, "text": text, "mrkdwn": True},
        timeout=15,
    )
    resp.raise_for_status()
    body = resp.json()
    if not body.get("ok"):
        raise RuntimeError(f"Slack API error: {body.get('error', 'unknown')}")
    return body


def slack_alert(
    action: str,
    message: str = "",
    channel_id: str = "",
) -> dict:
    """Send alerts to Thunder's Slack workspace."""
    token = os.environ.get("SLACK_BOT_TOKEN", "")
    channel = channel_id or os.environ.get("SLACK_CHANNEL_ID", "")

    if not token:
        return _wrap("error", {"message": "SLACK_BOT_TOKEN not set. Add to .env."})
    if not channel:
        return _wrap("error", {"message": "SLACK_CHANNEL_ID not set. Add to .env or pass channel_id."})

    try:
        if action == "ping":
            body = _post_message(token, channel, ":snowflake: *Snowdrop online.* Ping received — I'm alive and watching.")
            return _wrap("ok", {"slack_ts": body.get("ts"), "channel": body.get("channel")})

        elif action == "send":
            if not message:
                return _wrap("error", {"message": "'message' is required for action='send'."})
            body = _post_message(token, channel, message)
            return _wrap("ok", {"slack_ts": body.get("ts"), "channel": body.get("channel")})

        else:
            return _wrap("error", {"message": f"Unknown action '{action}'. Use: send, ping"})

    except Exception as exc:
        logger.exception("slack_alert error")
        return _wrap("error", {"message": str(exc)})
