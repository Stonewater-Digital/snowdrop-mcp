---
skill: budget_variance_analyzer
category: budgeting
description: Compares actuals to budget with variance labeling and assessments.
tier: free
inputs: budget, actuals, period
---

# Budget Variance Analyzer

## Description
Compares actuals to budget with variance labeling and assessments.

## Parameters
| Name | Type | Required | Description |
|------|------|----------|-------------|
| `budget` | `array` | Yes | List of budget line objects, each with `category` (string) and `budgeted_amount` (number, USD). One object per expense or revenue category. |
| `actuals` | `array` | Yes | List of actual spend/revenue objects, each with `category` (string, must match a budget category) and `actual_amount` (number, USD). |
| `period` | `string` | Yes | Human-readable label for the period being analyzed (e.g. "April 2026" or "Q1 2026"). Included in output for context. |

## Returns
Standard Snowdrop envelope:
```json
{"status": "ok"|"error", "data": {...}, "timestamp": "ISO8601"}
```

## Example
```json
{
  "tool": "budget_variance_analyzer",
  "arguments": {
    "budget": [
      {"category": "Infrastructure", "budgeted_amount": 1200},
      {"category": "Payroll", "budgeted_amount": 5000},
      {"category": "Marketing", "budgeted_amount": 800}
    ],
    "actuals": [
      {"category": "Infrastructure", "actual_amount": 1350},
      {"category": "Payroll", "actual_amount": 5000},
      {"category": "Marketing", "actual_amount": 620}
    ],
    "period": "April 2026"
  }
}
```

## Usage
Invoke via `snowdrop_execute` with `tool_name: "budget_variance_analyzer"`.
