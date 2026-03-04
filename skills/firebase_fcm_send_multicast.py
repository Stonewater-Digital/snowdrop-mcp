"""Firebase FCM multicast push notification skill.

Sends a push notification to up to 500 device tokens simultaneously using
Firebase Cloud Messaging via the firebase-admin SDK.
"""

import json
import logging
import os
from datetime import datetime, timezone

import firebase_admin
from firebase_admin import credentials as fb_credentials
from firebase_admin import messaging

logger = logging.getLogger("snowdrop.firebase_fcm_send_multicast")

TOOL_META = {
    "name": "firebase_fcm_send_multicast",
    "description": "Send FCM push notification to up to 500 device tokens simultaneously. Returns success_count, failure_count, and per-token results.",
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


def firebase_fcm_send_multicast(
    tokens: list[str],
    title: str,
    body: str,
    data: dict | None = None,
) -> dict:
    """Send an FCM push notification to up to 500 device tokens simultaneously.

    Uses firebase-admin's send_each_for_multicast which batches the sends and
    returns per-token results. Tokens list is validated to be non-empty and
    within the 500-token FCM limit.

    Args:
        tokens: List of FCM device registration tokens. Maximum 500 tokens.
        title: Notification title text displayed to the user.
        body: Notification body text displayed to the user.
        data: Optional dictionary of string key-value pairs to attach as data payload.
            All values will be coerced to strings.

    Returns:
        dict: Standard Snowdrop response envelope.
            On success: {
                "status": "ok",
                "data": {
                    "success_count": int,
                    "failure_count": int,
                    "responses": [{"token": str, "success": bool, "message_id": str|None, "error": str|None}]
                },
                "timestamp": str
            }
            On error: {"status": "error", "data": {"error": str}, "timestamp": str}

    Raises:
        ValueError: If tokens list is empty or exceeds 500 entries.
        firebase_admin.exceptions.FirebaseError: If the FCM API returns an error.

    Example:
        >>> result = firebase_fcm_send_multicast(
        ...     tokens=["token_A", "token_B", "token_C"],
        ...     title="Flash sale!",
        ...     body="50% off everything for the next 2 hours",
        ...     data={"sale_id": "flash_001"},
        ... )
        >>> result["status"]
        'ok'
        >>> result["data"]["success_count"]
        3
    """
    logger.info("firebase_fcm_send_multicast entered | token_count=%d", len(tokens))

    if not tokens:
        msg = "tokens list must not be empty."
        logger.error("firebase_fcm_send_multicast validation error: %s", msg)
        return {"status": "error", "data": {"error": msg}, "timestamp": _now()}

    if len(tokens) > 500:
        msg = f"tokens list exceeds FCM limit of 500 (got {len(tokens)})."
        logger.error("firebase_fcm_send_multicast validation error: %s", msg)
        return {"status": "error", "data": {"error": msg}, "timestamp": _now()}

    try:
        _get_fb_app()

        notification = messaging.Notification(title=title, body=body)

        str_data: dict[str, str] | None = None
        if data:
            str_data = {k: str(v) for k, v in data.items()}

        multicast_message = messaging.MulticastMessage(
            tokens=tokens,
            notification=notification,
            data=str_data,
        )

        batch_response = messaging.send_each_for_multicast(multicast_message)

        responses = []
        for idx, resp in enumerate(batch_response.responses):
            entry: dict = {
                "token": tokens[idx],
                "success": resp.success,
                "message_id": resp.message_id if resp.success else None,
                "error": str(resp.exception) if resp.exception else None,
            }
            responses.append(entry)

        logger.info(
            "firebase_fcm_send_multicast success | success=%d failure=%d",
            batch_response.success_count,
            batch_response.failure_count,
        )
        return {
            "status": "ok",
            "data": {
                "success_count": batch_response.success_count,
                "failure_count": batch_response.failure_count,
                "responses": responses,
            },
            "timestamp": _now(),
        }

    except Exception as exc:
        logger.error("firebase_fcm_send_multicast error: %s", exc, exc_info=True)
        return {"status": "error", "data": {"error": str(exc)}, "timestamp": _now()}
