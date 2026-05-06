---
skill: cash_flow_projector
category: treasury
description: Computes monthly cash flow projections with cumulative balances and risk flags.
tier: free
inputs: recurring_revenue, recurring_expenses, one_time_items
---

# Cash Flow Projector

## Description
Computes monthly cash flow projections with cumulative balances and risk flags.

## Parameters
| Name | Type | Required | Description |
|------|------|----------|-------------|
| `recurring_revenue` | `array` | Yes |  |
| `recurring_expenses` | `array` | Yes |  |
| `one_time_items` | `array` | Yes |  |
| `months_forward` | `integer` | No |  |

## Returns
Standard Snowdrop envelope:
```json
{"status": "ok"|"error", "data": {...}, "timestamp": "ISO8601"}
```

## Example
```json
{
  "tool": "cash_flow_projector",
  "arguments": {
    "recurring_revenue": [],
    "recurring_expenses": [],
    "one_time_items": []
  }
}
```

## Usage
Invoke via `snowdrop_execute` with `tool_name: "cash_flow_projector"`.
