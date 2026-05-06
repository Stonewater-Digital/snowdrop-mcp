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
| `payments` | `array` | Yes | List of payment objects, each with keys: `payee_id` (string), `amount` (number), and optional metadata fields. |

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
    "payments": [
      {"payee_id": "contractor-001", "amount": 1500.00, "date": "2024-03-15"},
      {"payee_id": "contractor-001", "amount": 800.00, "date": "2024-04-01"}
    ]
  }
}
```

## Usage
Invoke via `snowdrop_execute` with `tool_name: "contractor_payment_tracker"`.
