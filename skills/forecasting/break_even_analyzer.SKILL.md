---
skill: break_even_analyzer
category: forecasting
description: Computes break-even units, revenue, margin of safety, and estimated time to break even.
tier: free
inputs: fixed_costs_monthly, variable_cost_per_unit, price_per_unit, current_monthly_units
---

# Break Even Analyzer

## Description
Computes break-even units, revenue, margin of safety, and estimated time to break even.

## Parameters
| Name | Type | Required | Description |
|------|------|----------|-------------|
| `fixed_costs_monthly` | `number` | Yes |  |
| `variable_cost_per_unit` | `number` | Yes |  |
| `price_per_unit` | `number` | Yes |  |
| `current_monthly_units` | `integer` | Yes |  |

## Returns
Standard Snowdrop envelope:
```json
{"status": "ok"|"error", "data": {...}, "timestamp": "ISO8601"}
```

## Example
```json
{
  "tool": "break_even_analyzer",
  "arguments": {
    "fixed_costs_monthly": 0,
    "variable_cost_per_unit": 0,
    "price_per_unit": 0,
    "current_monthly_units": 0
  }
}
```

## Usage
Invoke via `snowdrop_execute` with `tool_name: "break_even_analyzer"`.
