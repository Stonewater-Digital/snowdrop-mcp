---
skill: trial_balance_generator
category: accounting
description: Aggregates journal entries into account-level debit/credit totals.
tier: free
inputs: journal_entries, as_of_date
---

# Trial Balance Generator

## Description
Aggregates journal entries into account-level debit/credit totals.

## Parameters
| Name | Type | Required | Description |
|------|------|----------|-------------|
| `journal_entries` | `array` | Yes |  |
| `as_of_date` | `string` | Yes |  |

## Returns
Standard Snowdrop envelope:
```json
{"status": "ok"|"error", "data": {...}, "timestamp": "ISO8601"}
```

## Example
```json
{
  "tool": "trial_balance_generator",
  "arguments": {
    "journal_entries": [],
    "as_of_date": "<as_of_date>"
  }
}
```

## Usage
Invoke via `snowdrop_execute` with `tool_name: "trial_balance_generator"`.
