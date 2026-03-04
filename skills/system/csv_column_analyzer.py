"""Analyze columns of CSV-like row data for types, nulls, and statistics.

MCP Tool Name: csv_column_analyzer
"""
from __future__ import annotations
from datetime import datetime, timezone
from typing import Any

TOOL_META: dict[str, Any] = {
    "name": "csv_column_analyzer",
    "description": "Analyze CSV-like tabular data (list of rows). For each column: infer type, count nulls, count unique values, compute min/max for numbers, and show sample values.",
    "inputSchema": {
        "type": "object",
        "properties": {
            "rows": {
                "type": "array",
                "items": {
                    "type": "array",
                    "description": "A single row represented as a list of values.",
                },
                "description": "List of rows, where each row is a list of cell values.",
            },
            "has_header": {
                "type": "boolean",
                "description": "Whether the first row is a header row.",
                "default": True,
            },
        },
        "required": ["rows"],
    },
}


def _infer_type(values: list[Any]) -> str:
    """Infer the predominant type of a column."""
    type_counts: dict[str, int] = {"number": 0, "string": 0, "boolean": 0, "null": 0}
    for v in values:
        if v is None or v == "" or v == "null" or v == "None":
            type_counts["null"] += 1
        elif isinstance(v, bool):
            type_counts["boolean"] += 1
        elif isinstance(v, (int, float)):
            type_counts["number"] += 1
        elif isinstance(v, str):
            # Try to parse as number
            try:
                float(v)
                type_counts["number"] += 1
            except (ValueError, TypeError):
                if v.lower() in ("true", "false"):
                    type_counts["boolean"] += 1
                else:
                    type_counts["string"] += 1
        else:
            type_counts["string"] += 1

    # Return most common non-null type
    non_null = {k: v for k, v in type_counts.items() if k != "null"}
    if not any(non_null.values()):
        return "null"
    return max(non_null, key=lambda k: non_null[k])


def _to_number(v: Any) -> float | None:
    """Try to convert a value to a number."""
    if v is None or v == "" or v == "null" or v == "None":
        return None
    try:
        return float(v)
    except (ValueError, TypeError):
        return None


def csv_column_analyzer(
    rows: list[list[Any]],
    has_header: bool = True,
) -> dict[str, Any]:
    """Analyze CSV column data."""
    try:
        if not rows:
            return {
                "status": "error",
                "data": {"error": "rows must not be empty."},
                "timestamp": datetime.now(timezone.utc).isoformat(),
            }

        if has_header:
            headers = [str(h) for h in rows[0]]
            data_rows = rows[1:]
        else:
            num_cols = len(rows[0])
            headers = [f"column_{i}" for i in range(num_cols)]
            data_rows = rows

        if not data_rows:
            return {
                "status": "error",
                "data": {"error": "No data rows found."},
                "timestamp": datetime.now(timezone.utc).isoformat(),
            }

        num_cols = len(headers)
        columns: list[dict[str, Any]] = []

        for col_idx in range(num_cols):
            col_values = []
            for row in data_rows:
                if col_idx < len(row):
                    col_values.append(row[col_idx])
                else:
                    col_values.append(None)

            col_name = headers[col_idx] if col_idx < len(headers) else f"column_{col_idx}"
            inferred_type = _infer_type(col_values)

            null_count = sum(
                1 for v in col_values
                if v is None or v == "" or v == "null" or v == "None"
            )
            non_null = [v for v in col_values if v is not None and v != "" and v != "null" and v != "None"]
            unique_count = len(set(str(v) for v in non_null))

            col_info: dict[str, Any] = {
                "name": col_name,
                "inferred_type": inferred_type,
                "total_values": len(col_values),
                "null_count": null_count,
                "non_null_count": len(non_null),
                "unique_count": unique_count,
            }

            # Numeric stats
            if inferred_type == "number":
                nums = [n for n in (_to_number(v) for v in col_values) if n is not None]
                if nums:
                    col_info["min"] = round(min(nums), 4)
                    col_info["max"] = round(max(nums), 4)
                    col_info["mean"] = round(sum(nums) / len(nums), 4)

            # Sample values (up to 5)
            samples = non_null[:5]
            col_info["sample_values"] = samples

            columns.append(col_info)

        return {
            "status": "ok",
            "data": {
                "num_rows": len(data_rows),
                "num_columns": num_cols,
                "has_header": has_header,
                "columns": columns,
            },
            "timestamp": datetime.now(timezone.utc).isoformat(),
        }
    except Exception as exc:
        return {
            "status": "error",
            "data": {"error": str(exc)},
            "timestamp": datetime.now(timezone.utc).isoformat(),
        }
