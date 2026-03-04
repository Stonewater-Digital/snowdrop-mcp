"""Firebase Auth — Get User skill.

Looks up a Firebase Authentication user by UID or email address using the
Firebase Admin SDK. Supports ADC on Cloud Run and GOOGLE_SERVICE_ACCOUNT_JSON
for local dev.
"""

import json
import logging
import os
from datetime import datetime, timezone

import firebase_admin
from firebase_admin import auth as fb_auth
from firebase_admin import credentials as fb_credentials

logger = logging.getLogger("snowdrop.firebase_auth_get_user")

TOOL_META = {
    "name": "firebase_auth_get_user",
    "description": "Look up a Firebase Auth user by UID or email address. Returns user profile data.",
    "tier": "free",
}

_fb_app = None


def _get_fb_app() -> firebase_admin.App:
    """Return initialized firebase_admin app. Idempotent.

    Returns:
        The initialized firebase_admin.App instance.
    """
    global _fb_app
    if _fb_app is not None:
        return _fb_app
    sa_json = os.environ.get("GOOGLE_SERVICE_ACCOUNT_JSON")
    if sa_json:
        cred = fb_credentials.Certificate(json.loads(sa_json))
        _fb_app = firebase_admin.initialize_app(cred)
    else:
        # Cloud Run: ADC via attached IAM service account
        _fb_app = firebase_admin.initialize_app()
    return _fb_app


def _now() -> str:
    return datetime.now(timezone.utc).isoformat()


def _ms_to_iso(ms: int | None) -> str | None:
    """Convert a millisecond epoch timestamp to an ISO 8601 UTC string."""
    if ms is None:
        return None
    return datetime.fromtimestamp(ms / 1000, tz=timezone.utc).isoformat()


def firebase_auth_get_user(
    uid: str | None = None,
    email: str | None = None,
) -> dict:
    """Look up a Firebase Auth user by UID or email address.

    Exactly one of ``uid`` or ``email`` must be supplied. Providing both or
    neither will return an error.

    Args:
        uid: The Firebase UID of the user to retrieve.
        email: The email address of the user to retrieve.

    Returns:
        dict: A result envelope with the following structure::

            {
                "status": "ok",
                "data": {
                    "uid": str,
                    "email": str | None,
                    "display_name": str | None,
                    "phone_number": str | None,
                    "disabled": bool,
                    "creation_time": str | None,   # ISO 8601 UTC
                    "last_sign_in": str | None,    # ISO 8601 UTC
                },
                "timestamp": str,  # ISO 8601 UTC
            }

        On error::

            {
                "status": "error",
                "data": {"error": str},
                "timestamp": str,
            }

    Raises:
        firebase_admin.auth.UserNotFoundError: If no user matches the given
            uid or email.

    Example:
        >>> result = firebase_auth_get_user(email="alice@example.com")
        >>> assert result["status"] == "ok"
        >>> print(result["data"]["uid"])

        >>> result = firebase_auth_get_user(uid="abc123XYZ")
        >>> print(result["data"]["display_name"])
    """
    logger.info(
        "firebase_auth_get_user: entry | uid=%s email=%s",
        uid,
        email,
    )
    try:
        if uid is None and email is None:
            raise ValueError("Exactly one of 'uid' or 'email' must be provided.")
        if uid is not None and email is not None:
            raise ValueError("Provide either 'uid' or 'email', not both.")

        _get_fb_app()

        if uid is not None:
            user: fb_auth.UserRecord = fb_auth.get_user(uid)
        else:
            user = fb_auth.get_user_by_email(email)

        meta = user.user_metadata
        creation_time = _ms_to_iso(meta.creation_timestamp if meta else None)
        last_sign_in = _ms_to_iso(meta.last_sign_in_timestamp if meta else None)

        result = {
            "status": "ok",
            "data": {
                "uid": user.uid,
                "email": user.email,
                "display_name": user.display_name,
                "phone_number": user.phone_number,
                "disabled": user.disabled,
                "creation_time": creation_time,
                "last_sign_in": last_sign_in,
            },
            "timestamp": _now(),
        }
        logger.info(
            "firebase_auth_get_user: exit | uid=%s email=%s",
            user.uid,
            user.email,
        )
        return result

    except ValueError as exc:
        logger.error("firebase_auth_get_user: validation error | %s", exc)
        return {"status": "error", "data": {"error": str(exc)}, "timestamp": _now()}
    except fb_auth.UserNotFoundError as exc:
        logger.error("firebase_auth_get_user: user not found | uid=%s email=%s | %s", uid, email, exc)
        return {"status": "error", "data": {"error": f"User not found: uid={uid}, email={email}"}, "timestamp": _now()}
    except Exception as exc:
        logger.exception("firebase_auth_get_user: unexpected error | %s", exc)
        return {"status": "error", "data": {"error": str(exc)}, "timestamp": _now()}
