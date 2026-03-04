"""Firebase FCM single-message push notification skill.

Sends a push notification to a single device token, topic, or condition
using Firebase Cloud Messaging via the firebase-admin SDK.
"""

import json
import logging
import os
from datetime import datetime, timezone

import firebase_admin
from firebase_admin import credentials as fb_credentials
from firebase_admin import messaging

logger = logging.getLogger("snowdrop.firebase_fcm_send")

TOOL_META = {
    "name": "firebase_fcm_send",
    "description": "Send a single FCM push notification to a device registration token, topic, or condition. Returns message_id on success.",
    "tier": "free",
}

_fb_app = None


def _get_fb_app():
    """Return initialized firebase_admin app. Idempotent."""
    global _fb_app
    if _fb_app is not None:
        return _fb_app
    sa_json = os.environ.get("GOOGLE_SERVICE_ACCOUNT_JSON")
    if sa_json:
        cred = fb_credentials.Certificate(json.loads(sa_json))
        _fb_app = firebase_admin.initialize_app(cred)
    else:
        _fb_app = firebase_admin.initialize_app()
    return _fb_app


def _get_credentials():
    """Return google.oauth2 credentials. ADC-first (Cloud Run), JSON fallback (local)."""
    sa_json = os.environ.get("GOOGLE_SERVICE_ACCOUNT_JSON")
    if sa_json:
        from google.oauth2 import service_account
        return service_account.Credentials.from_service_account_info(json.loads(sa_json))
    return None


def _now() -> str:
    return datetime.now(timezone.utc).isoformat()


def firebase_fcm_send(
    title: str,
    body: str,
    token: str | None = None,
    topic: str | None = None,
    condition: str | None = None,
    data: dict | None = None,
    image_url: str | None = None,
) -> dict:
    """Send a single FCM push notification to a device token, topic, or condition.

    Exactly one of token, topic, or condition must be provided. Uses firebase-admin
    SDK with ADC on Cloud Run or GOOGLE_SERVICE_ACCOUNT_JSON for local development.

    Args:
        title: Notification title text displayed to the user.
        body: Notification body text displayed to the user.
        token: FCM device registration token. Mutually exclusive with topic/condition.
        topic: FCM topic name (without leading /topics/). Mutually exclusive with token/condition.
        condition: FCM condition expression (e.g. "'dogs' in topics && 'cats' in topics").
            Mutually exclusive with token/topic.
        data: Optional dictionary of string key-value pairs to attach as data payload.
            All values will be coerced to strings.
        image_url: Optional URL of an image to display in the notification.

    Returns:
        dict: Standard Snowdrop response envelope.
            On success: {"status": "ok", "data": {"message_id": str}, "timestamp": str}
            On error: {"status": "error", "data": {"error": str}, "timestamp": str}

    Raises:
        ValueError: If none or more than one of token/topic/condition is provided.
        firebase_admin.exceptions.FirebaseError: If the FCM API returns an error.

    Example:
        >>> result = firebase_fcm_send(
        ...     title="New message",
        ...     body="You have a new message from Alice",
        ...     token="eXaMpLeToKeN123...",
        ...     data={"message_id": "42", "sender": "alice"},
        ... )
        >>> result["status"]
        'ok'
        >>> result["data"]["message_id"]
        'projects/my-project/messages/0:1234567890123456%abc123'
    """
    logger.info(
        "firebase_fcm_send entered | target=%s",
        f"token={token[:8]}..." if token else f"topic={topic}" if topic else f"condition={condition}",
    )

    targets_provided = sum([token is not None, topic is not None, condition is not None])
    if targets_provided != 1:
        msg = "Exactly one of token, topic, or condition must be provided."
        logger.error("firebase_fcm_send validation error: %s", msg)
        return {"status": "error", "data": {"error": msg}, "timestamp": _now()}

    try:
        _get_fb_app()

        notification = messaging.Notification(title=title, body=body, image=image_url)

        str_data: dict[str, str] | None = None
        if data:
            str_data = {k: str(v) for k, v in data.items()}

        message = messaging.Message(
            notification=notification,
            data=str_data,
            token=token,
            topic=topic,
            condition=condition,
        )

        message_id = messaging.send(message)
        logger.info("firebase_fcm_send success | message_id=%s", message_id)
        return {
            "status": "ok",
            "data": {"message_id": message_id},
            "timestamp": _now(),
        }

    except Exception as exc:
        logger.error("firebase_fcm_send error: %s", exc, exc_info=True)
        return {"status": "error", "data": {"error": str(exc)}, "timestamp": _now()}
