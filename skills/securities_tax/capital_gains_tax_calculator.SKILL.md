---
skill: capital_gains_tax_calculator
category: securities_tax
description: Calculates realized capital gain tax based on holding period and jurisdiction.
tier: free
inputs: proceeds, cost_basis, holding_period_days
---

# Capital Gains Tax Calculator

## Description
Calculates realized capital gain tax based on holding period and jurisdiction.

## Parameters
| Name | Type | Required | Description |
|------|------|----------|-------------|
| `proceeds` | `number` | Yes |  |
| `cost_basis` | `number` | Yes |  |
| `holding_period_days` | `number` | Yes |  |
| `federal_rate_long_pct` | `number` | No |  |
| `federal_rate_short_pct` | `number` | No |  |
| `state_rate_pct` | `number` | No |  |

## Returns
Standard Snowdrop envelope:
```json
{"status": "ok"|"error", "data": {...}, "timestamp": "ISO8601"}
```

## Example
```json
{
  "tool": "capital_gains_tax_calculator",
  "arguments": {
    "proceeds": 0,
    "cost_basis": 0,
    "holding_period_days": 0
  }
}
```

## Usage
Invoke via `snowdrop_execute` with `tool_name: "capital_gains_tax_calculator"`.
