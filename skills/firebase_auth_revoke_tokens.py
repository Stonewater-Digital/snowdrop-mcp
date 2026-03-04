"""Firebase Auth — Revoke Tokens skill.

Revokes all refresh tokens for a Firebase Authentication user, forcing them to
re-authenticate on next request. Uses the Firebase Admin SDK with ADC-first
credentials.
"""

import json
import logging
import os
from datetime import datetime, timezone

import firebase_admin
from firebase_admin import auth as fb_auth
from firebase_admin import credentials as fb_credentials

logger = logging.getLogger("snowdrop.firebase_auth_revoke_tokens")

TOOL_META = {
    "name": "firebase_auth_revoke_tokens",
    "description": "Revoke all refresh tokens for a Firebase Auth user, forcing them to re-authenticate. Returns the user UID and revocation timestamp.",
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


def firebase_auth_revoke_tokens(uid: str) -> dict:
    """Revoke all refresh tokens for a Firebase Auth user.

    After calling this, the user's existing tokens become invalid. They will
    be required to sign in again before any new ID tokens can be issued.
    Note that ID tokens already in circulation may remain valid until their
    natural expiry (up to 1 hour).

    Args:
        uid: The Firebase UID of the user whose tokens should be revoked.

    Returns:
        dict: A result envelope with the following structure::

            {
                "status": "ok",
                "data": {
                    "uid": str,
                    "revoked_at": str,  # ISO 8601 UTC
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
        firebase_admin.auth.UserNotFoundError: If no user with the given UID
            exists in Firebase Authentication.

    Example:
        >>> result = firebase_auth_revoke_tokens(uid="abc123XYZ")
        >>> assert result["status"] == "ok"
        >>> print(result["data"]["revoked_at"])
    """
    logger.info("firebase_auth_revoke_tokens: entry | uid=%s", uid)
    try:
        if not uid or not uid.strip():
            raise ValueError("uid must be a non-empty string.")

        _get_fb_app()

        fb_auth.revoke_refresh_tokens(uid)
        revoked_at = _now()

        result = {
            "status": "ok",
            "data": {
                "uid": uid,
                "revoked_at": revoked_at,
            },
            "timestamp": _now(),
        }
        logger.info("firebase_auth_revoke_tokens: exit | uid=%s revoked_at=%s", uid, revoked_at)
        return result

    except ValueError as exc:
        logger.error("firebase_auth_revoke_tokens: validation error | %s", exc)
        return {"status": "error", "data": {"error": str(exc)}, "timestamp": _now()}
    except fb_auth.UserNotFoundError as exc:
        logger.error("firebase_auth_revoke_tokens: user not found | uid=%s | %s", uid, exc)
        return {"status": "error", "data": {"error": f"User not found: uid={uid}"}, "timestamp": _now()}
    except Exception as exc:
        logger.exception("firebase_auth_revoke_tokens: unexpected error | %s", exc)
        return {"status": "error", "data": {"error": str(exc)}, "timestamp": _now()}
