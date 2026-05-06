---
skill: four_percent_rule_calculator
category: personal_finance
description: Applies the 4% rule to approximate sustainable withdrawals, adjusts for desired horizon and inflation, and scores success probability heuristically.
tier: free
inputs: portfolio_balance, annual_expenses, inflation_rate, retirement_years
---

# Four Percent Rule Calculator

## Description
Applies the 4% rule to approximate sustainable withdrawals, adjusts for desired horizon and inflation, and scores success probability heuristically.

## Parameters
| Name | Type | Required | Description |
|------|------|----------|-------------|
| `portfolio_balance` | `number` | Yes | Current investable retirement portfolio in dollars. |
| `annual_expenses` | `number` | Yes | Desired annual retirement spending in dollars. |
| `inflation_rate` | `number` | Yes | Expected annual inflation rate as decimal. |
| `retirement_years` | `number` | Yes | Planning horizon in years, typically 25-35. |

## Returns
Standard Snowdrop envelope:
```json
{"status": "ok"|"error", "data": {...}, "timestamp": "ISO8601"}
```

## Example
```json
{
  "tool": "four_percent_rule_calculator",
  "arguments": {
    "portfolio_balance": 0,
    "annual_expenses": 0,
    "inflation_rate": 0,
    "retirement_years": 0
  }
}
```

## Usage
Invoke via `snowdrop_execute` with `tool_name: "four_percent_rule_calculator"`.
