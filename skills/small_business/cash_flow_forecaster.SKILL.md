---
skill: cash_flow_forecaster
category: small_business
description: Builds a 12-month cash forecast factoring in revenue growth, fixed operating costs, variable expenses, and scheduled one-time cash outlays.
tier: free
inputs: starting_cash, monthly_revenue, revenue_growth_rate, fixed_expenses, variable_expense_pct, one_time_expenses
---

# Cash Flow Forecaster

## Description
Builds a 12-month cash forecast factoring in revenue growth, fixed operating costs, variable expenses, and scheduled one-time cash outlays.

## Parameters
| Name | Type | Required | Description |
|------|------|----------|-------------|
| `starting_cash` | `number` | Yes | Beginning cash balance. |
| `monthly_revenue` | `number` | Yes | Current monthly revenue run rate. |
| `revenue_growth_rate` | `number` | Yes | Expected monthly growth rate as decimal. |
| `fixed_expenses` | `array` | Yes | List of fixed expenses per month. |
| `variable_expense_pct` | `number` | Yes | Variable expense percentage of revenue. |
| `one_time_expenses` | `array` | Yes | List of {month, amount} one-time cash items. |

## Returns
Standard Snowdrop envelope:
```json
{"status": "ok"|"error", "data": {...}, "timestamp": "ISO8601"}
```

## Example
```json
{
  "tool": "cash_flow_forecaster",
  "arguments": {
    "starting_cash": 0,
    "monthly_revenue": 0,
    "revenue_growth_rate": 0,
    "fixed_expenses": [],
    "variable_expense_pct": 0,
    "one_time_expenses": []
  }
}
```

## Usage
Invoke via `snowdrop_execute` with `tool_name: "cash_flow_forecaster"`.
