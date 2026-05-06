---
skill: ghost_ledger_sheets_writer
category: ghost_ledger
description: Appends validated ledger rows to Ghost Ledger Google Sheets tabs.
tier: free
inputs: none
---

# Ghost Ledger Sheets Writer

## Description
Appends validated ledger rows to Ghost Ledger Google Sheets tabs.

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
  "tool": "ghost_ledger_sheets_writer",
  "arguments": {}
}
```

## Usage
Invoke via `snowdrop_execute` with `tool_name: "ghost_ledger_sheets_writer"`.
