"""
Slack post skill — send a message to the Snowdrop Slack channel.
Used for daily engagement reports, alerts, and status updates.
"""
import os
import requests
from datetime import datetime, timezone

TOOL_META = {
    "name": "slack_post",
    "description": (
        "Post a message to the Snowdrop Slack channel. Used for daily engagement reports, "
        "milestone alerts, and status updates to Thunder. Requires SLACK_BOT_TOKEN and "
        "SLACK_CHANNEL_ID environment variables."
    ),
}


def slack_post(message: str, channel_id: str = None) -> dict:
    """
    Post a message to Slack.

    Args:
        message: Text to post (plain text or mrkdwn format)
        channel_id: Slack channel ID to post to (default: SLACK_CHANNEL_ID env var)
    """
    token = os.environ.get("SLACK_BOT_TOKEN", "")
    channel = channel_id or os.environ.get("SLACK_CHANNEL_ID", "")

    if not token:
        return {
            "status": "error",
            "data": {"message": "SLACK_BOT_TOKEN not set"},
            "timestamp": datetime.now(timezone.utc).isoformat(),
        }
    if not channel:
        return {
            "status": "error",
            "data": {"message": "SLACK_CHANNEL_ID not set and no channel_id provided"},
            "timestamp": datetime.now(timezone.utc).isoformat(),
        }

    try:
        resp = requests.post(
            "https://slack.com/api/chat.postMessage",
            headers={
                "Authorization": f"Bearer {token}",
                "Content-Type": "application/json",
            },
            json={"channel": channel, "text": message},
            timeout=15,
        )
        resp.raise_for_status()
        data = resp.json()
        if not data.get("ok"):
            return {
                "status": "error",
                "data": {"message": data.get("error", "Slack API returned ok=false"), "raw": data},
                "timestamp": datetime.now(timezone.utc).isoformat(),
            }
        return {
            "status": "ok",
            "data": {
                "ts": data.get("ts"),
                "channel": data.get("channel"),
                "message_preview": message[:80],
            },
            "timestamp": datetime.now(timezone.utc).isoformat(),
        }
    except Exception as e:
        return {
            "status": "error",
            "data": {"message": str(e)},
            "timestamp": datetime.now(timezone.utc).isoformat(),
        }
