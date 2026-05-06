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
| `budget` | `array` | Yes |  |
| `actuals` | `array` | Yes |  |
| `period` | `string` | Yes |  |

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
    "budget": [],
    "actuals": [],
    "period": "<period>"
  }
}
```

## Usage
Invoke via `snowdrop_execute` with `tool_name: "budget_variance_analyzer"`.
