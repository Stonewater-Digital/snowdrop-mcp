---
skill: inflation_adjusted_return
category: personal_finance
description: Calculates nominal versus real returns by discounting investment growth for inflation and highlighting purchasing power erosion.
tier: free
inputs: nominal_return, inflation_rate, years, initial_investment
---

# Inflation Adjusted Return

## Description
Calculates nominal versus real returns by discounting investment growth for inflation and highlighting purchasing power erosion.

## Parameters
| Name | Type | Required | Description |
|------|------|----------|-------------|
| `nominal_return` | `number` | Yes | Nominal annual return as decimal. |
| `inflation_rate` | `number` | Yes | Annual inflation rate as decimal. |
| `years` | `number` | Yes | Investment horizon in years. |
| `initial_investment` | `number` | Yes | Starting principal in dollars, must be positive. |

## Returns
Standard Snowdrop envelope:
```json
{"status": "ok"|"error", "data": {...}, "timestamp": "ISO8601"}
```

## Example
```json
{
  "tool": "inflation_adjusted_return",
  "arguments": {
    "nominal_return": 0,
    "inflation_rate": 0,
    "years": 0,
    "initial_investment": 0
  }
}
```

## Usage
Invoke via `snowdrop_execute` with `tool_name: "inflation_adjusted_return"`.
