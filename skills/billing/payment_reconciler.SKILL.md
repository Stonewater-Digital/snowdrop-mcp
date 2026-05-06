---
skill: payment_reconciler
category: billing
description: Reconciles Watering Hole payments against invoice records.
tier: free
inputs: payments, invoices
---

# Payment Reconciler

## Description
Reconciles Watering Hole payments against invoice records.

## Parameters
| Name | Type | Required | Description |
|------|------|----------|-------------|
| `payments` | `array` | Yes |  |
| `invoices` | `array` | Yes |  |

## Returns
Standard Snowdrop envelope:
```json
{"status": "ok"|"error", "data": {...}, "timestamp": "ISO8601"}
```

## Example
```json
{
  "tool": "payment_reconciler",
  "arguments": {
    "payments": [],
    "invoices": []
  }
}
```

## Usage
Invoke via `snowdrop_execute` with `tool_name: "payment_reconciler"`.
