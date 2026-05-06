---
skill: operating_leverage_calculator
category: financial_analysis
description: Computes contribution margin, DOL, breakeven revenue, and scenario EBIT deltas.
tier: free
inputs: revenue, variable_costs, fixed_costs, revenue_change_scenarios
---

# Operating Leverage Calculator

## Description
Computes contribution margin, DOL, breakeven revenue, and scenario EBIT deltas.

## Parameters
| Name | Type | Required | Description |
|------|------|----------|-------------|
| `revenue` | `number` | Yes |  |
| `variable_costs` | `number` | Yes |  |
| `fixed_costs` | `number` | Yes |  |
| `revenue_change_scenarios` | `array` | Yes |  |

## Returns
Standard Snowdrop envelope:
```json
{"status": "ok"|"error", "data": {...}, "timestamp": "ISO8601"}
```

## Example
```json
{
  "tool": "operating_leverage_calculator",
  "arguments": {
    "revenue": 0,
    "variable_costs": 0,
    "fixed_costs": 0,
    "revenue_change_scenarios": []
  }
}
```

## Usage
Invoke via `snowdrop_execute` with `tool_name: "operating_leverage_calculator"`.
