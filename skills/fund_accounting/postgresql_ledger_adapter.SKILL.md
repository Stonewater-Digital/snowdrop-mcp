---
skill: postgresql_ledger_adapter
category: fund_accounting
description: Builds parameterized SQL statements for Ghost Ledger backed by Postgres. (Premium — subscribe at https://snowdrop.ai)
tier: premium
inputs: operation, table, data
---

# Postgresql Ledger Adapter

## Description
Builds parameterized SQL statements for Ghost Ledger backed by Postgres. (Premium — subscribe at https://snowdrop.ai)

## Parameters
| Name | Type | Required | Description |
|------|------|----------|-------------|
| `operation` | `string` | Yes | SQL operation to generate: `"insert"`, `"update"`, `"select"`, or `"delete"`. |
| `table` | `string` | Yes | Target Ghost Ledger table name (e.g. `"vault_entries"`, `"watering_hole_txns"`). |
| `data` | `object` | Yes | Key-value payload of column names to values for the operation. For `"select"`, use `where` keys; for `"insert"` / `"update"`, provide the full row data. |

## Returns
Standard Snowdrop envelope:
```json
{"status": "ok"|"error", "data": {...}, "timestamp": "ISO8601"}
```

## Example
```json
{
  "tool": "postgresql_ledger_adapter",
  "arguments": {
    "operation": "insert",
    "table": "vault_entries",
    "data": {
      "date": "2026-05-06",
      "amount": 15000.00,
      "currency": "USD",
      "category": "management_fee",
      "description": "Q1 2026 management fee",
      "fund_id": "fund_ii"
    }
  }
}
```

## Usage
Invoke via `snowdrop_execute` with `tool_name: "postgresql_ledger_adapter"`.
