---
skill: debt_capacity_calculator
category: credit_analysis
description: Computes leverage and cash-flow-based debt capacity estimates.
tier: free
inputs: ebitda, interest_rate, capex, working_capital_change, tax_rate
---

# Debt Capacity Calculator

## Description
Computes leverage and cash-flow-based debt capacity estimates.

## Parameters
| Name | Type | Required | Description |
|------|------|----------|-------------|
| `ebitda` | `number` | Yes |  |
| `max_leverage_ratio` | `number` | No |  |
| `interest_rate` | `number` | Yes |  |
| `min_dscr` | `number` | No |  |
| `capex` | `number` | Yes |  |
| `working_capital_change` | `number` | Yes |  |
| `tax_rate` | `number` | Yes |  |

## Returns
Standard Snowdrop envelope:
```json
{"status": "ok"|"error", "data": {...}, "timestamp": "ISO8601"}
```

## Example
```json
{
  "tool": "debt_capacity_calculator",
  "arguments": {
    "ebitda": 0,
    "interest_rate": 0,
    "capex": 0,
    "working_capital_change": 0,
    "tax_rate": 0
  }
}
```

## Usage
Invoke via `snowdrop_execute` with `tool_name: "debt_capacity_calculator"`.
