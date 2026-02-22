"""Prepare parameterized SQL for Ghost Ledger v2 interactions."""
from __future__ import annotations

import os
import re
from datetime import datetime, timezone
from typing import Any

TABLE_PATTERN = re.compile(r"^[a-zA-Z0-9_]+$")

TOOL_META: dict[str, Any] = {
    "name": "postgresql_ledger_adapter",
    "description": "Builds parameterized SQL statements for Ghost Ledger backed by Postgres.",
    "inputSchema": {
        "type": "object",
        "properties": {
            "operation": {
                "type": "string",
                "enum": ["read", "write", "reconcile"],
                "description": "SQL action to perform.",
            },
            "table": {"type": "string", "description": "Target table name."},
            "data": {
                "type": "object",
                "description": "Operation-specific payload (values, filters, window).",
            },
        },
        "required": ["operation", "table", "data"],
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


def postgresql_ledger_adapter(operation: str, table: str, data: dict[str, Any], **_: Any) -> dict[str, Any]:
    """Return a SQL statement plus parameters for Ghost Ledger operations.

    Args:
        operation: Database action to perform (read/write/reconcile).
        table: Target Postgres table to interact with.
        data: Operation-specific payload such as filters or values.

    Returns:
        Envelope containing the SQL statement and ordered parameter list.
    """

    try:
        if not os.getenv("DATABASE_URL"):
            raise ValueError("DATABASE_URL missing; see .env.template")

        if not TABLE_PATTERN.match(table):
            raise ValueError("Table names may only contain alphanumerics and underscores")

        operation = operation.lower()
        if operation == "read":
            query, params = _build_read(table, data)
        elif operation == "write":
            query, params = _build_write(table, data)
        elif operation == "reconcile":
            query, params = _build_reconcile(table, data)
        else:
            raise ValueError("Unsupported operation")

        return {
            "status": "success",
            "data": {
                "query": query,
                "params": params,
                "operation": operation,
            },
            "timestamp": datetime.now(timezone.utc).isoformat(),
        }
    except Exception as exc:
        _log_lesson("postgresql_ledger_adapter", str(exc))
        return {
            "status": "error",
            "data": {"error": str(exc)},
            "timestamp": datetime.now(timezone.utc).isoformat(),
        }


def _build_read(table: str, data: dict[str, Any]) -> tuple[str, list[Any]]:
    filters = data.get("filters", {})
    limit = data.get("limit")
    where_clauses = []
    params: list[Any] = []
    for column, value in filters.items():
        if not TABLE_PATTERN.match(column):
            raise ValueError("Invalid column in filters")
        where_clauses.append(f"{column} = %s")
        params.append(value)

    where_sql = f" WHERE {' AND '.join(where_clauses)}" if where_clauses else ""
    limit_sql = ""
    if limit:
        limit_sql = " LIMIT %s"
        params.append(int(limit))

    query = f"SELECT * FROM {table}{where_sql} ORDER BY timestamp DESC{limit_sql};"
    return query, params


def _build_write(table: str, data: dict[str, Any]) -> tuple[str, list[Any]]:
    values = data.get("values")
    if not isinstance(values, dict) or not values:
        raise ValueError("values dict is required for write operations")

    columns = []
    placeholders = []
    params: list[Any] = []

    for column, value in values.items():
        if not TABLE_PATTERN.match(column):
            raise ValueError("Invalid column name in values")
        columns.append(column)
        placeholders.append("%s")
        params.append(value)

    cols_sql = ", ".join(columns)
    placeholder_sql = ", ".join(placeholders)
    query = f"INSERT INTO {table} ({cols_sql}) VALUES ({placeholder_sql}) RETURNING *;"
    return query, params


def _build_reconcile(table: str, data: dict[str, Any]) -> tuple[str, list[Any]]:
    start = data.get("start_ts")
    end = data.get("end_ts")
    if not start or not end:
        raise ValueError("start_ts and end_ts are required for reconcile")

    target_account = data.get("account_id")
    params: list[Any] = [start, end]
    where_sql = "timestamp BETWEEN %s AND %s"
    if target_account:
        where_sql += " AND account_id = %s"
        params.append(target_account)

    query = (
        f"SELECT account_id, SUM(amount) AS delta, COUNT(*) AS txn_count"
        f" FROM {table} WHERE {where_sql} GROUP BY account_id;"
    )
    return query, params


def _log_lesson(skill_name: str, error: str) -> None:
    with open("logs/lessons.md", "a", encoding="utf-8") as handle:
        handle.write(f"- [{datetime.now(timezone.utc).isoformat()}] {skill_name}: {error}\n")
