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
| `recurring_revenue` | `array` | Yes | List of recurring revenue sources, each with key `monthly_amount` (number in USD). |
| `recurring_expenses` | `array` | Yes | List of recurring expense items, each with key `monthly_amount` (number in USD). |
| `one_time_items` | `array` | Yes | List of one-time cash items, each with keys `month` (integer, 1-indexed) and `amount` (number, positive=inflow, negative=outflow). Pass `[]` if none. |
| `months_forward` | `integer` | No | Number of months to project forward (default: 6). |

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
    "recurring_revenue": [{"monthly_amount": 25000}, {"monthly_amount": 8000}],
    "recurring_expenses": [{"monthly_amount": 18000}, {"monthly_amount": 6500}],
    "one_time_items": [{"month": 2, "amount": -15000}],
    "months_forward": 6
  }
}
```

## Usage
Invoke via `snowdrop_execute` with `tool_name: "cash_flow_projector"`.
