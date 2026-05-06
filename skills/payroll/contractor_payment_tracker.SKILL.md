---
skill: contractor_payment_tracker
category: payroll
description: Aggregates contractor payments and flags 1099 thresholds.
tier: free
inputs: payments
---

# Contractor Payment Tracker

## Description
Aggregates contractor payments and flags 1099 thresholds.

## Parameters
| Name | Type | Required | Description |
|------|------|----------|-------------|
| `payments` | `array` | Yes |  |

## Returns
Standard Snowdrop envelope:
```json
{"status": "ok"|"error", "data": {...}, "timestamp": "ISO8601"}
```

## Example
```json
{
  "tool": "contractor_payment_tracker",
  "arguments": {
    "payments": []
  }
}
```

## Usage
Invoke via `snowdrop_execute` with `tool_name: "contractor_payment_tracker"`.
