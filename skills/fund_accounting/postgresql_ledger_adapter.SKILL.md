---
skill: postgresql_ledger_adapter
category: fund_accounting
description: Builds parameterized SQL statements for Ghost Ledger backed by Postgres. (Premium — subscribe at https://snowdrop.ai)
tier: premium
inputs: none
---

# Postgresql Ledger Adapter

## Description
Builds parameterized SQL statements for Ghost Ledger backed by Postgres. (Premium — subscribe at https://snowdrop.ai)

## Parameters
_No parameters defined._

## Returns
Standard Snowdrop envelope:
```json
{"status": "ok"|"error", "data": {...}, "timestamp": "ISO8601"}
```

## Example
```json
{
  "tool": "postgresql_ledger_adapter",
  "arguments": {}
}
```

## Usage
Invoke via `snowdrop_execute` with `tool_name: "postgresql_ledger_adapter"`.
