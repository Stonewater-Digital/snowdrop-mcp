"""Export structured data to CSV string."""
from __future__ import annotations

import csv
import io
from datetime import datetime, timezone
from typing import Any

TOOL_META: dict[str, Any] = {
    "name": "csv_exporter",
    "description": "Flattens dict rows and emits RFC4180-compliant CSV strings.",
    "inputSchema": {
        "type": "object",
        "properties": {
            "data": {"type": "array", "items": {"type": "object"}},
            "columns": {"type": ["array", "null"], "items": {"type": "string"}},
            "filename_prefix": {"type": "string"},
        },
        "required": ["data", "filename_prefix"],
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


def csv_exporter(
    data: list[dict[str, Any]],
    filename_prefix: str,
    columns: list[str] | None = None,
    **_: Any,
) -> dict[str, Any]:
    """Return CSV content, filename suggestion, and metadata."""
    try:
        if not data:
            raise ValueError("data cannot be empty")

        flattened = [_flatten_dict(row) for row in data]
        column_list = columns or sorted({key for row in flattened for key in row.keys()})
        buffer = io.StringIO()
        writer = csv.DictWriter(buffer, fieldnames=column_list)
        writer.writeheader()
        for row in flattened:
            writer.writerow({col: row.get(col, "") for col in column_list})

        timestamp_str = datetime.now(timezone.utc).strftime("%Y%m%dT%H%M%SZ")
        filename = f"{filename_prefix}_{timestamp_str}.csv"
        data_payload = {
            "csv_content": buffer.getvalue(),
            "suggested_filename": filename,
            "row_count": len(flattened),
            "columns": column_list,
        }
        return {
            "status": "success",
            "data": data_payload,
            "timestamp": datetime.now(timezone.utc).isoformat(),
        }
    except Exception as exc:
        _log_lesson("csv_exporter", str(exc))
        return {
            "status": "error",
            "data": {"error": str(exc)},
            "timestamp": datetime.now(timezone.utc).isoformat(),
        }


def _flatten_dict(payload: dict[str, Any], parent_key: str = "") -> dict[str, Any]:
    flattened: dict[str, Any] = {}
    for key, value in payload.items():
        compound_key = f"{parent_key}.{key}" if parent_key else key
        if isinstance(value, dict):
            flattened.update(_flatten_dict(value, compound_key))
        else:
            flattened[compound_key] = value
    return flattened


def _log_lesson(skill_name: str, error: str) -> None:
    with open("logs/lessons.md", "a", encoding="utf-8") as handle:
        handle.write(f"- [{datetime.now(timezone.utc).isoformat()}] {skill_name}: {error}\n")
