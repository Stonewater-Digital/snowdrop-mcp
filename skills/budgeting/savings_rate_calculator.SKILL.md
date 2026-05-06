---
skill: savings_rate_calculator
category: budgeting
description: Calculates savings rate as a percentage of gross income and classifies the result.
tier: free
inputs: gross_income, total_savings
---

# Savings Rate Calculator

## Description
Calculates savings rate as a percentage of gross income and classifies the result.

## Parameters
| Name | Type | Required | Description |
|------|------|----------|-------------|
| `gross_income` | `number` | Yes | Monthly or annual gross income in dollars. |
| `total_savings` | `number` | Yes | Monthly or annual total savings/investments in dollars (same period as income). |

## Returns
Standard Snowdrop envelope:
```json
{"status": "ok"|"error", "data": {...}, "timestamp": "ISO8601"}
```

## Example
```json
{
  "tool": "savings_rate_calculator",
  "arguments": {
    "gross_income": 0,
    "total_savings": 0
  }
}
```

## Usage
Invoke via `snowdrop_execute` with `tool_name: "savings_rate_calculator"`.
