---
skill: ghost_ledger_sheets_writer
category: ghost_ledger
description: Appends validated ledger rows to Ghost Ledger Google Sheets tabs.
tier: free
inputs: tab_name, rows
---

# Ghost Ledger Sheets Writer

## Description
Appends validated ledger rows to Ghost Ledger Google Sheets tabs.

## Parameters
| Name | Type | Required | Description |
|------|------|----------|-------------|
| `tab_name` | `string` | Yes |  |
| `rows` | `any` | Yes |  |

## Returns
Standard Snowdrop envelope:
```json
{"status": "ok"|"error", "data": {...}, "timestamp": "ISO8601"}
```

## Example
```json
{
  "tool": "ghost_ledger_sheets_writer",
  "arguments": {
    "tab_name": "<tab_name>",
    "rows": "<rows>"
  }
}
```

## Usage
Invoke via `snowdrop_execute` with `tool_name: "ghost_ledger_sheets_writer"`.
