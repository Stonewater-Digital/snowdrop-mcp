---
skill: emergency_fund_calculator
category: personal_finance
description: Determines the ideal emergency fund amount by weighing monthly expenses, income stability, and dependents while highlighting current coverage gaps.
tier: free
inputs: monthly_expenses, income_stability, dependents, existing_savings
---

# Emergency Fund Calculator

## Description
Determines the ideal emergency fund amount by weighing monthly expenses, income stability, and dependents while highlighting current coverage gaps.

## Parameters
| Name | Type | Required | Description |
|------|------|----------|-------------|
| `monthly_expenses` | `number` | Yes | Average essential monthly expenses in dollars, must be positive. |
| `income_stability` | `string` | Yes | Job income stability: stable, variable, or freelance. |
| `dependents` | `number` | Yes | Number of people relying on this income, must be non-negative. |
| `existing_savings` | `number` | Yes | Liquid savings already available for emergencies, non-negative. |

## Returns
Standard Snowdrop envelope:
```json
{"status": "ok"|"error", "data": {...}, "timestamp": "ISO8601"}
```

## Example
```json
{
  "tool": "emergency_fund_calculator",
  "arguments": {
    "monthly_expenses": 0,
    "income_stability": "<income_stability>",
    "dependents": 0,
    "existing_savings": 0
  }
}
```

## Usage
Invoke via `snowdrop_execute` with `tool_name: "emergency_fund_calculator"`.
