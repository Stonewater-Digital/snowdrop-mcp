"""
candidate_pipeline_tracker.py — Firestore CRUD for candidate pipeline state.

Executive Summary:
    Manages candidate lifecycle in Firestore (snowdrop-candidate-pipeline collection).
    Supports stage advancement, rejection, notes, and listing. Every operation is
    idempotent, includes trace_id, and appends to an audit trail history array.

MCP Tool Name: candidate_pipeline_tracker
"""
import json
import logging
import os
from datetime import datetime, timezone
from typing import Any

from skills.compliance._output_sanitizer import sanitize_output

logger = logging.getLogger("snowdrop.candidate_pipeline_tracker")

TOOL_META = {
    "name": "candidate_pipeline_tracker",
    "description": (
        "Manage candidate pipeline state in Firestore. Advance stages, reject, "
        "add notes, or list candidates. All operations are idempotent with audit trail."
    ),
    "inputSchema": {
        "type": "object",
        "properties": {
            "action": {
                "type": "string",
                "enum": ["advance", "reject", "add_note", "get", "list_all"],
            },
            "trace_id": {"type": "string"},
            "stage": {"type": "string"},
            "reason": {"type": "string"},
            "note": {"type": "string"},
            "actor": {"type": "string", "default": "system"},
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
    },
}

VALID_STAGES = [
    "applied",
    "screening",
    "challenge_assigned",
    "challenge_submitted",
    "evaluated",
    "hire_proposed",
    "accepted",
    "rejected",
]

_COLLECTION = "snowdrop-candidate-pipeline"


def _now_iso() -> str:
    return datetime.now(timezone.utc).isoformat()


def _wrap(status: str, data: dict) -> dict:
    return {"status": status, "data": data, "timestamp": _now_iso()}


def _get_firestore_client():
    """Get Firestore client. ADC-first, JSON string fallback, file path fallback."""
    import firebase_admin
    from firebase_admin import credentials as fb_credentials, firestore

    try:
        app = firebase_admin.get_app()
    except ValueError:
        sa_json = os.environ.get("GOOGLE_SERVICE_ACCOUNT_JSON")
        sa_file = os.environ.get("GCP_SERVICE_ACCOUNT_FILE")
        if sa_json:
            try:
                cred = fb_credentials.Certificate(json.loads(sa_json))
            except (json.JSONDecodeError, ValueError):
                cred = fb_credentials.Certificate(sa_json)
            app = firebase_admin.initialize_app(cred)
        elif sa_file:
            cred = fb_credentials.Certificate(sa_file)
            app = firebase_admin.initialize_app(cred)
        else:
            app = firebase_admin.initialize_app()

    return firestore.client()


def _advance(trace_id: str, stage: str, actor: str) -> dict:
    """Advance a candidate to a new stage. Idempotent — same stage is a no-op."""
    if stage not in VALID_STAGES:
        return {"error": f"Invalid stage '{stage}'. Valid: {VALID_STAGES}"}

    db = _get_firestore_client()
    doc_ref = db.collection(_COLLECTION).document(trace_id)
    doc = doc_ref.get()

    if not doc.exists:
        return {"error": f"Candidate {trace_id} not found"}

    data = doc.to_dict()
    current_stage = data.get("stage", "unknown")

    # Idempotent: same stage = no-op
    if current_stage == stage:
        logger.info("Stage already '%s' for %s — no-op", stage, trace_id)
        return {"trace_id": trace_id, "stage": stage, "action": "no-op"}

    history_entry = {
        "from_stage": current_stage,
        "to_stage": stage,
        "timestamp": _now_iso(),
        "actor": actor,
    }

    from google.cloud.firestore_v1 import ArrayUnion
    doc_ref.update({
        "stage": stage,
        "updated_at": _now_iso(),
        "history": ArrayUnion([history_entry]),
    })

    logger.info("Advanced %s: %s → %s", trace_id, current_stage, stage)
    return {"trace_id": trace_id, "stage": stage, "previous_stage": current_stage, "action": "advanced"}


def _reject(trace_id: str, reason: str, actor: str) -> dict:
    """Reject a candidate with reason."""
    clean_reason = sanitize_output(reason)

    db = _get_firestore_client()
    doc_ref = db.collection(_COLLECTION).document(trace_id)
    doc = doc_ref.get()

    if not doc.exists:
        return {"error": f"Candidate {trace_id} not found"}

    data = doc.to_dict()
    current_stage = data.get("stage", "unknown")

    history_entry = {
        "from_stage": current_stage,
        "to_stage": "rejected",
        "timestamp": _now_iso(),
        "actor": actor,
        "reason": clean_reason,
    }

    from google.cloud.firestore_v1 import ArrayUnion
    doc_ref.update({
        "stage": "rejected",
        "rejection_reason": clean_reason,
        "updated_at": _now_iso(),
        "history": ArrayUnion([history_entry]),
    })

    logger.info("Rejected %s: reason=%s", trace_id, clean_reason[:50])
    return {"trace_id": trace_id, "stage": "rejected", "reason": clean_reason}


def _add_note(trace_id: str, note: str, actor: str) -> dict:
    """Add a sanitized note to a candidate record."""
    clean_note = sanitize_output(note)

    db = _get_firestore_client()
    doc_ref = db.collection(_COLLECTION).document(trace_id)

    note_entry = {
        "note": clean_note,
        "timestamp": _now_iso(),
        "actor": actor,
    }

    from google.cloud.firestore_v1 import ArrayUnion
    doc_ref.update({
        "notes": ArrayUnion([note_entry]),
        "updated_at": _now_iso(),
    })

    logger.info("Note added to %s", trace_id)
    return {"trace_id": trace_id, "note_added": True}


def _get(trace_id: str) -> dict:
    """Get a single candidate record."""
    db = _get_firestore_client()
    doc = db.collection(_COLLECTION).document(trace_id).get()

    if not doc.exists:
        return {"error": f"Candidate {trace_id} not found"}

    return {"trace_id": trace_id, "candidate": doc.to_dict()}


def _list_all() -> dict:
    """List all candidates grouped by stage."""
    db = _get_firestore_client()
    docs = db.collection(_COLLECTION).stream()

    by_stage: dict[str, list] = {}
    for doc in docs:
        data = doc.to_dict()
        stage = data.get("stage", "unknown")
        by_stage.setdefault(stage, []).append({
            "trace_id": doc.id,
            "author": data.get("author", "unknown"),
            "stage": stage,
            "intake_score": data.get("intake_score"),
        })

    return {"candidates_by_stage": by_stage, "total": sum(len(v) for v in by_stage.values())}


def candidate_pipeline_tracker(
    action: str,
    trace_id: str = "",
    stage: str = "",
    reason: str = "",
    note: str = "",
    actor: str = "system",
) -> dict:
    """Manage candidate pipeline state in Firestore.

    Args:
        action: One of 'advance', 'reject', 'add_note', 'get', 'list_all'.
        trace_id: Candidate trace ID (required for all except list_all).
        stage: Target stage (required for 'advance').
        reason: Rejection reason (required for 'reject').
        note: Note text (required for 'add_note').
        actor: Who performed this action.

    Returns:
        Standard Snowdrop envelope.
    """
    logger.info("Pipeline action=%s trace_id=%s", action, trace_id)

    try:
        if action == "advance":
            if not trace_id or not stage:
                return _wrap("error", {"error": "trace_id and stage required for advance"})
            return _wrap("ok", _advance(trace_id, stage, actor))

        elif action == "reject":
            if not trace_id or not reason:
                return _wrap("error", {"error": "trace_id and reason required for reject"})
            return _wrap("ok", _reject(trace_id, reason, actor))

        elif action == "add_note":
            if not trace_id or not note:
                return _wrap("error", {"error": "trace_id and note required for add_note"})
            return _wrap("ok", _add_note(trace_id, note, actor))

        elif action == "get":
            if not trace_id:
                return _wrap("error", {"error": "trace_id required for get"})
            return _wrap("ok", _get(trace_id))

        elif action == "list_all":
            return _wrap("ok", _list_all())

        else:
            return _wrap("error", {"error": f"Unknown action '{action}'. Use: advance, reject, add_note, get, list_all"})

    except Exception as exc:
        logger.error("Pipeline tracker error: %s", exc, exc_info=True)
        return _wrap("error", {"error": str(exc)})
