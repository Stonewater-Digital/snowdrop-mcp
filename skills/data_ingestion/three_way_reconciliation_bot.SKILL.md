---
skill: three_way_reconciliation_bot
category: data_ingestion
description: Matches GL, administrator, and custodian balances to highlight breaks exceeding tolerance.
tier: free
inputs: gl_entries, admin_entries, custodian_entries
---

# Three Way Reconciliation Bot

## Description
Matches GL, administrator, and custodian balances to highlight breaks exceeding tolerance.

## Parameters
| Name | Type | Required | Description |
|------|------|----------|-------------|
| `gl_entries` | `array` | Yes | General ledger rows containing id, amount, currency. |
| `admin_entries` | `array` | Yes | Fund administrator records aligned to the same identifiers. |
| `custodian_entries` | `array` | Yes | Custodian records with positions/cash for reconciliation. |
| `tolerance` | `number` | No | Absolute variance tolerance (in source currency units). |

## Returns
Standard Snowdrop envelope:
```json
{"status": "ok"|"error", "data": {...}, "timestamp": "ISO8601"}
```

## Example
```json
{
  "tool": "three_way_reconciliation_bot",
  "arguments": {
    "gl_entries": [],
    "admin_entries": [],
    "custodian_entries": []
  }
}
```

## Usage
Invoke via `snowdrop_execute` with `tool_name: "three_way_reconciliation_bot"`.
