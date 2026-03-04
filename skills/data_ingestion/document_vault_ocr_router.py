"""
Executive Summary: Routes vault documents to the correct OCR model batches while respecting capacity and priority rules.

Inputs: documents (list[dict]), ocr_profiles (dict[str, str], optional), max_batch (int, optional)
Outputs: status (str), data (routes/skipped/summary), timestamp (str)
MCP Tool Name: document_vault_ocr_router
"""
from __future__ import annotations

from typing import Any

from skills.utils import (
    SkillTelemetryEmitter,
    get_iso_timestamp,
    logger,
    log_lesson as _shared_log_lesson,
)

DEFAULT_MODEL = "ocr_v3"

TOOL_META: dict[str, Any] = {
    "name": "document_vault_ocr_router",
    "description": "Assign vault documents to OCR models based on mime type, priority, and presence of embedded text.",
    "inputSchema": {
        "type": "object",
        "properties": {
            "documents": {
                "type": "array",
                "items": {"type": "object"},
                "description": "Documents with doc_id, mime_type, page_count, priority, contains_text, source.",
            },
            "ocr_profiles": {
                "type": "object",
                "description": "Optional mime_type -> model overrides.",
            },
            "max_batch": {
                "type": "integer",
                "default": 25,
                "description": "Maximum number of documents to route in this call.",
            },
        },
        "required": ["documents"],
    },
    "outputSchema": {
        "type": "object",
        "properties": {
            "status": {"type": "string", "enum": ["ok", "error"]},
            "data": {
                "type": "object",
                "properties": {
                    "routes": {"type": "array", "items": {"type": "object"}},
                    "skipped": {"type": "array", "items": {"type": "object"}},
                    "summary": {"type": "object"},
                },
            },
            "timestamp": {"type": "string", "format": "date-time"},
        },
        "required": ["status", "timestamp"],
    },
}


def document_vault_ocr_router(
    documents: list[dict[str, Any]],
    ocr_profiles: dict[str, str] | None = None,
    max_batch: int = 25,
) -> dict[str, Any]:
    """Route documents to OCR models/batches.

    Args:
        documents: Document metadata entries.
        ocr_profiles: Mime-type specific OCR model overrides.
        max_batch: Maximum documents to include in the routed batch.

    Returns:
        Snowdrop response dict containing route decisions and summary metrics.

    Raises:
        ValueError: If documents input is invalid.
    """
    emitter = SkillTelemetryEmitter(
        "document_vault_ocr_router",
        {"documents": len(documents or []), "max_batch": max_batch},
    )
    try:
        if not isinstance(documents, list):
            raise ValueError("documents must be a list of dicts")
        if max_batch <= 0:
            raise ValueError("max_batch must be positive")

        profiles = {k.lower(): v for k, v in (ocr_profiles or {}).items()}
        routes: list[dict[str, Any]] = []
        skipped: list[dict[str, Any]] = []

        for payload in documents:
            if not isinstance(payload, dict):
                continue
            doc_id = payload.get("doc_id")
            mime_type = str(payload.get("mime_type", "")).lower()
            priority = str(payload.get("priority", "low")).lower()
            contains_text = bool(payload.get("contains_text"))
            page_count = max(int(payload.get("page_count") or 0), 0)

            if contains_text and priority == "low":
                skipped.append({"doc_id": doc_id, "reason": "already_has_text"})
                continue

            model = profiles.get(mime_type, DEFAULT_MODEL)
            reason = _route_reason(priority, contains_text, mime_type, page_count)
            routes.append(
                {
                    "doc_id": doc_id,
                    "model": model,
                    "priority": priority,
                    "reason": reason,
                    "page_count": page_count,
                }
            )
            if len(routes) >= max_batch:
                break

        summary = {
            "requested": len(documents),
            "routed": len(routes),
            "skipped": len(skipped),
        }
        emitter.record("ok", summary)
        data = {"routes": routes, "skipped": skipped, "summary": summary}
        return {"status": "ok", "data": data, "timestamp": get_iso_timestamp()}
    except Exception as exc:  # noqa: BLE001
        logger.error(f"document_vault_ocr_router failed: {exc}")
        _log_lesson("document_vault_ocr_router", str(exc))
        emitter.record("error", {"error": str(exc)})
        return {"status": "error", "data": {"error": str(exc)}, "timestamp": get_iso_timestamp()}


def _route_reason(priority: str, contains_text: bool, mime_type: str, page_count: int) -> str:
    """Return reason string for routing decision."""
    if priority == "high":
        return "high_priority_doc"
    if mime_type.startswith("image/"):
        return "image_requires_full_ocr"
    if page_count > 5:
        return "large_document_batch"
    if not contains_text:
        return "missing_text_layer"
    return "standard_processing"


def _log_lesson(skill_name: str, error: str) -> None:
    """Proxy shared logger."""
    _shared_log_lesson(skill_name, error)
