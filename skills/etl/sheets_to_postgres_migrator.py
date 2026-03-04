"""Plan migration from Google Sheets to PostgreSQL."""
from __future__ import annotations

from datetime import datetime, timezone
from typing import Any

TOOL_META: dict[str, Any] = {
    "name": "sheets_to_postgres_migrator",
    "description": "Produces SQL/ETL plan for moving Ghost Ledger tabs into PostgreSQL tables.",
    "inputSchema": {
        "type": "object",
        "properties": {
            "sheet_tabs": {"type": "array", "items": {"type": "string"}},
            "row_counts": {"type": "object"},
            "column_schemas": {"type": "object"},
        },
        "required": ["sheet_tabs", "row_counts", "column_schemas"],
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


def sheets_to_postgres_migrator(
    sheet_tabs: list[str],
    row_counts: dict[str, int],
    column_schemas: dict[str, list[dict[str, Any]]],
    **_: Any,
) -> dict[str, Any]:
    """Return migration SQL, row estimates, and pending approval notice."""
    try:
        statements: list[str] = []
        estimated_rows = 0
        for tab in sheet_tabs:
            columns = column_schemas.get(tab, [])
            col_defs = []
            for column in columns:
                name = column.get("name")
                col_type = column.get("type", "TEXT").upper()
                col_defs.append(f'"{name}" {col_type}')
            create_stmt = f'CREATE TABLE IF NOT EXISTS "{tab.lower()}" (id SERIAL PRIMARY KEY, {", ".join(col_defs)});'
            statements.append(create_stmt)
            estimated_rows += int(row_counts.get(tab, 0))
        plan = {
            "sql_statements": statements,
            "estimated_rows": estimated_rows,
            "insert_strategy": "COPY FROM staging CSV with batches of 5k rows",
            "validation_queries": [
                "SELECT COUNT(*) FROM {table};",
                "SELECT checksum FROM hash_agg ORDER BY checksum;",
            ],
            "execution": "pending_thunder_approval",
        }
        return {
            "status": "success",
            "data": plan,
            "timestamp": datetime.now(timezone.utc).isoformat(),
        }
    except Exception as exc:
        _log_lesson("sheets_to_postgres_migrator", str(exc))
        return {
            "status": "error",
            "data": {"error": str(exc)},
            "timestamp": datetime.now(timezone.utc).isoformat(),
        }


def _log_lesson(skill_name: str, error: str) -> None:
    with open("logs/lessons.md", "a", encoding="utf-8") as handle:
        handle.write(f"- [{datetime.now(timezone.utc).isoformat()}] {skill_name}: {error}\n")
