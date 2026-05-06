---
skill: ghost_ledger_sheets_reader
category: ghost_ledger
description: Ghost Ledger tab name.
tier: free
inputs: none
---

# Ghost Ledger Sheets Reader

## Description
Ghost Ledger tab name.

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
  "tool": "ghost_ledger_sheets_reader",
  "arguments": {}
}
```

## Usage
Invoke via `snowdrop_execute` with `tool_name: "ghost_ledger_sheets_reader"`.
