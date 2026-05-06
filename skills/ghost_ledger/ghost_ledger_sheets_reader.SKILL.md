---
skill: ghost_ledger_sheets_reader
category: ghost_ledger
description: Ghost Ledger tab name.
tier: free
inputs: ab_name, date_range_start, date_range_end
---

# Ghost Ledger Sheets Reader

## Description
Ghost Ledger tab name.

## Parameters
| Name | Type | Required | Description |
|------|------|----------|-------------|
| `ab_name` | `string` | Yes |  |
| `date_range_start` | `string` | Yes |  |
| `date_range_end` | `string` | Yes |  |

## Returns
Standard Snowdrop envelope:
```json
{"status": "ok"|"error", "data": {...}, "timestamp": "ISO8601"}
```

## Example
```json
{
  "tool": "ghost_ledger_sheets_reader",
  "arguments": {
    "ab_name": "<ab_name>",
    "date_range_start": "<date_range_start>",
    "date_range_end": "<date_range_end>"
  }
}
```

## Usage
Invoke via `snowdrop_execute` with `tool_name: "ghost_ledger_sheets_reader"`.
