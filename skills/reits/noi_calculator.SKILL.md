---
skill: noi_calculator
category: reits
description: Calculates NOI and margin from rental revenue and operating expenses.
tier: free
inputs: rental_revenue, operating_expenses
---

# Noi Calculator

## Description
Calculates NOI and margin from rental revenue and operating expenses.

## Parameters
| Name | Type | Required | Description |
|------|------|----------|-------------|
| `rental_revenue` | `number` | Yes |  |
| `other_income` | `number` | No |  |
| `operating_expenses` | `number` | Yes |  |
| `property_taxes` | `number` | No |  |
| `bad_debt` | `number` | No |  |

## Returns
Standard Snowdrop envelope:
```json
{"status": "ok"|"error", "data": {...}, "timestamp": "ISO8601"}
```

## Example
```json
{
  "tool": "noi_calculator",
  "arguments": {
    "rental_revenue": 0,
    "operating_expenses": 0
  }
}
```

## Usage
Invoke via `snowdrop_execute` with `tool_name: "noi_calculator"`.
