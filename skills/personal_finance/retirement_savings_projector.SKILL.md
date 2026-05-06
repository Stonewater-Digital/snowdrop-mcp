---
skill: retirement_savings_projector
category: personal_finance
description: Forecasts retirement savings from current age to retirement, reporting nominal and inflation-adjusted balances plus a 4% rule shortfall analysis.
tier: free
inputs: current_age, retirement_age, current_balance, annual_contribution, annual_return, inflation_rate
---

# Retirement Savings Projector

## Description
Forecasts retirement savings from current age to retirement, reporting nominal and inflation-adjusted balances plus a 4% rule shortfall analysis.

## Parameters
| Name | Type | Required | Description |
|------|------|----------|-------------|
| `current_age` | `number` | Yes | Current age in years, must be non-negative. |
| `retirement_age` | `number` | Yes | Planned retirement age in years, must exceed current_age. |
| `current_balance` | `number` | Yes | Existing retirement savings in dollars. |
| `annual_contribution` | `number` | Yes | Annual contribution amount in dollars (pre-inflation). |
| `annual_return` | `number` | Yes | Expected annual investment return as decimal. |
| `inflation_rate` | `number` | Yes | Estimated annual inflation rate as decimal. |

## Returns
Standard Snowdrop envelope:
```json
{"status": "ok"|"error", "data": {...}, "timestamp": "ISO8601"}
```

## Example
```json
{
  "tool": "retirement_savings_projector",
  "arguments": {
    "current_age": 0,
    "retirement_age": 0,
    "current_balance": 0,
    "annual_contribution": 0,
    "annual_return": 0,
    "inflation_rate": 0
  }
}
```

## Usage
Invoke via `snowdrop_execute` with `tool_name: "retirement_savings_projector"`.
