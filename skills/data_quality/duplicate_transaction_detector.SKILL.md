---
skill: duplicate_transaction_detector
category: data_quality
description: Finds exact and fuzzy duplicate transactions for Ghost Ledger hygiene.
tier: free
inputs: transactions
---

# Duplicate Transaction Detector

## Description
Finds exact and fuzzy duplicate transactions for Ghost Ledger hygiene.

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
  "tool": "duplicate_transaction_detector",
  "arguments": {
    "transactions": []
  }
}
```

## Usage
Invoke via `snowdrop_execute` with `tool_name: "duplicate_transaction_detector"`.
