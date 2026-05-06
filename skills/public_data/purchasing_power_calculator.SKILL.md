---
skill: purchasing_power_calculator
category: public_data
description: Calculate how inflation erodes purchasing power over time. Shows future value of money in today's dollars.
tier: free
inputs: amount
---

# Purchasing Power Calculator

## Description
Calculate how inflation erodes purchasing power over time. Shows future value of money in today's dollars.

## Parameters
| Name | Type | Required | Description |
|------|------|----------|-------------|
| `amount` | `number` | Yes | Current dollar amount. |
| `annual_inflation` | `number` | No | Expected annual inflation rate as decimal (e.g., 0.03 for 3%). |
| `years` | `integer` | No | Number of years into the future. |

## Returns
Standard Snowdrop envelope:
```json
{"status": "ok"|"error", "data": {...}, "timestamp": "ISO8601"}
```

## Example
```json
{
  "tool": "purchasing_power_calculator",
  "arguments": {
    "amount": 0
  }
}
```

## Usage
Invoke via `snowdrop_execute` with `tool_name: "purchasing_power_calculator"`.
