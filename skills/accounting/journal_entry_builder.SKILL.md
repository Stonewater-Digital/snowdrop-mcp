---
skill: journal_entry_builder
category: accounting
description: Builds balanced journal entries and assigns sequential IDs.
tier: free
inputs: date, description, lines
---

# Journal Entry Builder

## Description
Builds balanced journal entries and assigns sequential IDs.

## Parameters
| Name | Type | Required | Description |
|------|------|----------|-------------|
| `date` | `string` | Yes |  |
| `description` | `string` | Yes |  |
| `lines` | `array` | Yes | Journal lines with account_number, debit, credit |

## Returns
Standard Snowdrop envelope:
```json
{"status": "ok"|"error", "data": {...}, "timestamp": "ISO8601"}
```

## Example
```json
{
  "tool": "journal_entry_builder",
  "arguments": {
    "date": "<date>",
    "description": "<description>",
    "lines": []
  }
}
```

## Usage
Invoke via `snowdrop_execute` with `tool_name: "journal_entry_builder"`.
