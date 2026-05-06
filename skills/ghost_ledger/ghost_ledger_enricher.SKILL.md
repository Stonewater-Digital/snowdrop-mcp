---
skill: ghost_ledger_enricher
category: ghost_ledger
description: Annotates Ghost Ledger transactions with ROI heuristics and metadata.
tier: free
inputs: transactions
---

# Ghost Ledger Enricher

## Description
Annotates Ghost Ledger transactions with ROI heuristics and metadata.

## Parameters
| Name | Type | Required | Description |
|------|------|----------|-------------|
| `transactions` | `array` | Yes |  |

## Returns
Standard Snowdrop envelope:
```json
{"status": "ok"|"error", "data": {...}, "timestamp": "ISO8601"}
```

## Example
```json
{
  "tool": "ghost_ledger_enricher",
  "arguments": {
    "transactions": []
  }
}
```

## Usage
Invoke via `snowdrop_execute` with `tool_name: "ghost_ledger_enricher"`.
