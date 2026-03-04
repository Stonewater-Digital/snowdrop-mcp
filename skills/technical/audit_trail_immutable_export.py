"""
Executive Summary: Export records to SHA-256-signed CSV with hash embedded as metadata for cryptographically verifiable audit trails.
Inputs: records (list of dicts), export_name (str), include_hash (bool)
Outputs: csv_content (str), sha256_hash (str), record_count (int), export_metadata (dict)
MCP Tool Name: audit_trail_immutable_export
"""
import os
import csv
import io
import json
import hashlib
import logging
from typing import Any
from datetime import datetime, timezone

logger = logging.getLogger("snowdrop.skills")

TOOL_META = {
    "name": "audit_trail_immutable_export",
    "description": "Export records to a SHA-256 signed CSV. The hash covers the entire CSV content, making tampering detectable. Hash is embedded as the final row or metadata header.",
    "inputSchema": {
        "type": "object",
        "properties": {
            "records": {
                "type": "array",
                "description": "List of record dicts to export. All dicts should share consistent keys.",
                "items": {"type": "object"}
            },
            "export_name": {
                "type": "string",
                "description": "Name for the export (used in metadata header, no extension needed)."
            },
            "include_hash": {
                "type": "boolean",
                "description": "If true, append the SHA-256 hash as a trailing metadata row (default true).",
                "default": True
            }
        },
        "required": ["records", "export_name"]
    },
    "outputSchema": {
        "type": "object",
        "properties": {
            "csv_content": {"type": "string"},
            "sha256_hash": {"type": "string"},
            "record_count": {"type": "integer"},
            "export_metadata": {"type": "object"},
            "status": {"type": "string"},
            "timestamp": {"type": "string"}
        },
        "required": ["csv_content", "sha256_hash", "record_count", "export_metadata", "status", "timestamp"]
    }
}


def _collect_fieldnames(records: list[dict]) -> list[str]:
    """Collect all unique fieldnames across records in stable insertion order.

    Args:
        records: List of record dicts.

    Returns:
        Ordered list of unique fieldnames.
    """
    seen: dict[str, None] = {}
    for record in records:
        for key in record.keys():
            seen[key] = None
    return list(seen.keys())


def _serialize_value(val: Any) -> str:
    """Serialize a field value to a CSV-safe string.

    Dicts and lists are JSON-serialized. None becomes empty string.

    Args:
        val: Any Python value.

    Returns:
        String representation safe for CSV embedding.
    """
    if val is None:
        return ""
    if isinstance(val, (dict, list)):
        return json.dumps(val, separators=(",", ":"), sort_keys=True)
    if isinstance(val, bool):
        return "true" if val else "false"
    if isinstance(val, float):
        return f"{val:.10g}"
    return str(val)


def _build_csv(records: list[dict], fieldnames: list[str]) -> str:
    """Build CSV content from records and fieldnames.

    Args:
        records: List of record dicts.
        fieldnames: Ordered column headers.

    Returns:
        CSV content string with CRLF line endings (RFC 4180 compliant).
    """
    output = io.StringIO()
    writer = csv.DictWriter(
        output,
        fieldnames=fieldnames,
        extrasaction="ignore",
        lineterminator="\r\n",
    )
    writer.writeheader()

    for record in records:
        row = {field: _serialize_value(record.get(field)) for field in fieldnames}
        writer.writerow(row)

    return output.getvalue()


