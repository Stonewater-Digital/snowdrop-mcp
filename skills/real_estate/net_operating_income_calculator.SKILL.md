---
skill: net_operating_income_calculator
category: real_estate
description: Calculate net operating income (NOI) from gross income, vacancy rate, and operating expenses. NOI = Effective Gross Income - Operating Expenses.
tier: free
inputs: gross_income
---

# Net Operating Income Calculator

## Description
Calculate net operating income (NOI) from gross income, vacancy rate, and operating expenses. NOI = Effective Gross Income - Operating Expenses.

## Parameters
| Name | Type | Required | Description |
|------|------|----------|-------------|
| `gross_income` | `number` | Yes | Potential gross annual rental income in USD. |
| `vacancy_rate` | `number` | No | Expected vacancy rate as a decimal (e.g. 0.05 for 5%). |
| `operating_expenses` | `number` | No | Total annual operating expenses (property tax, insurance, maintenance, management, etc.) in USD. |

## Returns
Standard Snowdrop envelope:
```json
{"status": "ok"|"error", "data": {...}, "timestamp": "ISO8601"}
```

## Example
```json
{
  "tool": "net_operating_income_calculator",
  "arguments": {
    "gross_income": 0
  }
}
```

## Usage
Invoke via `snowdrop_execute` with `tool_name: "net_operating_income_calculator"`.
