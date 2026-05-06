---
skill: lean_fire_calculator
category: budgeting
description: Calculates Lean FIRE target (25x of 60% of normal expenses) and years to achieve it.
tier: free
inputs: annual_expenses, current_savings, annual_savings
---

# Lean Fire Calculator

## Description
Calculates Lean FIRE target (25x of 60% of normal expenses) and years to achieve it.

## Parameters
| Name | Type | Required | Description |
|------|------|----------|-------------|
| `annual_expenses` | `number` | Yes | Current annual living expenses in dollars. |
| `current_savings` | `number` | Yes | Current total invested savings in dollars. |
| `annual_savings` | `number` | Yes | Amount saved and invested per year in dollars. |
| `expected_return` | `number` | No | Expected annual real investment return as a decimal (default: 0.07). |

## Returns
Standard Snowdrop envelope:
```json
{"status": "ok"|"error", "data": {...}, "timestamp": "ISO8601"}
```

## Example
```json
{
  "tool": "lean_fire_calculator",
  "arguments": {
    "annual_expenses": 0,
    "current_savings": 0,
    "annual_savings": 0
  }
}
```

## Usage
Invoke via `snowdrop_execute` with `tool_name: "lean_fire_calculator"`.
