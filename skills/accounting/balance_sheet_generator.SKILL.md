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
| `trial_balance` | `array` | Yes | List of account objects with `account_number`, `name`, `type` (asset/liability/equity), and `balance` fields. |
| `as_of_date` | `string` | Yes | Balance sheet date in ISO 8601 format (e.g. "2024-12-31"). |
| `entity_name` | `string` | No | Legal entity name; defaults to "Stonewater Solutions LLC". |

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
