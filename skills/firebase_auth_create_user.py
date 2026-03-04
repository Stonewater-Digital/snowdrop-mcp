"""Firebase Auth — Create User skill.

Creates a new Firebase Authentication user account using the Firebase Admin SDK.
Supports ADC credentials on Cloud Run and GOOGLE_SERVICE_ACCOUNT_JSON for local dev.
"""

import json
import logging
import os
from datetime import datetime, timezone

import firebase_admin
from firebase_admin import auth as fb_auth
from firebase_admin import credentials as fb_credentials

logger = logging.getLogger("snowdrop.firebase_auth_create_user")

TOOL_META = {
    "name": "firebase_auth_create_user",
    "description": "Create a new Firebase Auth user account. Returns the user's UID, email, and creation time.",
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


def firebase_auth_create_user(
    email: str,
    password: str,
    display_name: str | None = None,
    phone_number: str | None = None,
    disabled: bool = False,
) -> dict:
    """Create a new Firebase Auth user account.

    Args:
        email: The user's email address. Must be a valid email format.
        password: The user's initial password. Must be at least 6 characters.
        display_name: Optional human-readable display name for the user.
        phone_number: Optional E.164-formatted phone number (e.g. '+15005550006').
        disabled: Whether the new account should be created in a disabled state.
            Defaults to False.

    Returns:
        dict: A result envelope with the following structure::

            {
                "status": "ok",
                "data": {
                    "uid": str,
                    "email": str,
                    "display_name": str | None,
                    "creation_time": str,  # ISO 8601 UTC
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
        firebase_admin.auth.EmailAlreadyExistsError: If a user with the given
            email already exists.
        firebase_admin.auth.PhoneNumberAlreadyExistsError: If a user with the
            given phone number already exists.

    Example:
        >>> result = firebase_auth_create_user(
        ...     email="alice@example.com",
        ...     password="s3cur3P@ss",
        ...     display_name="Alice Smith",
        ... )
        >>> assert result["status"] == "ok"
        >>> print(result["data"]["uid"])
    """
    logger.info(
        "firebase_auth_create_user: entry | email=%s display_name=%s disabled=%s",
        email,
        display_name,
        disabled,
    )
    try:
        _get_fb_app()

        kwargs: dict = {
            "email": email,
            "password": password,
            "disabled": disabled,
        }
        if display_name is not None:
            kwargs["display_name"] = display_name
        if phone_number is not None:
            kwargs["phone_number"] = phone_number

        user: fb_auth.UserRecord = fb_auth.create_user(**kwargs)

        creation_time = (
            datetime.fromtimestamp(
                user.user_metadata.creation_timestamp / 1000, tz=timezone.utc
            ).isoformat()
            if user.user_metadata and user.user_metadata.creation_timestamp
            else _now()
        )

        result = {
            "status": "ok",
            "data": {
                "uid": user.uid,
                "email": user.email,
                "display_name": user.display_name,
                "creation_time": creation_time,
            },
            "timestamp": _now(),
        }
        logger.info(
            "firebase_auth_create_user: exit | uid=%s email=%s",
            user.uid,
            user.email,
        )
        return result

    except fb_auth.EmailAlreadyExistsError as exc:
        logger.error("firebase_auth_create_user: email already exists | %s", exc)
        return {"status": "error", "data": {"error": f"Email already exists: {email}"}, "timestamp": _now()}
    except fb_auth.PhoneNumberAlreadyExistsError as exc:
        logger.error("firebase_auth_create_user: phone already exists | %s", exc)
        return {"status": "error", "data": {"error": f"Phone number already exists: {phone_number}"}, "timestamp": _now()}
    except Exception as exc:
        logger.exception("firebase_auth_create_user: unexpected error | %s", exc)
        return {"status": "error", "data": {"error": str(exc)}, "timestamp": _now()}
