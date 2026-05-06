---
skill: barista_fire_calculator
category: budgeting
description: Calculates Barista FIRE number: the portfolio needed to cover the gap between expenses and part-time income.
tier: free
inputs: annual_expenses, part_time_income, current_savings
---

# Barista Fire Calculator

## Description
Calculates Barista FIRE number: the portfolio needed to cover the gap between expenses and part-time income.

## Parameters
| Name | Type | Required | Description |
|------|------|----------|-------------|
| `annual_expenses` | `number` | Yes | Total annual living expenses in dollars. |
| `part_time_income` | `number` | Yes | Expected annual income from part-time or flexible work in dollars. |
| `current_savings` | `number` | Yes | Current total invested savings in dollars. |
| `expected_return` | `number` | No | Expected annual real investment return as a decimal (default: 0.07). |

## Returns
Standard Snowdrop envelope:
```json
{"status": "ok"|"error", "data": {...}, "timestamp": "ISO8601"}
```

## Example
```json
{
  "tool": "barista_fire_calculator",
  "arguments": {
    "annual_expenses": 0,
    "part_time_income": 0,
    "current_savings": 0
  }
}
```

## Usage
Invoke via `snowdrop_execute` with `tool_name: "barista_fire_calculator"`.
