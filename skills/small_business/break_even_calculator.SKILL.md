---
skill: break_even_calculator
category: small_business
description: Calculate the break-even point: units needed and revenue at which total costs equal total revenue.
tier: free
inputs: fixed_costs, price_per_unit, variable_cost_per_unit
---

# Break Even Calculator

## Description
Calculate the break-even point: units needed and revenue at which total costs equal total revenue.

## Parameters
| Name | Type | Required | Description |
|------|------|----------|-------------|
| `fixed_costs` | `number` | Yes | Total fixed costs. |
| `price_per_unit` | `number` | Yes | Selling price per unit. |
| `variable_cost_per_unit` | `number` | Yes | Variable cost per unit. |

## Returns
Standard Snowdrop envelope:
```json
{"status": "ok"|"error", "data": {...}, "timestamp": "ISO8601"}
```

## Example
```json
{
  "tool": "break_even_calculator",
  "arguments": {
    "fixed_costs": 0,
    "price_per_unit": 0,
    "variable_cost_per_unit": 0
  }
}
```

## Usage
Invoke via `snowdrop_execute` with `tool_name: "break_even_calculator"`.
