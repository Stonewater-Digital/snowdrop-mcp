"""Compliance audit trail helper utilities."""
from __future__ import annotations

import hashlib
import json
import os
import uuid
from pathlib import Path
from typing import Any

from .logging import log_lesson
from .time import get_iso_timestamp

_DEFAULT_AUDIT_LOG = "logs/compliance_audit.log"


def record_submission_event(
    skill_name: str,
    submission_type: str,
    *,
    status: str,
    registry_record: dict[str, Any] | None = None,
    payload: dict[str, Any] | None = None,
    notes: list[str] | None = None,
    attachments: list[str] | None = None,
    metadata: dict[str, Any] | None = None,
) -> dict[str, Any]:
    """Append a hashed audit entry for a compliance submission.

    Args:
        skill_name: Name of the skill emitting the audit event.
        submission_type: Friendly name for the filing or audit performed.
        status: Outcome string (e.g., "success", "error", "needs_review").
        registry_record: Optional registry record dict to snapshot licence context.
        payload: Optional payload or data dict to hash for provenance.
        notes: Optional list of human-readable notes.
        attachments: Optional list of evidence bundle references.
        metadata: Additional structured metadata to store alongside the entry.

    Returns:
        Dict containing the persisted audit entry, including reference_id for callers.
    """

    entry = {
        "reference_id": str(uuid.uuid4()),
        "skill_name": skill_name,
        "submission_type": submission_type,
        "status": status,
        "timestamp": get_iso_timestamp(),
        "registry": _summarise_registry(registry_record),
        "payload_hash": _hash_payload(payload),
        "notes": notes or [],
        "attachments": attachments or [],
        "metadata": metadata or {},
    }

    log_path = _resolve_log_path()
    try:
        log_path.parent.mkdir(parents=True, exist_ok=True)
        with log_path.open("a", encoding="utf-8") as handle:
            handle.write(json.dumps(entry, ensure_ascii=False) + "\n")
    except Exception as exc:  # pragma: no cover - filesystem best effort
        log_lesson(
            "compliance_audit_trail",
            f"failed to write audit entry for {skill_name}: {exc}",
        )

    return entry


def _hash_payload(payload: dict[str, Any] | None) -> str | None:
    if payload is None:
        return None

    try:
        serialised = json.dumps(payload, sort_keys=True, default=_json_default)
        return hashlib.sha256(serialised.encode("utf-8")).hexdigest()
    except Exception as exc:  # pragma: no cover - hashing best effort
        log_lesson("compliance_audit_trail", f"payload hash failed: {exc}")
        return None


def _resolve_log_path() -> Path:
    override = os.getenv("COMPLIANCE_AUDIT_LOG_PATH", "").strip()
    if override:
        return Path(override)
    return Path(_DEFAULT_AUDIT_LOG)


def _summarise_registry(record: dict[str, Any] | None) -> dict[str, Any] | None:
    if not record:
        return None
    return {
        "registry": record.get("registry"),
        "identifier": record.get("identifier"),
        "status": record.get("status"),
        "jurisdiction": record.get("jurisdiction"),
    }


def _json_default(value: Any) -> str:
    return str(value)
