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
| `journal_entries` | `array` | Yes | List of journal entry objects (as produced by `journal_entry_builder`), each containing a `lines` array with `account_number`, `debit`, and `credit`. |
| `as_of_date` | `string` | Yes | Report date in ISO 8601 format (e.g. "2024-12-31"); entries through this date are included. |

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
