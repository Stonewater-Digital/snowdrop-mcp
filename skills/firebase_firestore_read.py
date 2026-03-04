"""Firebase Firestore read skill.

Reads one document by ID or queries a collection with optional filters
using the firebase-admin Firestore client.
"""

import json
import logging
import os
from datetime import datetime, timezone

import firebase_admin
from firebase_admin import credentials as fb_credentials
from firebase_admin import firestore

logger = logging.getLogger("snowdrop.firebase_firestore_read")

TOOL_META = {
    "name": "firebase_firestore_read",
    "description": "Read a Firestore document by collection+document ID, or query a collection with optional filters. Returns document data as JSON.",
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


def _serialize_value(value) -> object:
    """Recursively convert Firestore-specific types to JSON-serializable Python objects."""
    from google.cloud.firestore_v1 import DocumentReference
    from google.protobuf.timestamp_pb2 import Timestamp

    if isinstance(value, dict):
        return {k: _serialize_value(v) for k, v in value.items()}
    if isinstance(value, list):
        return [_serialize_value(v) for v in value]
    if hasattr(value, "isoformat"):
        return value.isoformat()
    if isinstance(value, DocumentReference):
        return value.path
    return value


def firebase_firestore_read(
    collection: str,
    document_id: str | None = None,
    filters: list[dict] | None = None,
    limit: int = 100,
) -> dict:
    """Read a Firestore document by ID, or query a collection with optional filters.

    When document_id is provided, returns that single document. Otherwise,
    queries the collection and returns matching documents up to the limit.
    Filters follow the Firestore where() pattern using field/op/value triples.

    Args:
        collection: Firestore collection name, e.g. "users" or "orders/2024/items".
        document_id: Document ID to fetch directly. When provided, filters and
            limit are ignored.
        filters: List of filter dictionaries for collection queries. Each filter must
            contain:
            - "field" (str): The document field to filter on.
            - "op" (str): Comparison operator, one of "==", "!=", "<", "<=", ">",
              ">=", "array_contains", "in", "not_in".
            - "value" (any): The value to compare against.
        limit: Maximum number of documents to return when querying. Defaults to 100.
            Ignored when document_id is provided.

    Returns:
        dict: Standard Snowdrop response envelope.
            Single document: {
                "status": "ok",
                "data": {"document_id": str, "data": dict|None, "exists": bool},
                "timestamp": str
            }
            Collection query: {
                "status": "ok",
                "data": {"count": int, "documents": [{"id": str, "data": dict}]},
                "timestamp": str
            }
            On error: {"status": "error", "data": {"error": str}, "timestamp": str}

    Raises:
        google.cloud.exceptions.GoogleCloudError: If Firestore returns an API error.

    Example:
        >>> result = firebase_firestore_read(
        ...     collection="users",
        ...     filters=[{"field": "active", "op": "==", "value": True}],
        ...     limit=10,
        ... )
        >>> result["status"]
        'ok'
        >>> result["data"]["count"]
        3
    """
    logger.info(
        "firebase_firestore_read entered | collection=%s document_id=%s",
        collection, document_id,
    )

    try:
        _get_fb_app()
        db = firestore.client()

        if document_id is not None:
            doc_ref = db.collection(collection).document(document_id)
            doc = doc_ref.get()
            doc_data = _serialize_value(doc.to_dict()) if doc.exists else None
            logger.info(
                "firebase_firestore_read single doc | collection=%s id=%s exists=%s",
                collection, document_id, doc.exists,
            )
            return {
                "status": "ok",
                "data": {
                    "document_id": document_id,
                    "data": doc_data,
                    "exists": doc.exists,
                },
                "timestamp": _now(),
            }

        # Collection query
        query = db.collection(collection)

        if filters:
            for f in filters:
                field = f["field"]
                op = f["op"]
                value = f["value"]
                query = query.where(filter=firestore.FieldFilter(field, op, value))

        query = query.limit(limit)
        docs = query.stream()

        documents = []
        for doc in docs:
            documents.append({
                "id": doc.id,
                "data": _serialize_value(doc.to_dict()),
            })

        logger.info(
            "firebase_firestore_read query success | collection=%s count=%d",
            collection, len(documents),
        )
        return {
            "status": "ok",
            "data": {"count": len(documents), "documents": documents},
            "timestamp": _now(),
        }

    except Exception as exc:
        logger.error("firebase_firestore_read error: %s", exc, exc_info=True)
        return {"status": "error", "data": {"error": str(exc)}, "timestamp": _now()}
