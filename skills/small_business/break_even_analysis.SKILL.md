---
skill: break_even_analysis
category: small_business
description: Determines unit and revenue breakeven levels and runs pricing/cost what-if scenarios to stress test contribution margins.
tier: free
inputs: fixed_costs, variable_cost_per_unit, price_per_unit
---

# Break Even Analysis

## Description
Determines unit and revenue breakeven levels and runs pricing/cost what-if scenarios to stress test contribution margins.

## Parameters
| Name | Type | Required | Description |
|------|------|----------|-------------|
| `fixed_costs` | `number` | Yes | Total fixed costs per period. |
| `variable_cost_per_unit` | `number` | Yes | Variable cost per unit sold. |
| `price_per_unit` | `number` | Yes | Unit selling price. |

## Returns
Standard Snowdrop envelope:
```json
{"status": "ok"|"error", "data": {...}, "timestamp": "ISO8601"}
```

## Example
```json
{
  "tool": "break_even_analysis",
  "arguments": {
    "fixed_costs": 0,
    "variable_cost_per_unit": 0,
    "price_per_unit": 0
  }
}
```

## Usage
Invoke via `snowdrop_execute` with `tool_name: "break_even_analysis"`.
