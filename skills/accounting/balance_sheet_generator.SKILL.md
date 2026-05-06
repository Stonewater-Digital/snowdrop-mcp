---
skill: balance_sheet_generator
category: accounting
description: Groups trial balance entries into a balance sheet (A=L+E validation).
tier: free
inputs: trial_balance, as_of_date
---

# Balance Sheet Generator

## Description
Groups trial balance entries into a balance sheet (A=L+E validation).

## Parameters
| Name | Type | Required | Description |
|------|------|----------|-------------|
| `trial_balance` | `array` | Yes |  |
| `as_of_date` | `string` | Yes |  |
| `entity_name` | `string` | No |  |

## Returns
Standard Snowdrop envelope:
```json
{"status": "ok"|"error", "data": {...}, "timestamp": "ISO8601"}
```

## Example
```json
{
  "tool": "balance_sheet_generator",
  "arguments": {
    "trial_balance": [],
    "as_of_date": "<as_of_date>"
  }
}
```

## Usage
Invoke via `snowdrop_execute` with `tool_name: "balance_sheet_generator"`.
