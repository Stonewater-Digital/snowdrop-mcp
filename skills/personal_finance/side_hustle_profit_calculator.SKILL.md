---
skill: side_hustle_profit_calculator
category: personal_finance
description: Calculate profit, effective hourly rate, and estimated tax liability from a side hustle or gig work.
tier: free
inputs: revenue, expenses, hours_worked
---

# Side Hustle Profit Calculator

## Description
Calculate profit, effective hourly rate, and estimated tax liability from a side hustle or gig work.

## Parameters
| Name | Type | Required | Description |
|------|------|----------|-------------|
| `revenue` | `number` | Yes | Total revenue earned. |
| `expenses` | `array` | Yes | List of expense items with name and amount. |
| `hours_worked` | `number` | Yes | Total hours worked on the side hustle. |

## Returns
Standard Snowdrop envelope:
```json
{"status": "ok"|"error", "data": {...}, "timestamp": "ISO8601"}
```

## Example
```json
{
  "tool": "side_hustle_profit_calculator",
  "arguments": {
    "revenue": 0,
    "expenses": [],
    "hours_worked": 0
  }
}
```

## Usage
Invoke via `snowdrop_execute` with `tool_name: "side_hustle_profit_calculator"`.
