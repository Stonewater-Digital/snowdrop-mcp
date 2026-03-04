"""
Executive Summary: Normalizes administrator API/SFTP payloads, checks freshness, and surfaces validation gaps before downstream posting.

Inputs: responses (list[dict]), required_fields (list[str]), max_age_minutes (int, optional)
Outputs: status (str), data (normalized_payloads/issues/summary), timestamp (str)
MCP Tool Name: administrator_api_bridge
"""
from __future__ import annotations

from datetime import datetime, timedelta, timezone
from typing import Any

from skills.utils import (
    SkillTelemetryEmitter,
    get_iso_timestamp,
    logger,
    log_lesson as _shared_log_lesson,
)

TOOL_META: dict[str, Any] = {
    "name": "administrator_api_bridge",
    "description": "Bridge skill that validates administrator feeds and emits normalized payload summaries.",
    "inputSchema": {
        "type": "object",
        "properties": {
            "responses": {
                "type": "array",
                "items": {"type": "object"},
                "description": "Admin payloads with keys: source, endpoint, received_at, records[].",
            },
            "required_fields": {
                "type": "array",
                "items": {"type": "string"},
                "description": "Fields that must exist in each record for downstream posting.",
            },
            "max_age_minutes": {
                "type": "integer",
                "default": 15,
                "description": "Maximum acceptable payload age before marking as stale.",
            },
        },
        "required": ["responses", "required_fields"],
    },
    "outputSchema": {
        "type": "object",
        "properties": {
            "status": {"type": "string", "enum": ["ok", "error"]},
            "data": {
                "type": "object",
                "properties": {
                    "normalized_payloads": {"type": "array", "items": {"type": "object"}},
                    "issues": {"type": "object"},
                    "summary": {"type": "object"},
                },
            },
            "timestamp": {"type": "string", "format": "date-time"},
        },
        "required": ["status", "timestamp"],
    },
}


def administrator_api_bridge(
    responses: list[dict[str, Any]],
    required_fields: list[str],
    max_age_minutes: int = 15,
) -> dict[str, Any]:
    """Validate and normalize administrator feeds.

    Args:
        responses: Raw payloads returned by administrator APIs/SFTP.
        required_fields: Fields each record must contain for GL/NAV ingestion.
        max_age_minutes: Time window before a payload is treated as stale.

    Returns:
        Snowdrop response dict with normalized payloads, issues, and summary stats.

    Raises:
        ValueError: If inputs fail structural validation.
    """
    payload_count = len(responses) if isinstance(responses, list) else 0
    emitter = SkillTelemetryEmitter(
        "administrator_api_bridge",
        {"payloads": payload_count, "required_fields": len(required_fields or [])},
    )
    try:
        if not isinstance(responses, list):
            raise ValueError("responses must be a list of payload objects")
        if not isinstance(required_fields, list):
            raise ValueError("required_fields must be a list of field names")
        if max_age_minutes <= 0:
            raise ValueError("max_age_minutes must be positive")

        normalized: list[dict[str, Any]] = []
        stale_sources: list[str] = []
        missing_fields: list[dict[str, Any]] = []
        empty_payloads: list[str] = []

        now = datetime.now(timezone.utc)
        freshness_limit = now - timedelta(minutes=max_age_minutes)

        for payload in responses:
            if not isinstance(payload, dict):
                continue
            source = str(payload.get("source", "unknown")).lower()
            received_at = _parse_timestamp(payload.get("received_at"))
            if received_at and received_at < freshness_limit:
                stale_sources.append(source)
            elif received_at is None:
                missing_fields.append({"source": source, "record_id": None, "missing": ["received_at"]})

            records = payload.get("records", [])
            if not records:
                empty_payloads.append(source)

            sanitized_records = _sanitize_records(records, required_fields, source, missing_fields)
            normalized.append(
                {
                    "source": source,
                    "endpoint": payload.get("endpoint"),
                    "received_at": received_at.isoformat() if received_at else None,
                    "record_count": len(sanitized_records),
                    "records": sanitized_records,
                }
            )

        data = {
            "normalized_payloads": normalized,
            "issues": {
                "stale_sources": sorted(set(stale_sources)),
                "missing_fields": missing_fields,
                "empty_payloads": sorted(set(empty_payloads)),
            },
            "summary": {
                "payloads": len(responses),
                "normalized": len(normalized),
                "total_records": sum(item["record_count"] for item in normalized),
            },
        }
        emitter.record(
            "ok",
            {
                "normalized": len(normalized),
                "stale_sources": len(set(stale_sources)),
                "missing_fields": len(missing_fields),
            },
        )
        return {"status": "ok", "data": data, "timestamp": get_iso_timestamp()}
    except Exception as exc:
        msg = f"administrator_api_bridge failed: {exc}"
        logger.error(msg)
        _log_lesson("administrator_api_bridge", str(exc))
        emitter.record("error", {"error": str(exc)})
        return {
            "status": "error",
            "data": {"error": str(exc)},
            "timestamp": get_iso_timestamp(),
        }


def _sanitize_records(
    records: list[dict[str, Any]],
    required_fields: list[str],
    source: str,
    missing_fields: list[dict[str, Any]],
) -> list[dict[str, Any]]:
    """Keep only required fields and capture missing field issues."""
    sanitized: list[dict[str, Any]] = []
    for idx, record in enumerate(records or []):
        if not isinstance(record, dict):
            continue
        sanitized_record = {
            field: record.get(field) for field in required_fields
        }
        record_id = record.get("id") or record.get("record_id") or f"{source}-{idx}"
        sanitized_record["record_id"] = record_id
        sanitized_record["source"] = source

        missing = [field for field, value in sanitized_record.items() if field in required_fields and value is None]
        if missing:
            missing_fields.append({"source": source, "record_id": record_id, "missing": missing})
        sanitized.append(sanitized_record)
    return sanitized


def _parse_timestamp(raw_value: Any) -> datetime | None:
    """Parse ISO8601 timestamps while tolerating missing timezone."""
    if raw_value is None:
        return None
    try:
        value = str(raw_value).replace("Z", "+00:00")
        ts = datetime.fromisoformat(value)
        if ts.tzinfo is None:
            ts = ts.replace(tzinfo=timezone.utc)
        return ts.astimezone(timezone.utc)
    except (ValueError, TypeError):
        return None


def _log_lesson(skill_name: str, error: str) -> None:
    """Proxy to shared lesson logger for consistent formatting."""
    _shared_log_lesson(skill_name, error)