def audit_trail_immutable_export(
    records: list[dict],
    export_name: str,
    include_hash: bool = True,
) -> dict:
    """Export records to a cryptographically signed CSV for immutable audit trails.

    The export process:
    1. Collect all unique field names across all records.
    2. Serialize each record to canonical CSV rows.
    3. Compute SHA-256 of the raw CSV bytes.
    4. Optionally append the hash as a trailing metadata row.

    To verify integrity later, recompute SHA-256 of the CSV content
    (excluding the hash row if appended) and compare against the stored hash.

    Args:
        records: List of record dicts to export.
        export_name: Name for the export (used in metadata).
        include_hash: If True, append SHA-256 as trailing row (default True).

    Returns:
        A dict with keys:
            - csv_content (str): The complete CSV string (with hash row if include_hash).
            - sha256_hash (str): SHA-256 hex digest of the data CSV (before hash row appended).
            - record_count (int): Number of data records exported.
            - export_metadata (dict): Export details including field names and timestamps.
            - status (str): "success" or "error".
            - timestamp (str): ISO 8601 UTC timestamp.
    """
    try:
        if not isinstance(records, list):
            raise TypeError(f"records must be a list, got {type(records).__name__}.")
        if not export_name or not export_name.strip():
            raise ValueError("export_name cannot be empty.")

        export_name = export_name.strip()
        export_ts = datetime.now(timezone.utc)
        export_ts_iso = export_ts.isoformat()

        if len(records) == 0:
            # Empty export: still valid, hash of empty CSV
            empty_csv = ""
            h = hashlib.sha256(empty_csv.encode("utf-8")).hexdigest()
            metadata = {
                "export_name": export_name,
                "exported_at": export_ts_iso,
                "record_count": 0,
                "fieldnames": [],
                "sha256_hash": h,
                "include_hash": include_hash,
                "encoding": "utf-8",
                "line_ending": "CRLF",
                "format": "RFC4180",
            }
            return {
                "status": "success",
                "csv_content": "",
                "sha256_hash": h,
                "record_count": 0,
                "export_metadata": metadata,
                "timestamp": export_ts_iso,
            }

        # Validate all records are dicts
        for idx, rec in enumerate(records):
            if not isinstance(rec, dict):
                raise TypeError(f"Record at index {idx} must be a dict, got {type(rec).__name__}.")

        fieldnames = _collect_fieldnames(records)

        # Build the data CSV (without hash row)
        data_csv = _build_csv(records, fieldnames)

        # Compute SHA-256 over the raw data CSV bytes (utf-8)
        data_bytes = data_csv.encode("utf-8")
        sha256_hash = hashlib.sha256(data_bytes).hexdigest()

        # Append hash as trailing metadata row if requested
        final_csv = data_csv
        if include_hash:
            hash_row_fields = {f: "" for f in fieldnames}
            # Use the first field (or a dedicated key) to store the hash metadata
            hash_label = "#AUDIT_HASH"
            hash_value = f"SHA-256:{sha256_hash}"
            timestamp_label = export_ts_iso

            # Build trailing comment row
            hash_line = f"{hash_label},{hash_value},{timestamp_label},{export_name}\r\n"
            final_csv = data_csv + hash_line

        export_metadata = {
            "export_name": export_name,
            "exported_at": export_ts_iso,
            "record_count": len(records),
            "fieldnames": fieldnames,
            "field_count": len(fieldnames),
            "sha256_hash": sha256_hash,
            "include_hash": include_hash,
            "hash_row_appended": include_hash,
            "encoding": "utf-8",
            "line_ending": "CRLF",
            "format": "RFC4180",
            "data_csv_bytes": len(data_bytes),
            "verification_instructions": (
                "To verify: recompute SHA-256 of the CSV content excluding the final #AUDIT_HASH row "
                "and compare against the stored hash value."
            ),
        }

        return {
            "status": "success",
            "csv_content": final_csv,
            "sha256_hash": sha256_hash,
            "record_count": len(records),
            "export_metadata": export_metadata,
            "timestamp": export_ts_iso,
        }

    except Exception as e:
        logger.error(f"audit_trail_immutable_export failed: {e}")
        _log_lesson(f"audit_trail_immutable_export: {e}")
        return {
            "status": "error",
            "error": str(e),
            "csv_content": "",
            "sha256_hash": "",
            "record_count": 0,
            "export_metadata": {},
            "timestamp": datetime.now(timezone.utc).isoformat(),
        }


def _log_lesson(message: str) -> None:
    """Append an error lesson to the lessons log file.

    Args:
        message: The lesson message to record.
    """
    try:
        with open("logs/lessons.md", "a") as f:
            f.write(f"- [{datetime.now(timezone.utc).isoformat()}] {message}\n")
    except OSError:
        logger.warning("Could not write to logs/lessons.md")
