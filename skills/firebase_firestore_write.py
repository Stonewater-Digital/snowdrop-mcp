"""Firebase Firestore write skill.

Sets, updates, or deletes a Firestore document using the firebase-admin
Firestore client. Supports merge mode for partial field updates.
"""

import json
import logging
import os
from datetime import datetime, timezone

import firebase_admin
from firebase_admin import credentials as fb_credentials
from firebase_admin import firestore

logger = logging.getLogger("snowdrop.firebase_firestore_write")

TOOL_META = {
    "name": "firebase_firestore_write",
    "description": "Set, update, or delete a Firestore document. Use operation='set' to replace, 'update' to merge fields, 'delete' to remove document.",
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


_VALID_OPERATIONS = {"set", "update", "delete"}


def firebase_firestore_write(
    collection: str,
    document_id: str,
    data: dict | None = None,
    operation: str = "set",
    merge: bool = False,
) -> dict:
    """Set, update, or delete a Firestore document.

    Writes to a specific document within a Firestore collection. The operation
    controls whether the document is replaced, partially updated, or removed.

    Args:
        collection: Firestore collection name, e.g. "users" or "orders".
        document_id: The ID of the document to write to or delete.
        data: Document data to write. Required for "set" and "update" operations.
            Ignored for "delete". For "update", only the provided fields are
            modified; unlisted fields remain unchanged.
        operation: Write operation to perform. One of:
            - "set": Replace the document entirely. If merge=True, merges provided
              fields instead of replacing (equivalent to "update" but creates doc
              if missing).
            - "update": Update only the specified fields. Document must exist.
            - "delete": Remove the document entirely. data is ignored.
            Defaults to "set".
        merge: When operation="set", pass merge=True to merge fields into the
            existing document rather than replacing it. Has no effect on "update"
            or "delete". Defaults to False.

    Returns:
        dict: Standard Snowdrop response envelope.
            On success: {
                "status": "ok",
                "data": {"collection": str, "document_id": str, "operation": str},
                "timestamp": str
            }
            On error: {"status": "error", "data": {"error": str}, "timestamp": str}

    Raises:
        ValueError: If operation is invalid or data is missing for set/update.
        google.cloud.exceptions.NotFound: If "update" is called on a non-existent doc.
        google.cloud.exceptions.GoogleCloudError: If Firestore returns an API error.

    Example:
        >>> result = firebase_firestore_write(
        ...     collection="users",
        ...     document_id="alice",
        ...     data={"name": "Alice", "score": 42, "active": True},
        ...     operation="set",
        ... )
        >>> result["status"]
        'ok'
        >>> result["data"]["operation"]
        'set'
    """
    logger.info(
        "firebase_firestore_write entered | collection=%s document_id=%s operation=%s",
        collection, document_id, operation,
    )

    if operation not in _VALID_OPERATIONS:
        msg = f"Invalid operation '{operation}'. Must be one of: {sorted(_VALID_OPERATIONS)}."
        logger.error("firebase_firestore_write error: %s", msg)
        return {"status": "error", "data": {"error": msg}, "timestamp": _now()}

    if operation in ("set", "update") and data is None:
        msg = f"data is required for operation='{operation}'."
        logger.error("firebase_firestore_write error: %s", msg)
        return {"status": "error", "data": {"error": msg}, "timestamp": _now()}

    try:
        _get_fb_app()
        db = firestore.client()
        doc_ref = db.collection(collection).document(document_id)

        if operation == "delete":
            doc_ref.delete()
            logger.info(
                "firebase_firestore_write delete success | collection=%s id=%s",
                collection, document_id,
            )
        elif operation == "set":
            doc_ref.set(data, merge=merge)
            logger.info(
                "firebase_firestore_write set success | collection=%s id=%s merge=%s",
                collection, document_id, merge,
            )
        elif operation == "update":
            doc_ref.update(data)
            logger.info(
                "firebase_firestore_write update success | collection=%s id=%s",
                collection, document_id,
            )

        return {
            "status": "ok",
            "data": {
                "collection": collection,
                "document_id": document_id,
                "operation": operation,
            },
            "timestamp": _now(),
        }

    except Exception as exc:
        logger.error("firebase_firestore_write error: %s", exc, exc_info=True)
        return {"status": "error", "data": {"error": str(exc)}, "timestamp": _now()}
