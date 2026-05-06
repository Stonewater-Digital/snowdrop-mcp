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
| `revenue_assumptions` | `array` | Yes | List of revenue source objects, each with `source` (string label) and `monthly_amount` (number, base monthly USD amount). Optional `monthly_growth_rate` (decimal, e.g. 0.02 = 2% monthly growth) per source. |
| `expense_categories` | `array` | Yes | List of expense category objects, each with `category` (string label) and `monthly_amount` (number, base monthly USD amount). Optional `monthly_growth_rate` (decimal) per category. |
| `fiscal_year_start` | `string` | Yes | ISO date string for the start of the fiscal year (e.g. "2026-01-01"). Determines month labels across the 12-month projection. |

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
    "revenue_assumptions": [
      {"source": "MCP subscriptions", "monthly_amount": 8000, "monthly_growth_rate": 0.05},
      {"source": "Consulting", "monthly_amount": 3000}
    ],
    "expense_categories": [
      {"category": "Infrastructure", "monthly_amount": 1200},
      {"category": "Payroll", "monthly_amount": 5000, "monthly_growth_rate": 0.01}
    ],
    "fiscal_year_start": "2026-01-01"
  }
}
```

## Usage
Invoke via `snowdrop_execute` with `tool_name: "annual_budget_builder"`.
