---
skill: fire_number_calculator
category: personal_finance
description: Computes the FIRE nest egg based on expenses and withdrawal rate, simulates years to reach it with contributions, and reports Coast/Barista FIRE thresholds.
tier: free
inputs: annual_expenses, withdrawal_rate, current_savings, annual_savings, investment_return
---

# Fire Number Calculator

## Description
Computes the FIRE nest egg based on expenses and withdrawal rate, simulates years to reach it with contributions, and reports Coast/Barista FIRE thresholds.

## Parameters
| Name | Type | Required | Description |
|------|------|----------|-------------|
| `annual_expenses` | `number` | Yes | Target annual spending in retirement. |
| `withdrawal_rate` | `number` | Yes | Safe withdrawal rate as decimal (e.g., 0.04). |
| `current_savings` | `number` | Yes | Existing investable assets. |
| `annual_savings` | `number` | Yes | Annual contributions to the portfolio. |
| `investment_return` | `number` | Yes | Expected annual investment return as decimal. |

## Returns
Standard Snowdrop envelope:
```json
{"status": "ok"|"error", "data": {...}, "timestamp": "ISO8601"}
```

## Example
```json
{
  "tool": "fire_number_calculator",
  "arguments": {
    "annual_expenses": 0,
    "withdrawal_rate": 0,
    "current_savings": 0,
    "annual_savings": 0,
    "investment_return": 0
  }
}
```

## Usage
Invoke via `snowdrop_execute` with `tool_name: "fire_number_calculator"`.
