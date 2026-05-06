---
skill: sheets_to_postgres_migrator
category: etl
description: Produces SQL/ETL plan for moving Ghost Ledger tabs into PostgreSQL tables.
tier: free
inputs: sheet_tabs, row_counts, column_schemas
---

# Sheets To Postgres Migrator

## Description
Produces SQL/ETL plan for moving Ghost Ledger tabs into PostgreSQL tables.

## Parameters
| Name | Type | Required | Description |
|------|------|----------|-------------|
| `sheet_tabs` | `array` | Yes |  |
| `row_counts` | `object` | Yes |  |
| `column_schemas` | `object` | Yes |  |

## Returns
Standard Snowdrop envelope:
```json
{"status": "ok"|"error", "data": {...}, "timestamp": "ISO8601"}
```

## Example
```json
{
  "tool": "sheets_to_postgres_migrator",
  "arguments": {
    "sheet_tabs": [],
    "row_counts": {},
    "column_schemas": {}
  }
}
```

## Usage
Invoke via `snowdrop_execute` with `tool_name: "sheets_to_postgres_migrator"`.
