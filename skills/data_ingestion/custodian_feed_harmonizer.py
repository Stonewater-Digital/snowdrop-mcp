"""
Executive Summary: Harmonizes heterogeneous custodian statement rows into a canonical schema for downstream reconciliations.

Inputs: records (list[dict]), field_mappings (dict[str, dict[str, str]]), default_currency (str, optional)
Outputs: status (str), data (dict with harmonized_records/unmapped_records/summary/warnings), timestamp (str)
MCP Tool Name: custodian_feed_harmonizer
"""
from __future__ import annotations

from typing import Any

from skills.utils import (
    SkillTelemetryEmitter,
    get_iso_timestamp,
    logger,
    log_lesson as _shared_log_lesson,
)

TOOL_META: dict[str, Any] = {
    "name": "custodian_feed_harmonizer",
    "description": "Normalize custodian statement payloads into a canonical schema with validation flags.",
    "inputSchema": {
        "type": "object",
        "properties": {
            "records": {
                "type": "array",
                "items": {"type": "object"},
                "description": "Raw custodian rows that include at least a 'source' key.",
            },
            "field_mappings": {
                "type": "object",
                "additionalProperties": {"type": "object"},
                "description": "Mapping per source -> canonical field map (e.g., {'custody_bank': {'account_id': 'acct'}}).",
            },
            "default_currency": {
                "type": "string",
                "default": "USD",
                "description": "Currency to backfill when a record omits the field.",
            },
        },
        "required": ["records", "field_mappings"],
    },
    "outputSchema": {
        "type": "object",
        "properties": {
            "status": {"type": "string", "enum": ["ok", "error"]},
            "data": {
                "type": "object",
                "properties": {
                    "harmonized_records": {"type": "array", "items": {"type": "object"}},
                    "unmapped_records": {"type": "array", "items": {"type": "object"}},
                    "warnings": {"type": "array", "items": {"type": "string"}},
                    "summary": {"type": "object"},
                },
            },
            "timestamp": {"type": "string", "format": "date-time"},
        },
        "required": ["status", "timestamp"],
    },
}

_NUMERIC_FIELDS = {"quantity", "market_value"}


def custodian_feed_harmonizer(
    records: list[dict[str, Any]],
    field_mappings: dict[str, dict[str, str]],
    default_currency: str = "USD",
) -> dict[str, Any]:
    """Normalize custodian statement rows using the provided field map.

    Args:
        records: Raw custodian payloads that minimally contain a `source` identifier.
        field_mappings: Per-source canonical mapping (canonical field -> raw field name).
        default_currency: Currency code used when an incoming row omits currency.

    Returns:
        Snowdrop skill response dict with normalization results and warnings.

    Raises:
        ValueError: If inputs are not in the expected structure.
    """
    emitter = SkillTelemetryEmitter(
        "custodian_feed_harmonizer",
        {"total_rows": len(records or []), "sources": len(field_mappings or {})},
    )
    try:
        if not isinstance(records, list):
            raise ValueError("records must be a list of dicts")
        if not isinstance(field_mappings, dict):
            raise ValueError("field_mappings must be a dict keyed by source")

        harmonized: list[dict[str, Any]] = []
        unmapped: list[dict[str, Any]] = []
        warnings: list[str] = []

        for idx, record in enumerate(records):
            if not isinstance(record, dict):
                warnings.append(f"Row {idx} ignored: not a dict")
                continue

            source = str(record.get("source", "unknown")).lower()
            mapping = field_mappings.get(source)
            if mapping is None:
                unmapped.append({"source": source, "record_id": record.get("id"), "reason": "missing_mapping"})
                continue

            canonical_row, row_warnings = _normalize_row(record, mapping, default_currency)
            canonical_row["source"] = source
            harmonized.append(canonical_row)
            warnings.extend(row_warnings)

        response = {
            "harmonized_records": harmonized,
            "unmapped_records": unmapped,
            "warnings": warnings,
            "summary": {
                "total_rows": len(records),
                "harmonized_rows": len(harmonized),
                "unmapped_rows": len(unmapped),
            },
        }
        emitter.record(
            "ok",
            {
                "harmonized_rows": len(harmonized),
                "unmapped_rows": len(unmapped),
                "warnings": len(warnings),
            },
        )
        return {
            "status": "ok",
            "data": response,
            "timestamp": get_iso_timestamp(),
        }
    except Exception as exc:
        msg = f"custodian_feed_harmonizer failed: {exc}"
        logger.error(msg)
        _log_lesson("custodian_feed_harmonizer", str(exc))
        emitter.record("error", {"error": str(exc)})
        return {
            "status": "error",
            "data": {"error": str(exc)},
            "timestamp": get_iso_timestamp(),
        }


def _normalize_row(
    record: dict[str, Any],
    mapping: dict[str, str],
    default_currency: str,
) -> tuple[dict[str, Any], list[str]]:
    """Transform one record into the canonical schema.

    Args:
        record: Raw custodian row.
        mapping: Canonical field to raw field mapping.
        default_currency: Currency fallback when not provided.

    Returns:
        Tuple of (normalized record, warnings generated during normalization).
    """
    canonical: dict[str, Any] = {}
    warnings: list[str] = []

    for field in ("account_id", "instrument_id", "quantity", "market_value", "currency", "as_of"):
        raw_key = mapping.get(field, field)
        value = record.get(raw_key)

        if value is None and field == "currency":
            value = default_currency
        elif value is None and field == "as_of":
            fallback = record.get("as_of") or record.get("timestamp")
            value = fallback

        if field in _NUMERIC_FIELDS and value is not None:
            value = _to_float(value)
            if value is None:
                warnings.append(f"{record.get('id', 'unknown')} -> invalid {field} value")

        canonical[field] = value
        if value is None:
            warnings.append(f"{record.get('id', 'unknown')} -> missing {field}")

    canonical["metadata"] = {
        "raw_record_id": record.get(mapping.get("record_id", "record_id")),
        "position_status": record.get(mapping.get("status", "status")),
    }
    return canonical, warnings


def _to_float(value: Any) -> float | None:
    """Convert value to float when possible."""
    try:
        return float(value)
    except (TypeError, ValueError):
        return None


def _log_lesson(skill_name: str, error: str) -> None:
    """Proxy to shared lesson logger for consistent formatting."""
    _shared_log_lesson(skill_name, error)
