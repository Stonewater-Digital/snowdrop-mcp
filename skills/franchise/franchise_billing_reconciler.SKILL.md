---
skill: franchise_billing_reconciler
category: franchise
description: Calculates royalty balances for each franchise operator.
tier: free
inputs: operators
---

# Franchise Billing Reconciler

## Description
Calculates royalty balances for each franchise operator.

## Parameters
| Name | Type | Required | Description |
|------|------|----------|-------------|
| `operators` | `array` | Yes |  |

## Returns
Standard Snowdrop envelope:
```json
{"status": "ok"|"error", "data": {...}, "timestamp": "ISO8601"}
```

## Example
```json
{
  "tool": "franchise_billing_reconciler",
  "arguments": {
    "operators": []
  }
}
```

## Usage
Invoke via `snowdrop_execute` with `tool_name: "franchise_billing_reconciler"`.
