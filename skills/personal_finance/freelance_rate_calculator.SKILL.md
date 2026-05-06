---
skill: freelance_rate_calculator
category: personal_finance
description: Calculate the hourly rate a freelancer needs to charge to meet their target annual income after taxes and expenses.
tier: free
inputs: target_annual_income
---

# Freelance Rate Calculator

## Description
Calculate the hourly rate a freelancer needs to charge to meet their target annual income after taxes and expenses.

## Parameters
| Name | Type | Required | Description |
|------|------|----------|-------------|
| `target_annual_income` | `number` | Yes | Desired annual net income (take-home pay). |
| `billable_hours_per_week` | `number` | No | Expected billable hours per week. |
| `weeks_per_year` | `number` | No | Working weeks per year (accounting for vacation/sick time). |
| `expenses_pct` | `number` | No | Business expenses as fraction of gross revenue (e.g., 0.30 for 30%). |
| `tax_rate` | `number` | No | Estimated total tax rate as fraction (income + self-employment tax). |

## Returns
Standard Snowdrop envelope:
```json
{"status": "ok"|"error", "data": {...}, "timestamp": "ISO8601"}
```

## Example
```json
{
  "tool": "freelance_rate_calculator",
  "arguments": {
    "target_annual_income": 0
  }
}
```

## Usage
Invoke via `snowdrop_execute` with `tool_name: "freelance_rate_calculator"`.
