---
skill: vacancy_rate_calculator
category: real_estate
description: Calculate vacancy rate from total and vacant units. Estimates revenue loss based on vacancy.
tier: free
inputs: total_units, vacant_units
---

# Vacancy Rate Calculator

## Description
Calculate vacancy rate from total and vacant units. Estimates revenue loss based on vacancy.

## Parameters
| Name | Type | Required | Description |
|------|------|----------|-------------|
| `total_units` | `integer` | Yes | Total number of units in the property. |
| `vacant_units` | `integer` | Yes | Number of currently vacant units. |

## Returns
Standard Snowdrop envelope:
```json
{"status": "ok"|"error", "data": {...}, "timestamp": "ISO8601"}
```

## Example
```json
{
  "tool": "vacancy_rate_calculator",
  "arguments": {
    "total_units": 0,
    "vacant_units": 0
  }
}
```

## Usage
Invoke via `snowdrop_execute` with `tool_name: "vacancy_rate_calculator"`.
