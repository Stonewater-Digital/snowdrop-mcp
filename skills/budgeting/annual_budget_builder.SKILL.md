---
skill: annual_budget_builder
category: budgeting
description: Projects monthly revenue/expense totals with growth assumptions for 12 months.
tier: free
inputs: revenue_assumptions, expense_categories, fiscal_year_start
---

# Annual Budget Builder

## Description
Projects monthly revenue/expense totals with growth assumptions for 12 months.

## Parameters
| Name | Type | Required | Description |
|------|------|----------|-------------|
| `revenue_assumptions` | `array` | Yes |  |
| `expense_categories` | `array` | Yes |  |
| `fiscal_year_start` | `string` | Yes | ISO date of fiscal year start. |

## Returns
Standard Snowdrop envelope:
```json
{"status": "ok"|"error", "data": {...}, "timestamp": "ISO8601"}
```

## Example
```json
{
  "tool": "annual_budget_builder",
  "arguments": {
    "revenue_assumptions": [],
    "expense_categories": [],
    "fiscal_year_start": "<fiscal_year_start>"
  }
}
```

## Usage
Invoke via `snowdrop_execute` with `tool_name: "annual_budget_builder"`.
