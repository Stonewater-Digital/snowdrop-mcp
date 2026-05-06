---
skill: payment_history_analyzer
category: credit
description: Analyze payment history by computing on-time percentage and assessing impact on credit score.
tier: free
inputs: total_payments, on_time_payments
---

# Payment History Analyzer

## Description
Analyze payment history by computing on-time percentage and assessing impact on credit score.

## Parameters
| Name | Type | Required | Description |
|------|------|----------|-------------|
| `total_payments` | `integer` | Yes | Total number of payments made. |
| `on_time_payments` | `integer` | Yes | Number of payments made on time. |

## Returns
Standard Snowdrop envelope:
```json
{"status": "ok"|"error", "data": {...}, "timestamp": "ISO8601"}
```

## Example
```json
{
  "tool": "payment_history_analyzer",
  "arguments": {
    "total_payments": 0,
    "on_time_payments": 0
  }
}
```

## Usage
Invoke via `snowdrop_execute` with `tool_name: "payment_history_analyzer"`.
